# leGML — Apertus Domain Knowledge Transfer

> DRAFT — results and evidence pending. We investigate domain adaptation of Apertus for specialised Swiss knowledge. The proposed initial domain is Swiss federal private insurance law in French and German. No dataset size, performance gain or completed human review is claimed by this scaffold.

**Track:** Apertus Readiness — Track 1B, Swiss Voices / Core Task Intelligence
**Event:** Online
**Team:** leGML — Mohamad Alhajar; confirm additional members
**Repository:** https://github.com/legml-ai/apertus-domain-transfer
**Dataset:** https://huggingface.co/datasets/legmlai/swiss-insurance-eval (questions), https://huggingface.co/datasets/legmlai/swiss-insurance-eval-responses (responses); revision pinned at submission
**Demo / notebook:** TODO if available
**Final PDF:** `leGML_Report.pdf`, at most six pages excluding references

----

### Use of Apertus

- **Baseline model:** `swiss-ai/Apertus-8B-Instruct-2509`, unchanged weights.
- **Adapted model:** `swiss-ai/Apertus-8B-2509` (revision 3162c99) → continued pretraining → SFT; full weights (bf16, 16 GB).
- **Adaptation method:** (1) continued pretraining, 2 epochs, ~44k segments of Swiss insurance text in German and French (Fedlex, Federal Court, FINMA, insurer conditions, specialist press) mixed with general French, 3× H200, DeepSpeed ZeRO-3; (2) supervised fine-tuning, 2 epochs, ~18k conversations in which the assistant plans, calls `web_search`, reads results and answers with quoted sources, mixed with general French conversations, 2× B200.
- **Serving stack, inference settings and hardware:** Hugging Face Transformers, bf16, greedy decoding, 2048 new tokens per segment, 8192 per question, at most 6 tool rounds; one tool `web_search(query)` executed by Anthropic Claude Haiku web search (top-10 url/title/age). Both systems evaluated on one H200 on 2026-10-16 with identical prompt, tool and settings.
- **Supporting models:** Claude (Haiku and Sonnet class) for SFT-data generation and as the search executor; an LLM judge for grading (named in `results/judgements.jsonl`).

----
## Use Case Description

Proposed use case: factual questions about Swiss federal private insurance law, using Swiss French and German terminology. Confirm final scope and exclusions from actual project artifacts. Explain who needs these answers and which baseline failures domain adaptation should address.

## Dataset Summary

**TODO:** actual count (minimum 300 single-turn Q&A pairs), answer variations, source citations, languages, topics, difficulty, answerability and descriptive statistics. Link evaluation cases, model responses and metadata. Separate training data from the frozen evaluation set.

## Data Collection Method

**TODO:** sources, collection dates, sampling, question construction, reference validation, curation, deduplication and annotation guidance. Describe quality checks actually performed.

If data was collected from human subjects or contains sensitive or personally identifiable information, the method for obtaining consent must be clearly described.

## Dataset Details

**TODO:** source-level provenance and licences, redistribution rights, privacy checks, representativeness and contamination checks. Use the organiser's dataset template and document CDLA-Permissive-2.0 licensing.

## Evaluation

### Method
Planned comparison: baseline and adapted Apertus on identical held-out questions, graded correct / incorrect / not attempted against sourced references. Record judge, rubric and any retrieval/tool/prompt differences. Distinguish transferred-knowledge gains from retrieval changes.

**Human validation pending:** audit a random 20% of judgements with real human labels. Report sampling seed, coverage, agreement, disagreements and adjudication.

### Evaluation setup and inference parameters
**TODO:** exact model revisions, prompts, temperature, token limits, tool access, seed, dataset revision and code commit.

### Results
**Not measured in this repository.** Add actual counts and rates for all three grading labels for each system, with per-language/topic breakdowns. Include failed cases and define any hallucination metric and denominator.

## Dataset Limitations

**TODO:** coverage gaps, temporal validity, source ambiguity, jurisdictional leakage, synthetic-data risks, contamination uncertainty and evaluation limitations.

## Lessons Learnt and Recommendations

**TODO after evaluation:** what improved, what did not, adverse effects, and the next experiment justified by the evidence.

## Reproducibility

**Not implemented yet.** Add a public Docker evaluation workflow launched by `make run`. Document hardware, runtime, API/model access, dataset revision, seed and exact commit. Distinguish scoring saved responses from fresh model inference.

## License

Creative Commons Attribution 4.0 (CC-BY-4.0). All HackApertus projects are open-sourced.

## References

- [Official Track 1B challenge](https://github.com/HackApertus/project-template/blob/main/track_1b/README.md)
- [Official dataset template](https://huggingface.co/datasets/HackApertus/online_hack_template)
- [Hack Apertus terms](https://hackapertus.ch/terms-and-conditions)
- TODO: authoritative domain sources and scientific references actually used.
