import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_excel("GSE246487_DESeq2_results_4_tabs (4).xlsx", sheet_name="attached vs suspended")

df.columns = df.columns.str.strip()
df["log2(FC)"] = pd.to_numeric(df["log2(FC)"], errors="coerce")

top_genes = df.sort_values("log2(FC)", ascending=False).head(10)
print(top_genes[["GeneID", "log2(FC)"]])

# Making all of the columns numeric
df["P-adj"] = pd.to_numeric(df["P-adj"], errors="coerce")
# Sorts all significant genes by log2(Fold Change), and how much the genes changed in expression, whether increase or decrease (top 10 in each way
top_up = sig_df.sort_values("log2(FC)", ascending=False).head(10)
top_down = sig_df.sort_values("log2(FC)").head(10)

# Plots the top and bottom genes that decreased/dropped the most in expression
plt.figure(figsize=(10, 6))
sns.barplot(x="log2(FC)", y="GeneID", data=top_up, palette="crest")
plt.title("Top 10 Upregulated Genes")
plt.xlabel("log2(Fold Change)")
plt.tight_layout()
plt.savefig("top_upregulated_genes_day2.png")
plt.show()

plt.figure(figsize=(10, 6))
sns.barplot(x="log2(FC)", y="GeneID", data=top_down, palette="flare")
plt.title("Top 10 Downregulated Genes")
plt.xlabel("log2(Fold Change)")
plt.tight_layout()
plt.savefig("top_downregulated_genes_day2.png")
plt.show()
