#!/usr/bin/env python
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

parser = argparse.ArgumentParser()
parser.add_argument("--xlsx", default="GSE246487_DESeq2_results_4_tabs.xlsx")
parser.add_argument("--sheet")                       # process one sheet if given
parser.add_argument("--padj", type=float, default=0.05)
args = parser.parse_args()

xlsx = Path(args.xlsx)
sheets = [args.sheet] if args.sheet else pd.ExcelFile(xlsx).sheet_names
outdir = Path("results/figures")
outdir.mkdir(parents=True, exist_ok=True)

def run(sheet):
    df = pd.read_excel(xlsx, sheet_name=sheet).rename(columns=str.strip)
    df["log2FC"] = pd.to_numeric(df.get("log2(FC)", df.get("log2FC")), errors="coerce")
    df["padj"]   = pd.to_numeric(df.get("P-adj", df.get("padj")),   errors="coerce")

    sig = df[df["padj"] < args.padj]
    top = sig.sort_values("log2FC", ascending=False).head(10)
    bottom = sig.sort_values("log2FC").head(10)

    top.to_csv(outdir / f"{sheet}_top_up.csv", index=False)
    bottom.to_csv(outdir / f"{sheet}_top_down.csv", index=False)

    plt.figure(figsize=(8,5))
    sns.barplot(x="log2FC", y="GeneID", data=top, palette="crest")
    plt.axvline(0, color="grey", lw=0.8)
    plt.title(f"Top 10 Up – {sheet}")
    plt.tight_layout()
    plt.savefig(outdir / f"{sheet}_top_up.png", dpi=300)
    plt.close()

    plt.figure(figsize=(8,5))
    sns.barplot(x="log2FC", y="GeneID", data=bottom, palette="flare")
    plt.axvline(0, color="grey", lw=0.8)
    plt.title(f"Top 10 Down – {sheet}")
    plt.tight_layout()
    plt.savefig(outdir / f"{sheet}_top_down.png", dpi=300)
    plt.close()

    plt.figure(figsize=(6,5))
    sns.scatterplot(x="log2FC", y=-np.log10(df["padj"]), data=df, alpha=0.3, edgecolor=None)
    plt.axhline(-np.log10(args.padj), ls="--", c="grey")
    plt.axvline(1, ls="--", c="grey");  plt.axvline(-1, ls="--", c="grey")
    plt.title(f"Volcano – {sheet}")
    plt.xlabel("log2FC");  plt.ylabel("-log10 padj")
    plt.tight_layout()
    plt.savefig(outdir / f"{sheet}_volcano.png", dpi=300)
    plt.close()

for s in sheets:
    run(s)
