# Technical report — `project name`

> Three sentence summary: The use case, your dataset, and your key evaluation results.

**Track:** Apertus Readiness  - Track 1B  
**Event:** Online  
**Team:** `team name` — `member`, `member`, `member`  
**Demo:** `link to video, deployment, or notebook`  

----

### Use of Apertus

- **Model:** `e.g. swiss-ai/Apertus-v1.5-70B`
- **How it is used:** inference | fine-tuning | evaluation | red-teaming
- **Where it runs:** `local weights, hosted endpoint, ...`

----
## Use Case Description

Why the dataset was collected, the use case that it evaluates and why this use case matters.

## Dataset Summary

Clear specifications for the dataset. Description of what makes it representative for the use case. Descriptive statistics of the dataset across variables of interest.

## Data Collection Method

Motivation of design choices. Description of the data collection, curation and cleaning methods, the annotation method for ground truth labels and if relevant, instructions provided to annotators for creating the ground truth and annotating LLM responses.

If data was collected from human subjects or contains sensitive or personally identifiable information, the method for obtaining consent must be clearly described.

## Dataset Details

All relevant details related to dataset quality, ethics, licensing and legal considerations. 

## Evaluation

### Method
Evaluation method clearly described.

### Evaluation setup and inference parameters
Setup instructions and parameters for reproducing evaluation results clearly described.

### Results
Evaluation results clearly presented.

## Dataset Limitations

## Lessons Learnt and Recommendations

How you would improve the dataset. What insights the dataset presents on how the model can be improved for your use case.

## Reproducibility

What a judge needs to get your numbers back: hardware, runtime, seeds, and the exact commit. `make run` should do the rest.

## License

Creative Commons Attribution 4.0 (CC-BY-4.0). All HackApertus projects are open-sourced.

## References
