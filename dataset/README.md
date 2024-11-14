# Data Download

We introduce various versions of MC-LARC, which is available in [here](https://mc-larc.github.io/download).

# Data Description

We provide the MC-LARC dataset and refined ['LARC_dataset'](refined_larc.csv).

MC-LARC has three versions:
- ['Original'](original_mc_larc.csv) [2]: without constraints and methods.
- ['Constraints'](constraints_mc_larc.csv) [3]: with constraints.
- ['Self-feedback'](self-feedback_mc_larc.csv) [4]: with constraints and the self-feedback method.

If you have any questions about our dataset, please contact us at shindong97411@gmail.com.

<br/> 

---

## Metadata

The metadata provides basic information about refined LARC and MC-LARC.

### 1. refined_larc.csv
This file contains *"input description"* and *"output description"* for the ARC 400 training dataset. </br>

| Field               | Description                                |
|---------------------|--------------------------------------------|
| task_id             | Unique ID number of MC-LARC                |
| task_name           | Unique ID of ARC task                      |
| description_input   | Description of the input for an ARC task   |
| description_output  | Description of the rule for an ARC task    |

This dataset was created based on LARC [1]. </br>
However, the LARC dataset was not directly used; Through the refinement process, the quality was improved. </br>
</br>

---
### 2. MC-LARC csv files
This file includes five options for each *"description_output"* from the ['refined_larc.csv'](refined_larc.csv) [3] file, serving as the correct answer. </br>
The five options are randomly shuffled, and there is only one correct answer. You can find what is the correct answer by checking the last *answer* field. </br>

| Field                         | Description                               |
|-------------------------------|-------------------------------------------|
| task_id                       | Unique ID number of MC-LARC               |
| task_name                     | Unique ID of ARC task                     |
| shuffled_description (1 ~ 5)  | Shuffled description of the MC-LARC       |
| answer                        | Description of the rule for an ARC task   |

</br>

---
### Reference
[1] Acquaviva, Sam, et al. "Communicating natural programs to humans and machines." *Advances in Neural Information Processing Systems 35* (2022): 3731-3743. </br>
[2] Shin, et al. "MC-LARC Dataset for Evaluating the Reasoning Abilities of Large Language Models", *Korea Software Congress* (2023) </br>
[3] Shin, et al. "Regulation Using Large Language Models to Generate Synthetic Data for Evaluating Analogical Ability" *IJCAI Workshop on Analogical Abstraction in Cognition, Perception, and Language* (2024) </br>
[4] Shin and Lee, et al. "From Generation to Selection: Findings of Converting Analogical Problem-Solving into Multiple-Choice Questions", *EMNLP Findings* (2024)