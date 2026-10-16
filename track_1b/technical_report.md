# leGML — Apertus Domain Knowledge Transfer

> DRAFT — results and evidence pending. We investigate domain adaptation of Apertus for specialised Swiss knowledge. The proposed initial domain is Swiss federal private insurance law in French and German. No dataset size, performance gain or completed human review is claimed by this scaffold.

**Track:** Apertus Readiness — Track 1B, Swiss Voices / Core Task Intelligence
**Event:** Online
**Team:** leGML — Mohamad Alhajar; confirm additional members
**Repository:** https://github.com/legml-ai/apertus-domain-transfer
**Dataset:** TODO — public Hugging Face URL and revision
**Demo / notebook:** TODO if available
**Final PDF:** `leGML_Report.pdf`, at most six pages excluding references

----

### Use of Apertus

- **Baseline model and exact revision:** TODO.
- **Adapted model/adapter and exact revision:** TODO.
- **Adaptation method and training configuration:** TODO.
- **Serving stack, inference settings and hardware:** TODO.
- **Supporting open-weight models and their roles:** TODO.

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
