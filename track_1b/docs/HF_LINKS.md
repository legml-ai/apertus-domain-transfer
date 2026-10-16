# Hugging Face resources — checked 16 October 2026

The checks below used unauthenticated Hugging Face API requests and file requests. They confirm public accessibility and current file contents, not scientific validity, legal rights or model performance. No model inference was run.

## Project model

- **[Apertus-8B Swiss Insurance](https://huggingface.co/legmlai/apertus-8b-swiss-insurance)**
- Public and ungated. The card identifies Track 1B / Swiss Voices / Core Task Intelligence.
- Checked revision: `764b574b127dfa4498dd1c394b78a14f0b9d97f4`.
- Contains model card, configuration, tokenizer, chat template, weight index, four safetensors shards, licence and usage policy.
- All four weight URLs returned HTTP 200 without authentication. Index total weight size: 16,106,676,480 bytes.
- The card identifies the base model as `swiss-ai/Apertus-8B-2509`; this does not resolve the form's v1.5-only selection.

## Project datasets

- **[Evaluation questions](https://huggingface.co/datasets/legmlai/swiss-insurance-eval)** — public, ungated; 300 JSONL records, 150 German / 150 French. Revision `cc48f5da8715bd0257b988e8497667dc37bc6b81`. Fields: `id`, `language`, `question`, `reference_sha256`. **Reference answers and answer variants are not in this file.**
- **[Model responses](https://huggingface.co/datasets/legmlai/swiss-insurance-eval-responses)** — public, ungated; revision `c1f1c71041c62371b6a93c46dd7eb1e73b234ad9`. **Only README and .gitattributes are present.** The named `ours.jsonl` and `vanilla_apertus_8b_instruct.jsonl` files are not yet present at this revision.
- **[SFT sample](https://huggingface.co/datasets/legmlai/swiss-insurance-sft-sample)** — public, ungated; 50 JSONL records, 25 German / 25 French. Revision `8bcaedf51fd1b61d92bd9379f5db19bd6620f8b6`. This is a format sample, not the complete training set.
- **[Pretraining sample](https://huggingface.co/datasets/legmlai/swiss-insurance-pt-sample)** — public, ungated; 50 JSONL records, 25 German / 25 French. Revision `3fb63d0fead3e1a5ef23b434df9973dec5987ac0`. This is a format sample, not the full pretraining corpus.

All four dataset cards declare CDLA-Permissive-2.0. Licence declarations were read, not independently verified against every source item.

## Other linked Hugging Face resources

- [Apertus-8B-2509 base model](https://huggingface.co/swiss-ai/Apertus-8B-2509) — public API accessible, ungated.
- [Apertus-8B-Instruct-2509 baseline](https://huggingface.co/swiss-ai/Apertus-8B-Instruct-2509) — public API accessible, ungated.
- [Organiser's dataset template](https://huggingface.co/datasets/HackApertus/online_hack_template) — public page/API; file access is automatically gated and may require signing in and accepting access conditions.
- [Organiser's Apertus v1.5 8B link](https://huggingface.co/swiss-ai/Apertus-v1.5-8B) and [v1.5 70B link](https://huggingface.co/swiss-ai/Apertus-v1.5-70B) — public pages/API; file access is automatically gated. Existence of these repositories is not evidence that the current 2509 runs used v1.5.

The submission form has one primary dataset URL field. Keep the evaluation dataset there; the model, responses, samples and demo links are listed in **Your message (optional)** and the report.
