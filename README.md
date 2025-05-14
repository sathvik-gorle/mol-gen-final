# How Gene Expression Changes caused by Black Carbon materials affect PCB Degradation | Molecular Genetics Final Project

## Abstract
Cleaning up PCB‑contaminated soil usually means mixing in some kind of black carbon. That carbon soaks up the pollutant, but it also gives Paraburkholderia xenovorans LB400, a bacterium that can  digest PCBs, a place to live. This analysis investigates whether the kind of black‑carbon surface matters at the gene‑expression level. Using the public RNA‑seq dataset GSE246487, I compared LB400 cells that were floating freely with cells attached to 3 things: 1. small corn‑kernel biochar, (2: large corn‑kernel biochar, and 3: granular activated carbon (GAC). Out of about nine‑thousand genes, 744 flipped just from surface attachment and nearly 2000 flipped when the GAC was swapped for the finer corn biochar. PCB‑breaking genes (bphA1–4) always went up, but only the biochars cranked up CO₂‑fixing genes (cbbL/S, RuBisCO). Overall, corn biochar doesn’t just hold onto PCBs, but it flips LB400 into a gene program that breaks them down faster than GAC can.

## Background
Biochar is a carbon‑rich solid formed when biomass is pyrolyzed under low oxygen. It act as both a physical habitat and an electron shuttling surface, influencing microbial activity and also pollutant degradation gene expression. Current lab work shows that biochar promotes distinct microbial populations that accelerate PCB degradation. Paraburkholderia xenovorans LB400 is the model PCB degrader as its biphenyl pathway begins with the bphA gene cluster, which encodes biphenyl dioxygenase. (MPDI, 2024) Recent work demonstrates that corn‑kernel biochar increases surface‑attached LB400 cell density and raises bphA transcript abundance relative to either planktonic culture or granular activated carbon. (Lui & Zhang, 2025) Moreover, the adjustment of pyrolysis temperature modifies pore volume and oxygen‑containing functional groups, which in turn shifts expression of oxidative‑stress and transport genes in soil. These studies suggest that biochar properties such as pore size distribution, surface area, and residual redox‑active sites can modulate microbial gene expression and ultimately determine pollutant removal efficiency. (Dong).

## Method
| Step                        | Approach                                                                                                                                                                                                                                      |         |      |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- | ---- |
| **Data source**             | GEO accession **GSE246487** (4 contrasts, 12 libraries)                                                                                                                                                                                       |         |      |
| **Pre‑processing**          | Raw counts → DESeq2 (in original study); downloaded **DESeq2 result file (4 tabs)**                                                                                                                                                           |         |      |
| **Significance cut‑offs**   | *adjusted p* < 0.05 and                                                                                                                                                                                                                       | log₂ FC |  > 1 |
| **Python workflow (Colab)** | `pandas`, `seaborn`, `matplotlib`, `scipy`, `sklearn` *(code supplied)*                                                                                                                                                                       |         |      |
| **Visualisations**          | <br>• Bar chart of DEG counts<br>• Volcano plots per contrast<br>• Spearman ρ heat‑map of log₂ FC vectors<br>• “UpSet‑like” bar chart for DEG‑overlap patterns<br>• PCA of contrasts (scaled log₂ FC)<br>• Heat‑map of 20 most‑variable genes |         |      |


## Citations
MDPI. (2024, October 31). Biochar Composite with Enhanced Performance Prepared Through Microbial . https://www.mdpi.com/1422-0067/25/21/11732

Liu, Z. & Zhang, Y. 2025. Journal of Biochar Science. DOI: 10.1007/s42773‑025‑00452‑4 https://link.springer.com/article/10.1007/s42773-025-00452-4

Springer. (2025, March 18). Interactions between microbial extracellular polymeric substances and . https://link.springer.com/article/10.1007/s42773-025-00452-4

Dong, Q. et al. 2024. Environmental Science & Technology. PMID: 38840421 https://pubmed.ncbi.nlm.nih.gov/38840421/
