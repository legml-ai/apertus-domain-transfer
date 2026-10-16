# Domain knowledge transfer — proposed evaluation

This is a plan. No experiment, dataset size, human review or performance gain is claimed.

## Question

Does domain adaptation improve Apertus's factual answers in a defined Swiss domain without increasing hallucination or importing rules from another jurisdiction?

The proposed initial use case is Swiss federal private insurance law in French and German. Confirm the final scope from the actual artifacts.

## Dataset

- At least 300 distinct single-turn questions, accepted answer variations and authoritative source citations.
- Document language, topic, jurisdiction, source date/version, answerability and difficulty. Measure language balance and topic counts.
- Freeze evaluation IDs and sources before checkpoint selection. Check for training duplicates and paraphrases; document uncertainty.
- Confirm source-level publication rights. Public accessibility is not proof of redistribution rights.
- Follow the organiser's Hugging Face dataset template for final schemas. This document is not a replacement schema.

## Comparison

Compare baseline Apertus and adapted Apertus on the same held-out questions. Record exact model/checkpoint revisions and inference settings. Identify retrieval/tool/prompt differences and add an ablation if needed before attributing a gain to fine-tuning.

Save actual model responses and run identifiers. Report failed, retried or excluded calls; do not invent missing responses.

## Scoring and human audit

Use correct / incorrect / not attempted labels against sourced reference answers. Document the judge, version, rubric and prompt. Explain the role of any supporting non-Apertus open-weight model.

Report counts and proportions for all three labels, with language/topic breakdowns. Define any hallucination metric and denominator explicitly.

Randomly select 20% of scored judgements for real human review and record the seed. With 300 questions and one system, this is 60 judgements. For multiple systems, define the sampling frame and audit coverage explicitly.

A human reviewer checks questions, references and responses, records independent labels, and reports agreement, disagreements and any adjudication. Automated review cannot be reported as human review.

## Reproduction

Run from a clean checkout using Docker via `make run`. Record hardware, runtime, model/API access, dataset revision, seed and code commit. Clearly distinguish scoring cached responses from generating new responses.
