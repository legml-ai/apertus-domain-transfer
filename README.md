# leGML — Apertus Domain Knowledge Transfer

Hack Apertus Online 2026 · **Track 1B: Swiss Voices — Core Task Intelligence**

How much does domain adaptation (continued pretraining + supervised fine-tuning) change the factual accuracy of
Apertus-8B on specialised questions about **Swiss federal private insurance law**, in German and French, when both
the baseline and the adapted model have the same live web-search tool?

## Status

| Deliverable | State |
|---|---|
| Adapted model weights | public: [legmlai/apertus-8b-swiss-insurance](https://huggingface.co/legmlai/apertus-8b-swiss-insurance); all four safetensors shard URLs checked |
| Evaluation dataset: 300 held-out questions (150 DE / 150 FR) | published: [legmlai/swiss-insurance-eval](https://huggingface.co/datasets/legmlai/swiss-insurance-eval) |
| Model responses, baseline vs adapted, both with live search | generation running on 2026-10-16; pushed to [legmlai/swiss-insurance-eval-responses](https://huggingface.co/datasets/legmlai/swiss-insurance-eval-responses) as they complete |
| Training-data samples (format only) | [swiss-insurance-sft-sample](https://huggingface.co/datasets/legmlai/swiss-insurance-sft-sample), [swiss-insurance-pt-sample](https://huggingface.co/datasets/legmlai/swiss-insurance-pt-sample) |
| Evaluation harness (`make run`, Docker) | implemented: `track_1b/src/evaluate.py`, see below |
| LLM-judge grading + 20 % human audit | pending, runs after the responses are complete |
| Technical report PDF | draft in `track_1b/technical_report.md`; PDF pending results |

The team reports preliminary correct-answer rates of **95% for the adapted model versus 25% for vanilla instruct**.
These figures were supplied by Mohamad Alhajar on 16 October 2026 and have not been independently reproduced.
They are recorded in `track_1b/results/team_reported_preliminary.json`, separately from measured harness outputs.
No complete scored response file or human-audit result is claimed.

The five project Hugging Face repositories are public. See [verified resource links](track_1b/docs/HF_LINKS.md) for checked revisions and file availability. The responses repository still contains its card only at the checked revision; the public evaluation questions contain reference hashes, not reference answers.

## Demo video

[Watch the leGML Hack Apertus demo](https://drive.google.com/file/d/1M0_HGipQ7kq1pfYyo4aU-OVESDTRK8ht/view?usp=sharing).

## The two systems

| | Baseline | Adapted (ours) |
|---|---|---|
| Weights | `swiss-ai/Apertus-8B-Instruct-2509` | `swiss-ai/Apertus-8B-2509` → continued pretraining, 2 epochs, ~44k Swiss insurance segments (DE/FR) + general French → SFT, 2 epochs, ~18k search-and-cite conversations + general French |
| Prompt | identical: Apertus instruct chat template, pinned system date, one tool `web_search(query)` | identical |
| Search | Anthropic Claude Haiku web search, top-10 results (url, title, age) returned to the model | identical |
| Decoding | greedy, bf16, 2048 new tokens per segment, 8192 per question, ≤ 6 tool rounds | identical |

Everything except the weights is held fixed, so the measured difference is the effect of the adaptation, not of
retrieval, tools or prompts.

## Repository layout

```
track_1b/
  README.md               official challenge requirements (unchanged)
  Makefile                make run / make verify (Docker)
  Dockerfile, requirements.txt
  .env.example            LLM_NAME, LLM_BASE_URL, LLM_API_KEY for the judge
  src/evaluate.py         harness: load datasets, judge, score, verify
  results/                judgements.jsonl, results.json, results.md (committed once graded)
  technical_report.md     report source; leGML_Report.pdf once final
  docs/                   submission checklist, evaluation plan, dataset-card notes
Makefile                  delegates to track_1b/
```

## Reproduction

```bash
make run          # from the project root; builds the image and runs the harness
```

- **Without credentials**: re-scores the committed `track_1b/results/judgements.jsonl`, writes
  `results.recomputed.{json,md}` and verifies them against the committed `results.json`. Deterministic, no GPU, no
  API. This is the check judges need.
- **With credentials** (`track_1b/.env`, see `.env.example`: any OpenAI-compatible chat endpoint): additionally
  judges every response that has no cached judgement, using the SimpleQA rubric
  (`CORRECT` / `INCORRECT` / `NOT_ATTEMPTED`) in `src/evaluate.py`.
- `make verify` runs the offline check only.

Requirements: Docker; Python 3.12 inside the image; network access to Hugging Face for the datasets. Generating
model responses (not part of `make run`) needs one 80 GB+ GPU and the search backend; the generation code and
settings are documented in the dataset cards.

## Licensing

Code: **Apache-2.0**. Documentation: **CC-BY-4.0**. Datasets: **CDLA-Permissive-2.0**, with source-level rights
documented in the dataset cards. Model weights and the full training corpora are not part of this repository.

## Links

- Official challenge requirements: `track_1b/README.md`
- Submissions: https://hackapertus.ch/online-hack/submissions
- Organiser dataset template: https://huggingface.co/datasets/HackApertus/online_hack_template
