<h1 align="center">
MC-LARC
</h1>


<h3 align="center">
  From Generation to Selection: Findings Converting Analogical Problem-Solving into Multiple-Choice Questions
</h3>

<p align="center">
  <a href="https://scholar.google.com/citations?user=J5BIlf8AAAAJ&hl=en"><strong>Donghyeon Shin*</strong></a>
  ·  
  <a href="https://iamseungpil.github.io/"><strong>Seungpil Lee*</strong></a>
  ·
  <a href=""><strong>Klea Lena Kovačec</strong></a>
  ·
  <a href="https://sundong.kim/"><strong>Sundong Kim&dagger;</strong></a>
  <br>
  <b>EMNLP Findings 2024</b>
</p>

<p align="center">
  <a href="https://mc-larc.github.io/"><strong><code>Project Page</code></strong></a>
  <a href="https://aclanthology.org/2024.findings-emnlp.392/"><strong><code>Paper</code></strong></a>
  <a href="https://mc-larc.github.io/download"><strong><code>Dataset</code></strong></a>
</p>

---

This page is the official github repository for "From Generation to Selection: Findings Converting Analogical Problem-Solving into Multiple-Choice Questions".

We introduce various versions of MC-LARC, which is available in [here](https://mc-larc.github.io/download).

If you have any questions about our dataset, please contact us at shindong97411@gmail.com.

# Main Results

- **MC-LARC's Effect**: MC-LARC, a multiple-choice version of ARC, increased LLM accuracy from 10% to 76%, focusing on *"Understand"* and *"Apply"* stages of Bloom's Taxonomy, making it easier to assess low level of reasoning abilities.

- **LLM Shortcuts**: LLMs often used shortcuts, like eliminating options based on repeated expressions or format, rather than actual reasoning, which inflated performance, especially without images.

- **Self-Feedback to Reduce Shortcuts**: A self-feedback framework was introduced, where LLMs refined the options after solving the questions, reducing shortcut use and improving the reliability of the evaluation process.


# Citation
If you find our paper helpful in your research, we would appreciate it if you could consider citing it.

```BibTex
@inproceedings{shin2024from,
  title={From Generation to Selection Findings of Converting Analogical Problem-Solving into Multiple-Choice Questions},
  booktitle={Findings of the Association for Computational Linguistics: EMNLP 2024},
  author={Shin, Donghyeon and Lee, Seungpil and Kovacec, Klea and Kim, Sundong},
  year={2024}
}
```

# Acknowledgement
This work was supported by the IITP (RS-2023-00216011, RS-2024-00445087, No. 2019-0-01842) and the NRF (RS-2024-00451162) grants funded by the Ministry of Science and ICT, Korea. Experiments were supported by the Accelerate Foundation Models Research Initiative, Microsoft.

###### *This work was done @ GIST Data Science Lab*