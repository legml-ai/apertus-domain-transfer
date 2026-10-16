# leGML — Teaching Apertus Swiss Insurance Law: Search, Quote, Cite

**Track:** Hack Apertus Online 2026 — Track 1B, Swiss Voices / Core Task Intelligence
**Team:** leGML — Mohamad Alhajar
**Repository:** https://github.com/legml-ai/apertus-domain-transfer
**Demo video:** [Watch the demo](https://drive.google.com/file/d/1M0_HGipQ7kq1pfYyo4aU-OVESDTRK8ht/view?usp=sharing)
**Datasets:** [swiss-insurance-eval](https://huggingface.co/datasets/legmlai/swiss-insurance-eval) (questions, metadata, contamination check) ·
[swiss-insurance-eval-responses](https://huggingface.co/datasets/legmlai/swiss-insurance-eval-responses) (model responses) ·
[swiss-insurance-sft-sample](https://huggingface.co/datasets/legmlai/swiss-insurance-sft-sample) ·
[swiss-insurance-pt-sample](https://huggingface.co/datasets/legmlai/swiss-insurance-pt-sample)
**Final PDF:** `leGML_Report.pdf`

----

## 1. Use case

People who deal with Swiss private insurance (insured persons, brokers, claims handlers and legal-aid desks) ask
questions like *"My supplementary health insurer refuses to pay for treatment abroad: what does Swiss law say?"*.
The answers depend on Swiss federal law: the Insurance Contract Act (VVG/LCA), supplementary health insurance,
liability and motor insurance (SVG/LCR), private international law (IPRG/LDIP, Lugano Convention), FINMA
supervision, and the practice of the Federal Court and the Ombudsman. Questions come in German and French.

General-purpose models fail here in three ways:
1. **They answer from memory.** Article numbers and rulings are recalled, not checked.
2. **They mix jurisdictions.** German and Swiss law share names: the German *VVG* and the Swiss *VVG* are different
   statutes with different article numbers. The same goes for French and Swiss-French terminology.
3. **They hide uncertainty.** Answers read as confident even when no source supports them.

**Goal.** Measure whether domain adaptation makes Apertus-8B answer these questions more correctly when it is
given a web-search tool, compared with the original Apertus-8B given the *same* tool.

**Scope and exclusions.** Federal private insurance law and its supervision, in German and French. Excluded:
cantonal law, social insurance as such (AHV/AVS, IV/AI, basic health insurance under KVG/LAMal), except where a
question explicitly contrasts it with private insurance, and Italian/Romansh. The model is not legal advice. Every
answer points to its sources so a human can check it.

## 2. Use of Apertus

| | Baseline | Adapted (ours) |
|---|---|---|
| Weights | `swiss-ai/Apertus-8B-Instruct-2509`, unchanged | `swiss-ai/Apertus-8B-2509` (rev. `3162c99`) → continued pretraining → SFT |
| Prompt | Apertus instruct chat template, pinned system date, one tool `web_search(query)` | identical |
| Search executor | Claude Haiku web search, top-10 results (url, title, age) returned as tool output | identical |
| Decoding | greedy, bf16, ≤2048 new tokens per segment, ≤8192 per question, ≤6 tool rounds | identical |
| Hardware | 1× NVIDIA H200, 2026-10-16 | identical |

Everything except the weights is held fixed, so the measured difference is the effect of the adaptation, not of
retrieval, tools or prompts.

**Adaptation.**
1. **Continued pretraining (CPT), 2 epochs.** ~43.7k segments of Swiss insurance text (29.2k German, 14.5k French;
   ~143M tokens) from public Swiss legal and insurance sources, mixed with general French text to limit
   forgetting. Full-parameter training in bf16 (no adapters) on 3× H200 with DeepSpeed ZeRO-3.
2. **Supervised fine-tuning (SFT), 2 epochs.** ~15.9k Swiss-insurance conversations (8.7k DE, 7.3k FR) plus 2.6k
   general French conversations, ~65M tokens, on 2× B200. The insurance conversations teach one behaviour: state
   what must be checked, call `web_search`, read the results, then answer with a verbatim quote and its URL for every
   legal claim, and say explicitly what could not be found. The format is shown in
   [swiss-insurance-sft-sample](https://huggingface.co/datasets/legmlai/swiss-insurance-sft-sample).

The adapted model is a full-weight 8B checkpoint (16 GB, bf16).

## 3. Dataset

### 3.1 Summary

| | |
|---|---|
| Test items | 300 single-turn questions (150 DE, 150 FR) |
| Ground truth | one sourced reference answer per question, with verbatim quotes and URLs |
| Model responses | Planned: 2 systems × 300 (tool calls, search results, final answer); verify completed exports before submission |
| Question length | median 51 words |
| Reference length | median ~780 words; median 7 cited URLs; 243/300 references cite at least one URL |
| Licence | CDLA-Permissive-2.0 |

### 3.2 Construction

1. **Questions.** Each question describes a concrete situation and asks how Swiss federal private insurance law
   applies to it, in German or French.
2. **Reference answers.** Each question was answered by an LLM with live web search. The answer quotes the
   retrieved sources verbatim with their URLs and lists what could not be found. The reference is the final answer
   of that conversation. 57/300 references cite no URL (the search found nothing usable); they still state which
   points remain open, and are kept so that abstention can be graded.
3. **Held-out split.** A fixed share of the conversations was held out by hash *before* any training run. The 300
   test items were sampled from this held-out pool, stratified by language with seed 11.
4. **Freeze.** The question set was frozen and published before grading (Hub revision `cc48f5d`).

### 3.3 Quality checks performed

- Structural checks when the split was built: well-formed tool calls and a final assistant answer; conversations
  that failed were rejected and are not in the pool.
- Held-out integrity: 0/300 held-out IDs occur in the training split.
- Contamination check, in section 3.5.
- Human audit of the grading on a random 20%: pending, see section 4.3.

### 3.4 Provenance and licensing

- Questions, references and model responses were generated for this project. They are published under
  CDLA-Permissive-2.0.
- Quotes inside references and responses come from public Swiss sources. Federal acts and Federal Court decisions
  are not protected by copyright (Art. 5 URG). Quotes from other sources are short citations with attribution
  (Art. 25 URG). Each quote carries its source URL, which gives instance-level provenance.
- No personal data. Situations are generic, with no names, policy numbers or identifiable persons.
- The training corpora are not published. The samples on the Hub show the format only, and the pretraining sample
  is restricted to Fedlex and Federal Court text.

### 3.5 Contamination

Full details are in `track_1b/docs/CONTAMINATION.md`.
- **Against Apertus training data:** all questions and references were written on 14–15 October 2026 and first
  published on 16 October 2026. Apertus-8B (September 2025) was trained on a frozen earlier corpus, so it cannot
  have seen them.
- **Against our training data:** 0/300 exact question matches. 66/300 questions and 118/300 references share at
  least one 13-word phrase with training text, at most 13% of a reference. When we read these overlaps by hand,
  they are the shared answer template plus a few same-topic sibling questions, not duplicated items.

## 4. Evaluation

### 4.1 Method

SimpleQA-style three-way grading by an LLM judge against the reference answer:
- **CORRECT:** states the reference's key legal conclusions without contradicting them.
- **INCORRECT:** contradicts the reference, invents a legal basis (article, ruling or authority) or answers a
  different question.
- **NOT_ATTEMPTED:** commits to no answer (only lists open points, declines, or stops before answering).

The judge is {{JUDGE_MODEL}}, at temperature 0, with the rubric in `src/evaluate.py`. It sees the question, the
reference and the candidate's final answer, but not which system produced it. The judge is chosen outside the
model family that wrote the references, to limit self-preference.

**Metrics.** We report the correct rate (CORRECT / 300), the incorrect rate (our hallucination proxy: committed but
wrong) and the not-attempted rate. We also report correct-given-attempted, CORRECT / (CORRECT + INCORRECT), which
rewards a model that abstains instead of guessing. Results are given per system and per language.

### 4.2 Results

| system | correct | incorrect | not attempted | correct rate | correct given attempted |
|---|---|---|---|---|---|
| Apertus-8B-Instruct (baseline) | {{C_BASE}} | {{I_BASE}} | {{NA_BASE}} | {{CR_BASE}} | {{CGA_BASE}} |
| Apertus-8B + leGML (ours) | {{C_OURS}} | {{I_OURS}} | {{NA_OURS}} | {{CR_OURS}} | {{CGA_OURS}} |

By language: {{TABLE_BY_LANGUAGE}}

**Tool use.** The baseline called `web_search` in {{BASE_SEARCH_RATE}} of questions; on its first 110 answers it
searched 3 times. Ours searched in {{OURS_SEARCH_RATE}}, with a mean of {{OURS_SEARCHES_MEAN}} searches per question.

### 4.3 Human audit

**Pending.** Draw a random 20% of completed judgements with seed {{AUDIT_SEED}}, and have them labelled independently
by a human annotator ({{AUDITOR}}) who does not see the judge label. If all 600 responses are graded, this requires
120 audited judgements across the two systems; report the actual sampling frame and coverage. Judge–human
agreement: {{AGREEMENT}} (Cohen's κ {{KAPPA}}). Add real disagreements and adjudication to `results/human_audit.csv`
before replacing this paragraph with completed-review results.

### 4.4 Error analysis

We observed the following failure modes of the adapted model in pilot runs. Their frequency over the full set is
{{ERROR_COUNTS}}.
- **Under-searching:** it plans 3–4 searches, then runs only 1, so the answer rests on a single result page.
- **Wrong instrument:** for example, it applied the Lugano Convention to a US judgment, although the US is not a
  party.
- **Unsupported citation:** a Federal Court reference that did not appear in the retrieved results.
- **Degeneration:** a sentence repeated at the end of a long answer under greedy decoding.
- **Malformed tool call:** an announced search that is never emitted.

The baseline's typical failure is a short answer from memory with no source. Some of these cite foreign (German or
French) law. {{BASE_FOREIGN_LAW_COUNT}}

## 5. Limitations

- **References are model-written.** Each reference is grounded in quoted Swiss sources, but no lawyer validated
  all 300. The human audit checks the judge, not the references. A wrong reference makes a correct answer look
  wrong for both systems alike.
- **Shared style.** Our SFT data and the references come from the same answer format, which could favour our model
  in the judge's eyes. The rubric scores legal content only; the planned human audit will check grading agreement.
- **Search is live.** Results depend on the web on 2026-10-16 and are not fully reproducible. All search results
  are stored with the responses, so grading is reproducible.
- **Temporal validity.** Law and case law change. The set reflects the state of October 2026.
- **Coverage.** Federal private insurance law only. No Italian, Romansh or cantonal law.
- **Model version.** We adapted Apertus 8B (2509). The track names Apertus v1.5; transferring the recipe to v1.5 is
  the next step.
- **Operational incident.** During generation an expired search credential returned empty results for a batch of
  answers. We detected it, fixed it and regenerated every affected item. No answer produced with failed searches is
  in the results.
- **No lawyer review of the training data.** The SFT conversations were filtered automatically, not reviewed by a
  lawyer; the adapted model can reproduce their mistakes.

## 6. Lessons learnt

- Holding retrieval fixed is essential. Without it, "better answers" cannot be separated from "better search".
- A base model given a search tool does not use it. Tool use has to be trained, and it transfers from a modest SFT
  set.
- Honest abstention ("not found") must be rewarded explicitly. Otherwise correct-rate metrics punish it.
- Next: a lawyer-validated subset of the references, sampling-based decoding to reduce loops, and Apertus v1.5.

## 7. Reproducibility

```bash
git clone https://github.com/legml-ai/apertus-domain-transfer && cd apertus-domain-transfer
make run      # Docker; downloads the datasets, re-scores committed judgements, verifies against results.json
```

- In the final bundle, without credentials, `make run` should recompute every score from committed
  `results/judgements.jsonl` and compare it with `results/results.json`, without a GPU or API.
  **Pending:** commit the actual judgements and results, and verify this workflow from a clean checkout.
- With a judge endpoint in `track_1b/.env` (`LLM_NAME`, `LLM_BASE_URL`, `LLM_API_KEY`, any OpenAI-compatible API),
  it grades any response without a cached judgement. New systems are added by uploading a responses file.
- Pinned versions: dataset revisions `cc48f5d` and {{RESPONSES_REVISION}}, code commit {{COMMIT}}.
- Regenerating the model responses is not part of `make run`. It needs a GPU with at least 40 GB and the search
  backend. The settings are listed in section 2.

## License

Code: Apache-2.0. Datasets: CDLA-Permissive-2.0. Report: CC-BY-4.0.

## References

- Hack Apertus Track 1B challenge — https://github.com/HackApertus/project-template/blob/main/track_1b/README.md
- Apertus models — https://huggingface.co/swiss-ai
- Wei et al., *Measuring short-form factuality in large language models* (SimpleQA), 2024.
- Fedlex, systematic compilation of federal law — https://www.fedlex.admin.ch
- Swiss Federal Supreme Court — https://www.bger.ch
