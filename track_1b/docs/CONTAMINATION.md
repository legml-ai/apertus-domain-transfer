# Contamination check

Date: 2026-10-16. Evaluation set: 300 questions (150 DE, 150 FR) of `legmlai/swiss-insurance-eval`, with their withheld reference answers.

## 1. Against the Apertus pretraining data (baseline model)

`swiss-ai/Apertus-8B-2509` and `Apertus-8B-Instruct-2509` were released in September 2025 with a fixed training corpus.
All 300 questions and all reference answers were written by our pipeline between 2026-10-14 and 2026-10-15, i.e. after
the Apertus training data was frozen, and were never published before 2026-10-16. They therefore cannot be part of the
Apertus pretraining or post-training data. The underlying *sources* (Fedlex, Federal Court rulings, FINMA) are public
and may well be in the Apertus corpus; that is domain knowledge, not test-set contamination, and is exactly what the
evaluation is meant to measure.

## 2. Against our own training data (adapted model)

The adapted model saw two training sets: the continued-pretraining corpus (43,736 segments) and the SFT set (18,521
conversations). The evaluation questions come from a held-out split made by document hash *before* training
(`int(sha256(url)) % 10000 < 100` for the corpus; a group hash for the SFT data). Checks run on 2026-10-16:

| check | result |
|---|---|
| held-out ids present in the SFT train split | 0 / 300 |
| question text exactly present in any training text (whitespace/case normalised) | 0 / 300 |
| questions sharing at least one 13-word n-gram with training text | 66 / 300 (median shared fraction 0.0%) |
| reference answers sharing at least one 13-word n-gram with training text | 118 / 300 (median shared fraction 0.0%, max 13.2%) |

Index: 74,209,302 distinct 13-grams over 180,595 training segments (SFT conversations without the held-out ids,
plus the full CPT corpus in both languages). Per-item numbers: `contamination_internal.jsonl`.

Manual inspection of the top-overlap items shows that the shared n-grams are the *answer template* that the SFT set
teaches ("**Réflexion initiale** La question porte sur …", "Restent ouverts : le contenu exact des conditions
générales de chaque assureur …", "**Reflexion vor der Recherche** Die Frage verlangt drei Dinge …"), not legal content.
One real effect: some French questions share their opening clause with training questions on the same topic
(e.g. "En Suisse, dans une assurance privée d'indemnités journalières en cas de maladie, comment …", 6 training
questions). These are same-topic siblings, not the same question; the asked situation and the reference differ.

## Limitations

- The n-gram check covers verbatim overlap only; paraphrased training items on the same topic are not detected
  beyond the sibling effect noted above.
- No check against the Claude models used for SFT-data generation and search execution was possible; their training
  data is not public. The judge model is therefore chosen from a different family than the generators.
