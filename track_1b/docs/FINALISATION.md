# Submission handover — Track 1B / Core Task Intelligence

Prepared 16 October 2026. This is a status snapshot, not a completed submission.

## Form

https://hackapertus.ch/online-hack/submissions

- Track: **Track 1B - Core Task Intelligence**.
- Team: **leGML**. Confirm the full list of participating team members.
- Project: **Teaching Apertus Swiss Insurance Law: Search, Quote, Cite**.
- GitHub: https://github.com/legml-ai/apertus-domain-transfer
- Hugging Face: https://huggingface.co/datasets/legmlai/swiss-insurance-eval
- Include the responses link in the optional message: https://huggingface.co/datasets/legmlai/swiss-insurance-eval-responses
- Final attachment: `leGML_Report.pdf`, maximum six pages excluding references.
- No demo video field is required on the Track 1B Core Task Intelligence form.
- To include an optional video, paste a watchable URL in **Your message (optional)**. Verify that judges can open it without requesting access; the same URL can be added to the report.
- Demo video: https://drive.google.com/file/d/1M0_HGipQ7kq1pfYyo4aU-OVESDTRK8ht/view?usp=sharing
- Use the original Devpost registration email. Participant contact details are kept out of this public repository.

## Resolve before the final click

1. **Model version:** the form only lists 8B v1.5 / 70B v1.5 / both v1.5. Current report and dataset metadata describe Apertus 2509. Do not label 2509 as v1.5. Obtain organiser clarification or use the supported version and report the actual run.
2. **References:** the public questions revision `cc48f5da8715bd0257b988e8497667dc37bc6b81` has 300 questions (150 DE / 150 FR), but only hashes of withheld references. It contains no public answer variants or reference answers. Include accessible ground truth, variants and source citations for the judges in the organiser's required format. The current grading code expects a `reference` field.
3. **Responses:** at checked revision `c1f1c71041c62371b6a93c46dd7eb1e73b234ad9`, the public responses repository contains a card only. Upload and verify actual response files before claiming complete evaluation.
4. **Judgements and human review:** add actual scored outputs and real human labels, then report agreement. For 600 scored responses, 20% is 120 judgements, not 60 across both systems. Define the audit sampling frame explicitly.
5. **Report:** replace every `{{PLACEHOLDER}}`, confirm factual claims against run artifacts, and remove statements describing pending reviews as already completed. Confirm licences and publication rights rather than inferring them from public accessibility.
6. **Reproduction:** verify `make run` from a clean checkout with the final dataset and committed results. Report the generation workflow separately from cached-response scoring. The provided Makefile requires Docker.
7. **Team and student status:** confirm additional members and the Swiss-student-team selection.

## Report PDF

The added report builder creates a clearly marked draft by default. It does not generate results or call any model APIs.

```bash
python -m pip install reportlab pypdf
cd track_1b
python tools/build_report.py --output /path/to/leGML_Report_DRAFT.pdf
# After results and review are complete:
python tools/build_report.py --final --output leGML_Report.pdf
```

The final-mode check rejects unresolved placeholders or draft markers and rejects a PDF over six pages. It is not a substitute for verifying results, references, human review, version eligibility or licences.

The form has been prepared without accepting the terms or clicking Submit. Browser fields may be lost on reload; use this handover to restore project fields.

Published deadline: **16 October 2026 at 12:00 CEST (Paris/Zurich), no extensions**.
