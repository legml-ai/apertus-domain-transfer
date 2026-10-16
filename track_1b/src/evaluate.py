"""Track 1B evaluation harness: SimpleQA-style grading of model responses against sourced references.

Pipeline (all steps are idempotent and write under RESULTS_DIR, default track_1b/results):

  1. load      pull the public leGML datasets from Hugging Face (questions + references, model responses)
  2. grade     ask an LLM judge (OpenAI-compatible endpoint, LLM_NAME / LLM_BASE_URL / LLM_API_KEY) to label every
               response CORRECT / INCORRECT / NOT_ATTEMPTED against the reference; cached per (system, id)
  3. score     compute counts and rates per system, per language; write results.json and results.md
  4. verify    recompute the scores from the committed judgements file and compare with the committed results

Without API credentials the harness still runs: it uses the committed judgements (track_1b/results/judgements.jsonl)
and only re-scores and verifies, which is what judges need for a deterministic check. With credentials it re-judges
any response that has no cached judgement.

Grading rubric (SimpleQA): CORRECT if the response contains the reference's key legal conclusion(s) without
contradicting them; INCORRECT if it states something that contradicts the reference or invents a legal basis;
NOT_ATTEMPTED if the response does not commit to an answer (declines, only asks questions, stops mid-way).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RESULTS = Path(os.environ.get("RESULTS_DIR", ROOT / "results"))

QUESTIONS_REPO = "legmlai/swiss-insurance-eval"
RESPONSES_REPO = "legmlai/swiss-insurance-eval-responses"
SYSTEMS = {"vanilla": "vanilla_apertus_8b_instruct.jsonl", "ours": "ours.jsonl"}
LABELS = ("CORRECT", "INCORRECT", "NOT_ATTEMPTED")

JUDGE_SYSTEM = (
    "You grade answers to questions on Swiss private insurance law. You get the question, a reference answer written "
    "by a domain reviewer with source citations, and a candidate answer. Output exactly one word: CORRECT if the "
    "candidate states the reference's key legal conclusions and does not contradict them (extra correct detail and "
    "different wording are fine); INCORRECT if the candidate contradicts the reference, invents a legal basis "
    "(article, ruling, authority) not supported by the reference, or answers a different question; NOT_ATTEMPTED if "
    "the candidate does not commit to an answer (only lists open points, only asks questions, declines, or stops "
    "before answering). Judge content, not style, length or citations."
)


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------- 1. load

def load(data_dir: Path, revision_q: str | None, revision_r: str | None) -> tuple[list[dict], dict[str, list[dict]]]:
    from huggingface_hub import hf_hub_download

    q_path = hf_hub_download(QUESTIONS_REPO, "test_cases/questions.jsonl", repo_type="dataset",
                             revision=revision_q, local_dir=data_dir / "questions")
    questions = read_jsonl(Path(q_path))
    responses = {}
    for system, fname in SYSTEMS.items():
        p = hf_hub_download(RESPONSES_REPO, fname, repo_type="dataset", revision=revision_r,
                            local_dir=data_dir / "responses")
        responses[system] = read_jsonl(Path(p))
    return questions, responses


# ---------------------------------------------------------------- 2. grade

def judge_client():
    name, base, key = os.environ.get("LLM_NAME"), os.environ.get("LLM_BASE_URL"), os.environ.get("LLM_API_KEY")
    if not (name and base and key):
        return None, None
    from openai import OpenAI
    return OpenAI(base_url=base, api_key=key, max_retries=3, timeout=120), name


def judge_one(client, model: str, question: str, reference: str, candidate: str) -> str:
    user = f"QUESTION:\n{question}\n\nREFERENCE ANSWER:\n{reference}\n\nCANDIDATE ANSWER:\n{candidate}\n\nLabel:"
    for attempt in range(3):
        r = client.chat.completions.create(model=model, temperature=0, max_tokens=5,
                                           messages=[{"role": "system", "content": JUDGE_SYSTEM},
                                                     {"role": "user", "content": user}])
        text = (r.choices[0].message.content or "").strip().upper().replace(" ", "_")
        for lab in LABELS:
            if text.startswith(lab):
                return lab
        time.sleep(1)
    return "NOT_ATTEMPTED"  # unparsable judge output is treated as no judgement, never as correct


def grade(questions: list[dict], responses: dict[str, list[dict]], judgements_path: Path) -> list[dict]:
    by_id = {q["id"]: q for q in questions}
    cached = {(j["system"], j["id"]): j for j in (read_jsonl(judgements_path) if judgements_path.exists() else [])}
    client, model = judge_client()
    out, todo = [], []
    for system, rows in responses.items():
        for r in rows:
            key = (system, r["id"])
            if key in cached:
                out.append(cached[key])
            else:
                todo.append((system, r))
    if todo and client is None:
        print(f"[grade] {len(todo)} responses have no cached judgement and no LLM credentials are set; "
              f"scoring the {len(out)} cached judgements only", file=sys.stderr)
    elif todo:
        print(f"[grade] judging {len(todo)} responses with {model}", file=sys.stderr)
        for n, (system, r) in enumerate(todo, 1):
            q = by_id[r["id"]]
            if "reference" not in q:
                raise SystemExit("questions file has no reference answers; use the revision with references")
            label = judge_one(client, model, q["question"], q["reference"], r.get("final_answer_text", ""))
            out.append({"system": system, "id": r["id"], "language": r.get("language", q.get("language")),
                        "label": label, "judge": model, "end": r.get("end"), "searches": len(r.get("searches", []))})
            if n % 20 == 0:
                write_jsonl(judgements_path, out)
                print(f"[grade] {n}/{len(todo)}", file=sys.stderr)
        write_jsonl(judgements_path, out)
    return out


# ---------------------------------------------------------------- 3. score

def score(judgements: list[dict]) -> dict:
    res: dict = {"systems": {}}
    for system in sorted({j["system"] for j in judgements}):
        js = [j for j in judgements if j["system"] == system]
        block = {"n": len(js), "overall": _rates(js), "by_language": {}}
        for lang in sorted({j.get("language") for j in js}):
            block["by_language"][lang] = _rates([j for j in js if j.get("language") == lang])
        res["systems"][system] = block
    res["judgements_sha256"] = hashlib.sha256(
        "\n".join(json.dumps(j, sort_keys=True, ensure_ascii=False) for j in
                  sorted(judgements, key=lambda j: (j["system"], j["id"]))).encode()).hexdigest()
    return res


def _rates(js: list[dict]) -> dict:
    c = Counter(j["label"] for j in js)
    n = max(len(js), 1)
    attempted = c["CORRECT"] + c["INCORRECT"]
    return {"n": len(js), **{lab: c[lab] for lab in LABELS},
            "correct_rate": round(c["CORRECT"] / n, 4), "incorrect_rate": round(c["INCORRECT"] / n, 4),
            "not_attempted_rate": round(c["NOT_ATTEMPTED"] / n, 4),
            "correct_given_attempted": round(c["CORRECT"] / attempted, 4) if attempted else None}


def render_md(res: dict) -> str:
    lines = ["# Results", "", "| system | n | correct | incorrect | not attempted | correct rate | correct given attempted |",
             "|---|---|---|---|---|---|---|"]
    for system, b in res["systems"].items():
        o = b["overall"]
        lines.append(f"| {system} | {o['n']} | {o['CORRECT']} | {o['INCORRECT']} | {o['NOT_ATTEMPTED']} | "
                     f"{o['correct_rate']:.1%} | {o['correct_given_attempted'] if o['correct_given_attempted'] is None else format(o['correct_given_attempted'], '.1%')} |")
    lines += ["", "## By language", "", "| system | language | n | correct | incorrect | not attempted | correct rate |", "|---|---|---|---|---|---|---|"]
    for system, b in res["systems"].items():
        for lang, o in b["by_language"].items():
            lines.append(f"| {system} | {lang} | {o['n']} | {o['CORRECT']} | {o['INCORRECT']} | {o['NOT_ATTEMPTED']} | {o['correct_rate']:.1%} |")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- 4. verify

def verify(res: dict, committed: Path) -> bool:
    if not committed.exists():
        print("[verify] no committed results to compare with; skipping", file=sys.stderr)
        return True
    old = json.loads(committed.read_text())
    same = old.get("systems") == res["systems"] and old.get("judgements_sha256") == res["judgements_sha256"]
    print(f"[verify] {'OK: recomputed scores match the committed results' if same else 'MISMATCH against committed results'}",
          file=sys.stderr)
    return same


# ---------------------------------------------------------------- main

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data-dir", type=Path, default=RESULTS / "data")
    ap.add_argument("--questions-revision", default=os.environ.get("QUESTIONS_REVISION"))
    ap.add_argument("--responses-revision", default=os.environ.get("RESPONSES_REVISION"))
    ap.add_argument("--offline", action="store_true", help="skip the Hub download; use the committed judgements only")
    ap.add_argument("--write", action="store_true", help="overwrite the committed results (maintainers only)")
    args = ap.parse_args(argv)

    RESULTS.mkdir(parents=True, exist_ok=True)
    judgements_path = RESULTS / "judgements.jsonl"
    if args.offline:
        judgements = read_jsonl(judgements_path) if judgements_path.exists() else []
    else:
        questions, responses = load(args.data_dir, args.questions_revision, args.responses_revision)
        print(f"[load] {len(questions)} questions; responses: " + ", ".join(f"{k}={len(v)}" for k, v in responses.items()),
              file=sys.stderr)
        judgements = grade(questions, responses, judgements_path)
    if not judgements:
        print("no judgements available: set LLM_NAME/LLM_BASE_URL/LLM_API_KEY to grade, or commit judgements.jsonl",
              file=sys.stderr)
        return 2
    res = score(judgements)
    out_json = RESULTS / ("results.json" if args.write else "results.recomputed.json")
    out_json.write_text(json.dumps(res, indent=1, ensure_ascii=False))
    (RESULTS / ("results.md" if args.write else "results.recomputed.md")).write_text(render_md(res))
    print(render_md(res))
    ok = verify(res, RESULTS / "results.json")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
