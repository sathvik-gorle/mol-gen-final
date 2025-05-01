import pandas as pd

df = pd.read_excel("GSE246487_DESeq2_results_4_tabs (4).xlsx", sheet_name="attached vs suspended")

df.columns = df.columns.str.strip()
df["log2(FC)"] = pd.to_numeric(df["log2(FC)"], errors="coerce")

top_genes = df.sort_values("log2(FC)", ascending=False).head(10)
print(top_genes[["GeneID", "log2(FC)"]])
