# leGML — Apertus Domain Knowledge Transfer

Hack Apertus Online 2026 · **Track 1B: Swiss Voices — Core Task Intelligence**

Investigating how domain adaptation changes Apertus's factual accuracy on specialised Swiss questions.

**Status: submission scaffold.** The evaluation dataset, model responses, measured results, final report PDF and evaluation runner still need to be added. This is not a completed submission.

## Scope

The proposed initial domain is **Swiss federal private insurance law**, in French and German. Confirm this scope against the actual project artifacts before submission. The intended comparison is baseline Apertus and adapted Apertus answering the same held-out questions.

The report must distinguish fine-tuning gains from changes in retrieval, tools or prompts. Identify any French-law material used for transfer and evaluate jurisdictional leakage. Separate training, development and evaluation data, and freeze the final benchmark before checkpoint selection.

## Submission materials

- Public GitHub repository, generated from the official template.
- Public Hugging Face dataset: evaluation cases, model responses and metadata, using the organiser's dataset template. **URL pending.**
- [`track_1b/technical_report.md`](track_1b/technical_report.md), to be exported as `track_1b/leGML_Report.pdf`: maximum six pages excluding references.
- End-to-end Docker evaluation launched with `make run`. **Implementation pending.**

Core Task Intelligence requires at least **300 single-turn Q&A pairs with answer variations and source citations**. The organiser's example evaluation uses correct / incorrect / not attempted grading, a random **20% human audit**, and reported judge–human agreement. This is our proposed evaluation plan; no scores or completed review are claimed.

## Repository layout

The official `track_1b/` directory and its original challenge README and Makefile are retained. Other track directories have been removed.

```text
track_1b/
  README.md                 Official challenge requirements
  technical_report.md       leGML report draft
  Makefile                  Evaluation entry point; implementation pending
  .env.example              Required model environment variable names
  src/                      Public evaluation code, to be added
  docs/
    SUBMISSION_CHECKLIST.md
    EVALUATION_PLAN.md
    DATASET_CARD_DRAFT.md
    UPSTREAM.md
Makefile                    Delegates to track_1b/
LICENSE                     Apache-2.0 for code
```

## Reproduction

The official runner currently exits with an error until the evaluation implementation is added. **`make run` is not yet ready for judges.** Both entry points are reserved for the same Docker workflow:

```bash
make run
# or:
cd track_1b && make run
```

Use `LLM_NAME`, `LLM_BASE_URL` and `LLM_API_KEY` for evaluated endpoints. Record the exact model revision, checkpoint/adapter, prompts, inference settings, code commit and dataset revision. Keep credentials, private training data and unapproved client materials out of this repository.

## Links

- [Official challenge requirements](track_1b/README.md)
- [Submission checklist](track_1b/docs/SUBMISSION_CHECKLIST.md)
- [Submission form](https://hackapertus.ch/online-hack/submissions)
- [Official dataset template](https://huggingface.co/datasets/HackApertus/online_hack_template)
- [Organiser's terms](https://hackapertus.ch/terms-and-conditions)

## Licensing

Code: **Apache-2.0**. Original documentation: **CC-BY-4.0**. Submitted datasets must use **CDLA-Permissive-2.0**, with source-level rights and attribution documented. No dataset or model weights are included here. Existing private leGML repositories are not part of this publication.
