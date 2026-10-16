# Challenge 1B: Swiss Voices

This track 1 is focused on improving the multimodal Apertus v1.5 8B and 70B models. There are two different paths. Path B focuses on localising Apertus to the languages, dialects, knowledge and values of Switzerland. Submissions can focus either on the 8B or 70B model.

The submission must comply with the [HackApertus T&C](https://hackapertus.ch/terms-and-conditions). For this challenge it is essential that you pay particular attention to the conditions for responsibly sourced datasets.

## 🎯 The Challenge

**Localised alignment to the languages, dialects, knowledge and values of Switzerland**

**👉🏼You can pick one localisation dimension for your submission.**

This challenge accepts submissions that evaluate any of the following dimensions of localising Apertus to specific Swiss contexts: **input adaptation**, domain-specific **core task intelligence**, and **behavioural alignment.** These dimensions are motivated as follows.

### Input adaptation to local speech and dialects

Many speech-native multimodal LLMs struggle with phonetic drift, code-switching, local accents, and unwritten or low-resource dialects. Submissions should measure transcription accuracy and dialect comprehension to evaluate Apertus’s ability to transcribe Swiss voice inputs into written text representations without losing local context. Note that audio input is an experimental feature in Apertus 1.5.

Dialects that belong to the following ISO-639-3 dialect groups are permitted: gsw, wae, roh, lmo, frp. Dialects should be reported with their glottocodes.

### Core task intelligence for domain-specific knowledge

General base models usually struggle with domain-specific knowledge and niche terminology. Submissions should measure factuality and hallucination rates to evaluate whether Apertus possesses factually accurate, domain-tailored knowledge to execute specialised reasoning for localised Swiss contexts (e.g., legal statutes, local medical guidelines, local government administration processes).

### Alignment to localised preferences

Model performance is not only about dialects and facts, but also about cultural nuances, tone, safety boundaries, and local ethics. For every item in the dataset, the "correct" behaviour must trace to a source of normative authority. This could be a codified law or regulation, a documented professional or institutional standard, a measured majority preference (primary data collection or citation), a convention documented in a style guide or reference work. An item whose only warrant is the author's intuition does not present an authoritative source.

Submissions should measure how frequently responses meet end user expectations, to evaluate which regional norms and local regulatory standards Apertus respects by default. 

---

Each localisation approach calls for a different evaluation dataset type and has its own expectations for test items and evaluation metrics. The table below lists minimum dataset expectations for each localisation approach and example evaluation metrics. We expect the winning submissions to present datasets and evaluations that are significantly deeper than the minimum requirements. 

You should describe and motivate your dataset and evaluation design choices in detail in the submission report. 

| Localisation approach | Minimum evaluation dataset expectations | Example evaluation metrics |
|---|---|---|
| **Input Adaptation** | 100 curated audio clips, paired with text transcriptions and translations to a standard written language (e.g. German, French, Italian, Romansh) | Transcription: mean character error rate and word error rate across all audio clips.<br>Translation: BLEU, chrF, COMET. |
| **Core Task Intelligence** | 300 single-turn Q&A pairs with answer variations and source citations | SimpleQA-style three-way grading (correct/incorrect/not attempted) against ground-truth references using LLM-as-a-judge (with a random sample of 20% of judgements evaluated by a human and reported judge–human agreement). |
| **Behavioural Alignment** | 200 scenario prompts with explicit criteria defining acceptable vs. unacceptable answers, and a matched pair of `chosen` vs. `rejected` outputs; must be anchored in a specific use case and user community; expected behaviours should be labelled as contested vs. settled and treated accordingly. | Forced-choice preference accuracy, rubric-scored free generation with LLM-as-a-judge scoring against stated acceptance criteria (with a random sample of 20% of judgements evaluated by a human and reported judge–human agreement). |

---

## 🔧 Resources & Tools

Check our resources & tools page for detailed information:
https://hackapertus.notion.site/resources-tools


| Models           | URL                                      |
|------------------|------------------------------------------|
| Apertus v1.5 8B  | [huggingface.co/swiss-ai/Apertus-v1.5-8B](https://huggingface.co/swiss-ai/Apertus-v1.5-8B)  |
| Apertus v1.5 70B | [huggingface.co/swiss-ai/Apertus-v1.5-70B](https://huggingface.co/swiss-ai/Apertus-v1.5-70B) |

---

## 📦 Submission Requirements & Deliverables

❗️ Submissions are not handled on Devpost but via this URL only:
http://hackapertus.ch/online-hack/submissions

The submission must: 
1. follow the template repo and include all prerequisite files and definitions
2. follow the specified input/output formats
3. run in a Docker container, launched with `make run` from the root of the project
4. run end-to-end when judges try to run it

### Git repo (URL)
- Create your repo from this template (**Use this template**) and work in the `track_1b/` challenge directory. Delete the other track challenge directories.
- Keep `track_1b/` as it is: don't rename it or move its files.
- Set the repo to PUBLIC (Settings --> Collaborators --> Manage Visibility)
- Submit the URL of YOUR Git repo.

### Technical Report (pdf)
- Update [technical_report.md](technical_report.md) in this repository with all the details for your submission.
- Upload a pdf of your technical report to this directory, named as `TeamName_Report.pdf`.
- Format: pdf, max. 6 pages w/o references
- Submit the pdf of the technical report.

### Dataset (URL)
Submitted datasets must comply with our guidelines for responsibly sourced datasets.

- Create a user account on Hugging Face
- Clone our dataset template on Hugging Face: https://huggingface.co/datasets/HackApertus/online_hack_template
- Complete the dataset card with all required information
- Upload your dataset. It should consist of the following components:
    - evaluation dataset (i.e. individual test cases)
    - model response dataset (i.e. the model response to each test case)
    - metadata file (i.e. additional information about each test case; where relevant, this file must contain instance-level licensing information) 
- Make sure your dataset access control is set to PUBLIC
- Provide the URL of _your_ data set

### Reproducibility

You can create a Python notebook that reproduces your evaluation.

Judges will *only* run code for reproducing the submission from the root of the project with the following command:
```bash
make run
```
You should update the [Makefile](Makefile) so that it works for your submission on a clean checkout.

Requirements: `runtime, hardware, API keys, model weights`

---

## ⚖️ Judging Criteria

The following rubric will be used for scoring submissions. The points gained correspond to the scoring level, i.e. 1 scores 1 point. A submission must score at least at Level 1 on categories 1. to 4. to receive any points.

Categories 2. to 4. are weighted. The total score for the team is calculated as the weighted sum across all categories. The maximum score is 100 and the winning team will be the team with the highest score.

| **Category (× weight)** | **Scoring levels** |
|---|---|
| **1. Localisation and use case relevance** | **0:** No use case stated.<br>**1:** Use case clearly stated.<br>**2:** Use case relevance motivated; use case matters.<br>**5:** Dataset specifications clearly defined.<br>**10:** Dataset specifications are well matched to use case. |
| **2. Dataset quality (× 3)** | **0:** Only dataset links shared; dataset includes personally identifiable information.<br>**1:** Minimally viable dataset that follows schema and includes test items, metadata and ground truth / expected responses; basic descriptive statistics.<br>**2:** Quality metrics provided and motivated; ad hoc quality checks were done; dataset is usable but limited / has low diversity.<br>**5:** Full quality control was done to validate the dataset and is documented; dataset includes diverse / interesting examples (e.g. edge cases, adversarial examples).<br>**10:** Dataset presents a major improvement over currently available datasets; previously untested capabilities can be evaluated with this dataset; contamination checks conducted against Apertus training data (if relevant). |
| **3. Dataset documentation (× 2)** | **0:** Data card with placeholders or missing information; dataset not licensed under CDLA-Permissive-2.0 license.<br>**1:** Documentation complete; licenses provided for individual content items; appropriate consent form template provided.<br>**2:** Consent management and AI permissions clearly outlined.<br>**5:** Reproducible dataset construction (e.g. sampling strategy, data cleaning and preprocessing, annotation guidelines).<br>**10:** Exemplary data card providing full provenance on design choices, versioning, data sourcing, metadata labelling, ground truth annotations and compliance. |
| **4. Evaluation reproducibility (× 2)** | **0:** Cannot be reproduced; code or data missing.<br>**1:** Reproducible only with significant manual tweaking.<br>**2:** Scripted workflow exists but is fragile or poorly documented.<br>**5:** Deterministic workflow given fixed model outputs; clear instructions for creating the results file; substantiated grading; correctly implemented scoring functions.<br>**10:** Reusable harness for fully automated, self-contained evaluation; verifies its own outputs against expected results; works from a clean environment and can accept new models. |
| **Report clarity and communication** | **0:** Poorly organized with major gaps or unreadable sections.<br>**1:** Basic structure but difficult to follow.<br>**2:** Clear narrative with minor ambiguities.<br>**5:** Polished writing with well-chosen figures; concise.<br>**10:** Publication-quality document with compelling visualisations and flawless flow. |
| **Code quality** | **1:** Only submission files shared.<br>**2:** Useful shared notebook or package with basic documentation.<br>**5:** Well-documented package, Apache-2.0 licence, basic tests.<br>**10:** Plug-and-play package that can be adopted in the next iteration of the hackathon; excellent docs. |

## Support

### Licensing requirements
Please check our Terms & Conditions (6. What you build is open source):
https://hackapertus.ch/terms-and-conditions

### FAQ
💡 https://hackapertus.ch/faq

### Contact

💬 In case you have questions, join the conversation on Discord. Alternatively, send an email to “hello@hackapertus.ch”.
