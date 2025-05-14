import itertools
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr        # saw example on scipy.org
from sklearn.decomposition import PCA    # followed scikit‑learn quickstart
from sklearn.preprocessing import StandardScaler

from google.colab import files
uploaded = files.upload()


xlsx = Path("GSE246487_DESeq2_results_4_tabs.xlsx")
out_tab = Path("results/tables"); out_tab.mkdir(parents=True, exist_ok=True)
out_fig = Path("results/figs");   out_fig.mkdir(parents=True, exist_ok=True)

# read sheets (Used pandas.read_excel guide for the code)
xlsx = "GSE246487_DESeq2_results_4_tabs.xlsx"
wb, data = pd.ExcelFile(xlsx), {}

for s in wb.sheet_names:
    d = pd.read_excel(xlsx, sheet_name=s).rename(columns=str.strip)
    d["log2FC"] = pd.to_numeric(d.get("log2(FC)", d.get("log2FC")), errors="coerce")
    d["padj"]   = pd.to_numeric(d.get("P-adj",  d.get("padj")),    errors="coerce")
    data[s]     = d[["GeneID", "log2FC", "padj"]].dropna()

deg_rows = []
for n, d in data.items():
    sig = d[(d.padj < 0.05) & (d.log2FC.abs() > 1)]
    deg_rows.append(dict(contrast=n,
                         up=(sig.log2FC > 0).sum(),
                         down=(sig.log2FC < 0).sum(),
                         total=len(sig)))
deg_df = pd.DataFrame(deg_rows)
deg_df.to_csv(out_tab / "DEG_counts_summary.csv", index=False)

plt.figure(figsize=(7,4))
sns.barplot(data=deg_df.melt("contrast", ["up","down"], var_name="dir"),
            x="contrast", y="value", hue="dir",
            palette={"up":"#3b8bba","down":"#ba3b46"})
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(out_fig / "deg_counts_bar.png", dpi=300)
plt.show()

# Volcano Plot from Seaborn documentation
for n, d in data.items():
    plt.figure(figsize=(6,5))
    sns.scatterplot(x="log2FC", y=-np.log10(d.padj), data=d,
                    alpha=.25, edgecolor=None)
    sig = d[(d.padj < 0.05) & (d.log2FC.abs() > 1)]
    sns.scatterplot(x="log2FC", y=-np.log10(sig.padj), data=sig,
                    color="red", alpha=.6, edgecolor=None)
    plt.axhline(-np.log10(0.05), ls="--", c="grey")
    plt.axvline(1, ls="--", c="grey"); plt.axvline(-1, ls="--", c="grey")
    plt.title(n)
    plt.tight_layout()
    plt.savefig(out_fig / f"volcano_{n.replace(' ','_')}.png", dpi=300)
    plt.show()

# Heat map of correlation(From Seaborn heatmap gallery documentation)
contr = list(data)
corr  = pd.DataFrame(index=contr, columns=contr, dtype=float)
for a, b in itertools.combinations(contr, 2):
    xa = data[a].set_index("GeneID").log2FC
    yb = data[b].set_index("GeneID").log2FC
    common = xa.index.intersection(yb.index)
    corr.loc[a,b] = corr.loc[b,a] = spearmanr(xa[common], yb[common]).statistic
np.fill_diagonal(corr.values, 1)
corr.to_csv(out_tab / "spearman_contrast_log2FC.csv")

plt.figure(figsize=(5,4))
sns.heatmap(corr, annot=True, cmap="vlag", vmin=-1, vmax=1)
plt.tight_layout()
plt.savefig(out_fig / "contrast_corr_heatmap.png", dpi=300)
plt.show()

# Overlapping Combinations (idea from a blog post relating to data analysis)
sig_sets = {c:set(d[(d.padj<0.05)&(d.log2FC.abs()>1)].GeneID) for c,d in data.items()}
allg     = sorted(set.union(*sig_sets.values()))
binmat   = pd.DataFrame(0, index=allg, columns=contr)
for c in contr:
    binmat[c] = binmat.index.isin(sig_sets[c]).astype(int)
binmat["n"] = binmat.sum(1)
core = binmat[binmat.n >= 3].index
(out_tab / "core_DEGs.txt").write_text("\n".join(core))

comb = (binmat.groupby(contr).size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
        .head(10))
comb.to_csv(out_tab / "top_overlap_combinations.csv", index=False)

plt.figure(figsize=(6,4))
sns.barplot(x="count",
            y=comb[contr].astype(str).agg("|".join, axis=1),
            data=comb, color="steelblue")
plt.xlabel("genes"); plt.ylabel("overlap pattern")
plt.tight_layout()
plt.savefig(out_fig / "upset_like_overlap.png", dpi=300)
plt.show()

# PCA on contrast signatures (Used sklearn PCA cheat sheet)
wide = pd.concat({c:d.set_index("GeneID").log2FC for c,d in data.items()}, axis=1).dropna()
X    = StandardScaler().fit_transform(wide.T)
coords= PCA(2, random_state=1).fit_transform(X)
pca  = pd.DataFrame(coords, columns=["PC1","PC2"], index=contr)
pca.to_csv(out_tab / "contrasts_pca_coords.csv")

plt.figure(figsize=(4.5,4))
sns.scatterplot(data=pca, x="PC1", y="PC2", s=120)
for lbl,r in pca.iterrows():
    plt.text(r.PC1+.02, r.PC2, lbl, fontsize=8)
plt.axhline(0,c='grey',lw=.5); plt.axvline(0,c='grey',lw=.5)
plt.tight_layout()
plt.savefig(out_fig / "contrasts_pca.png", dpi=300)
plt.show()

# Heat map for the top 20 variables
top20 = wide.var(1).nlargest(20).index
plt.figure(figsize=(6,6))
sns.heatmap(wide.loc[top20], cmap="vlag", center=0, linewidths=.5)
plt.tight_layout()
plt.savefig(out_fig / "top20_heatmap.png", dpi=300)
plt.show()
