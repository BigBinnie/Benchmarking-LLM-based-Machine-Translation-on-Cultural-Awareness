# Benchmarking Machine Translation with Cultural Awareness

This repository contains data and code for the paper [Benchmarking Machine Translation with Cultural Awareness](https://arxiv.org/abs/2305.14328). If you have any questions, please reach out to the authors at binwei.yao@wisc.edu.

## Overview
*How to Evaluate MT Systems’ **Cultural Awareness**?*

To address this challenge, we propose

1. **CAMT (6,948 parallel sentences)**: a novel parallel corpus for culturally-aware machine translation

2. **CSI-Match and Pragmatic Translation Assessment**: two new evaluation metrics to assess translation quality of cultural nuances, particularly for terms lacking established translations.

3. **Benchmarking both LLM-based MT and NMT systems**: our results indicate that LLMs can effectively incorporate external cultural knowledge, thereby improving the pragmatic translation quality of CSIs.


## CAMT Data
CAMT Corpus includes **6** language pairs, **6,983** CSIs across **18** concept categories from **235** countries. The statisics are as follows:

| **Pair**  | **Sent.** | **CSIs Counts** | **CSIs Types** | **CSI Translations** |
|-----------|-----------|-----------------|----------------|----------------------|
| En-Zh     | 778       | 794             | 601            | 730                  |
| En-Fr     | 2,073     | 2,213           | 2,213          | 1,130                |
| En-Es     | 1,580     | 1,652           | 1,652          | 817                  |
| En-Hi     | 1,086     | 1,127           | 1,127          | 168                  |
| En-Ta     | 677       | 695             | 695            | 118                  |
| En-Te     | 754       | 695             | 695            | 66                   |
| **Total** | 6,948     | 7,176           | 6,983          | 3,029                |


We performed quality checks on the En-Zh dataset and filtered out low-quality data. For the other language pairs, the data was automatically generated using our pipeline.
## Pipeline for data preprocessing
1. **Entity Linking**

We use [SLING](https://github.com/ringgaard/sling) to label the entities which have Wikipedia pages in the source sentence (in English). Please follow the instruction of SLING to [install](https://github.com/ringgaard/sling/blob/master/doc/guide/install.md) and [link the entity](https://github.com/ringgaard/sling/blob/master/doc/guide/wikiflow.md). After parsing the output of SLING, you can get all the entities' QIDs in the sentence.

2. **Culture Category Classification**

We use [drafttopc](https://github.com/wikimedia/drafttopic) to label the categories of these wiki entities. The scripts are as following:

- Categorize the entity

``bash scripts/category_classification.sh``

- Keep the cultural related entities

3. **Cultural Metadata Augmentation**

``bash scripts/metadata_augmentation.sh``

## Citation
If you use any source codes or datasets included in this repository in your work, please cite the corresponding paper. The bibtex are listed below:
```
@inproceedings{yao2024benchmarking,
  title={Benchmarking Machine Translation with Cultural Awareness},
  author={Yao, Binwei and Jiang, Ming and Bobinac, Tara and Yang, Diyi and Hu, Junjie},
  booktitle={Findings of the Association for Computational Linguistics: EMNLP 2024},
  pages={13078--13096},
  year={2024}
}
```