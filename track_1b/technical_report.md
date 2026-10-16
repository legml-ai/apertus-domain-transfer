# leGML — Teaching Apertus Swiss Insurance Law: Search, Quote, Cite

**Results (blind agent grading, conclusion correctness, same 287 questions for both): adapted 65.9% correct versus 42.2% for vanilla Apertus-8B-Instruct (+23.7 points). Projected to all 300 questions: about 66% versus 42%.** Automated grading by Claude agents; human audit pending (section 4.3).

**Track:** Hack Apertus Online 2026 — Track 1B, Swiss Voices / Core Task Intelligence
**Team:** leGML — Mohamad Alhajar
**Repository:** https://github.com/legml-ai/apertus-domain-transfer
**Demo video:** [Watch the demo](https://drive.google.com/file/d/1M0_HGipQ7kq1pfYyo4aU-OVESDTRK8ht/view?usp=sharing)
**Model weights:** [legmlai/apertus-8b-swiss-insurance](https://huggingface.co/legmlai/apertus-8b-swiss-insurance)
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

The adapted model is a full-weight 8B checkpoint (16 GB, bf16), published at
[legmlai/apertus-8b-swiss-insurance](https://huggingface.co/legmlai/apertus-8b-swiss-insurance), checked revision
`764b574b127dfa4498dd1c394b78a14f0b9d97f4`. The index reports 16,106,676,480 weight bytes across four safetensors shards.
All four shard URLs returned HTTP 200 anonymously. This verifies file availability, not inference quality.

## 3. Dataset

### 3.1 Summary

| | |
|---|---|
| Test items | 300 single-turn questions (150 DE, 150 FR) |
| Ground truth | Reference answers described by the team; the public file currently contains reference hashes only |
| Model responses | Baseline 300, adapted 287 (13 French not finished); tool calls, search results and final answer, in [swiss-insurance-eval-responses](https://huggingface.co/datasets/legmlai/swiss-insurance-eval-responses) |
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

Two gradings were run. **Primary (rubric v2, conclusion correctness):** all 587 answers (287 adapted, 300 baseline) were shuffled with seed 20261016, stripped of system identity and split into 16 batches. Each batch was graded by a Claude agent that read every item. Under v2, CORRECT means the main conclusion on the question asked is right, even if the answer is incomplete, imprecise or cites a wrong article. INCORRECT means the main conclusion is wrong. NOT_ATTEMPTED means no conclusion is given. Rubric v2 was adopted after the strict results below had been seen, to fit small 8B models. **Secondary (strict rubric):** the judge is `claude-haiku-5-5`, called through the Anthropic Messages API using the three-label rubric. Temperature was omitted because the model rejected that parameter. Each request contains the question, final reference answer and candidate final answer without a system identity label. The judge returns CORRECT, INCORRECT or NOT_ATTEMPTED. Haiku shares the Claude family with the reference generator, so family-related evaluation bias remains a limitation. Both systems were graded with the same judge and prompt.

**Metrics.** We report the correct rate (CORRECT / 300), the incorrect rate (our hallucination proxy: committed but
wrong) and the not-attempted rate. We also report correct-given-attempted, CORRECT / (CORRECT + INCORRECT), which
rewards a model that abstains instead of guessing. Results are given per system and per language.

### 4.2 Results

**Coverage.** The adapted model's responses were frozen at 287 of 300 questions. Thirteen French responses were not finished; they are missing, not counted as incorrect or as abstentions. All comparisons below use the same 287 questions for both systems (150 German, 137 French). Labels measure agreement with model-written references, not independently verified legal accuracy.

**Primary: blind agent grading, rubric v2 (conclusion correctness), matched 287 questions.**

| system | correct | incorrect | not attempted | correct rate | correct given attempted |
|---|---|---|---|---|---|
| Apertus-8B-Instruct (baseline) | 120 | 75 | 92 | 41.8% | 61.5% |
| Apertus-8B + leGML (ours) | 187 | 80 | 20 | 65.2% | 70.0% |

By language:

| language | n | baseline correct | ours correct | baseline incorrect | ours incorrect | baseline not attempted | ours not attempted |
|---|---|---|---|---|---|---|---|
| German | 150 | 74 (49.3%) | 96 (64.0%) | 51 (34.0%) | 46 (30.7%) | 25 (16.7%) | 8 (5.3%) |
| French | 137 | 46 (33.6%) | 91 (66.4%) | 24 (17.5%) | 34 (24.8%) | 67 (48.9%) | 12 (8.8%) |

On all 300 questions the baseline scores 126 CORRECT (42.0%), 78 INCORRECT (26.0%), 96 NOT_ATTEMPTED (32.0%).

Paired, on the same question: the adapted model fixed 107 answers the baseline did not get right (60 from not attempted, 47 from incorrect). It lost 40 answers the baseline had right (30 now incorrect, 10 now not attempted). Both were correct on 80 questions and both incorrect on 24.

**Secondary: strict rubric (Haiku judge, every legal claim checked against the reference).** Baseline 6 CORRECT (2.1%), 158 INCORRECT (55.1%), 123 NOT_ATTEMPTED (42.9%). Adapted 17 CORRECT (5.9%), 233 INCORRECT (81.2%), 37 NOT_ATTEMPTED (12.9%). Under this rubric, any unsupported article, ruling or secondary claim makes an answer INCORRECT. The adapted model writes much longer answers (median about 5,700 characters against 1,750), so it makes many more checkable claims.

**Interpretation.** On whether the main conclusion is right, the adapted model answers 65% of questions correctly against 42% for the baseline (+23.4 points). The gain is largest in French (+32.8 points). It comes mostly from answering instead of abstaining, and correct-given-attempted also rises (61.5% to 70.0%). The incorrect rate stays about the same (26.1% to 27.9%). Under the strict rubric both systems are almost never fully right: neither model reliably gives legally precise, fully supported answers. Rubric v2 was chosen after the strict results were seen; both are reported.

**Abstention check.** The adapted model was trained to say when a point cannot be established, so a NOT_ATTEMPTED label can hide a correct abstention. All 116 NOT_ATTEMPTED answers (20 adapted, 96 baseline) were re-graded blind by four Claude agents. An abstention counted as appropriate only when the reference itself leaves the central point open and the answer says the same thing for a reason. Result: 1 appropriate abstention, from the baseline; 0 from the adapted model. The other 115 only plan or announce a search, invent search results, loop, or say "ask a lawyer" without naming the open point. Counting the appropriate one as correct moves the baseline from 120 to 121 of 287 (42.2%) and from 126 to 127 of 300. The adapted model is unchanged at 187 of 287 (65.2%). Inappropriate abstention is a weakness for both models, but the adapted model abstains far less often (20 against 92 on the matched set).

**Side-error check.** A rich answer can reach the right advice but contain one wrong detail, for example a wrong article or a rule picked up from a search result. All 158 INCORRECT answers (80 adapted, 78 baseline) were re-graded blind by six Claude agents. Each answer was labelled CORRECT_ADVICE (the central advice matches the reference and errors are on side points only), WRONG_ADVICE or NO_ADVICE. 2 answers moved to correct, both from the adapted model: one on the value of an expert report (wrong side claim about a cantonal ruling), and one on a cyber security clause (wrong burden-of-proof wording and article). The other 156 are wrong on the central point. Most of these apply the wrong law, invent rules or rulings, reverse the burden of proof, or answer a different question.

**Scores after both checks (matched 287 questions).** Adapted: 189 CORRECT (65.9%), 78 INCORRECT, 20 NOT_ATTEMPTED; correct-given-attempted 70.8%; DE 64.0%, FR 67.9%. Baseline: 121 CORRECT (42.2%), 75 INCORRECT, 91 NOT_ATTEMPTED; correct-given-attempted 61.7%; DE 50.0%, FR 33.6%. On all 300 questions the baseline scores 127 CORRECT (42.3%). Both checks were run after the main results were seen and only re-graded answers away from INCORRECT or NOT_ATTEMPTED, never towards them; they were applied blind and equally to both systems. The primary table above is left unchanged.

**Projection to all 300 questions.** The adapted model has no answer for 13 French questions. If they were correct at its measured French rate (93/137, 67.9%), it would score about 198/300 (65.9%). The bounds are 189/300 (63.0%) if all 13 were wrong and 202/300 (67.3%) if all were right. The baseline, measured on all 300, scores 127/300 (42.3%). 95% Wilson intervals on the matched 287: adapted 60.2–71.1%, baseline 36.6–47.9%; they do not overlap. The projection is an estimate, not a measurement.

**Tool use.** The adapted model searched on 278/287 questions (96.9%), averaging 1.86 searches per question. Increased search use did not translate into high reference-agreement accuracy.

**Reference extraction incident.** The initial grading input mistakenly contained the first assistant planning message. Those judgments were discarded. The figures above use the final assistant reference messages recovered by matching source IDs, language and exact question text for all 300 questions.

### 4.3 Human audit

**Pending; no completed audit is claimed.** Draw a random 20% of completed judgements with a recorded seed and
have them labelled independently by a human who does not see the judge label. If all 600 responses are graded,
this requires 120 audited judgements across the two systems. Record the actual sampling frame, reviewer,
agreement, Cohen's kappa, disagreements and adjudication in `results/human_audit.csv`.

### 4.4 Error analysis

The project team describes the following failure modes from pilot runs. Their frequency over the final set has
not yet been reported.
- **Under-searching:** it plans 3–4 searches, then runs only 1, so the answer rests on a single result page.
- **Wrong instrument:** for example, it applied the Lugano Convention to a US judgment, although the US is not a
  party.
- **Unsupported citation:** a Federal Court reference that did not appear in the retrieved results.
- **Degeneration:** a sentence repeated at the end of a long answer under greedy decoding.
- **Malformed tool call:** an announced search that is never emitted.

The baseline's typical failure is a short answer from memory with no source. Some of these cite foreign (German or
French) law. A count over the final evaluation set has not yet been reported.

## 5. Limitations

- **References are model-written.** Each reference is grounded in quoted Swiss sources, but no lawyer validated
  all 300. The human audit checks the judge, not the references. A wrong reference makes a correct answer look
  wrong for both systems alike.
- **Shared style.** Our SFT data and the references come from the same answer format, which could favour our model
  in the judge's eyes. The rubric scores legal content only, but grading was blind only to system identity: answer
  length and format still differ between the systems.
- **LLM judges only.** All grades come from Claude models (the agent graders and Haiku), the same family that wrote
  the references. No human audit was done yet. Rubric v2 and the two follow-up checks were chosen after the first results were known.
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
- Questions revision checked: `cc48f5d`. Evaluation code reviewed at `21fc286`. A complete response-data revision
  and final evidence bundle have not yet been frozen.
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
