import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. Leitura dos dados originais
caminho_csv = os.path.join("dados", "fornecedores.csv")
df = pd.read_csv(caminho_csv)

# 2. Normalização para escala 1 a 10 (conforme skill decision-matrix)
df_scores = pd.DataFrame()
df_scores["fornecedor"] = df["fornecedor"]
df_scores["score_preco"] = 10 * (df["preco_unitario"].min() / df["preco_unitario"])
df_scores["score_prazo"] = 10 * (df["prazo_dias"].min() / df["prazo_dias"])
df_scores["score_defeitos"] = 10 * (df["defeitos_pct"].min() / df["defeitos_pct"])
df_scores["score_suporte"] = 10 * (df["suporte_nota"] / df["suporte_nota"].max())

# 3. Pesos dos critérios
pesos = {
    "preco": 0.30,
    "defeitos": 0.30,
    "prazo": 0.20,
    "suporte": 0.20
}

# 4. Cálculo da pontuação ponderada final
df_scores["nota_final"] = (
    df_scores["score_preco"] * pesos["preco"] +
    df_scores["score_defeitos"] * pesos["defeitos"] +
    df_scores["score_prazo"] * pesos["prazo"] +
    df_scores["score_suporte"] * pesos["suporte"]
)

# Ordenar por ranking
df_scores = df_scores.sort_values(by="nota_final", ascending=False).reset_index(drop=True)
df_scores["rank"] = df_scores.index + 1
melhor = df_scores.iloc[0]

os.makedirs("resultados", exist_ok=True)

# -------------------------------------------------------------
# GRÁFICO 1 APERFEIÇOADO: Matriz de Decisão e Critérios Individuais
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Subplot 1: Nota Final Ponderada
cores = ["#27ae60" if f == melhor["fornecedor"] else "#2980b9" for f in df_scores["fornecedor"]]
barras = ax1.bar(df_scores["fornecedor"], df_scores["nota_final"], color=cores, width=0.55, edgecolor="#1c2833")
ax1.set_title("Pontuação Final Ponderada (0 a 10)\n[Verde = Vencedor]", fontsize=12, fontweight="bold")
ax1.set_xlabel("Fornecedor", fontsize=10, fontweight="bold")
ax1.set_ylabel("Nota Final", fontsize=10, fontweight="bold")
ax1.set_ylim(0, 11)
ax1.grid(axis="y", linestyle="--", alpha=0.5)

for barra in barras:
    h = barra.get_height()
    ax1.text(barra.get_x() + barra.get_width() / 2, h + 0.2, f"{h:.2f}", ha="center", va="bottom", fontweight="bold", fontsize=10)

# Subplot 2: Notas Individuais por Critério com Rótulos
posicoes = np.arange(len(df_scores["fornecedor"]))
largura = 0.20

b1 = ax2.bar(posicoes - 1.5 * largura, df_scores["score_preco"], width=largura, label="Preço (30%)", color="#d35400")
b2 = ax2.bar(posicoes - 0.5 * largura, df_scores["score_defeitos"], width=largura, label="Defeitos (30%)", color="#c0392b")
b3 = ax2.bar(posicoes + 0.5 * largura, df_scores["score_prazo"], width=largura, label="Prazo (20%)", color="#8e44ad")
b4 = ax2.bar(posicoes + 1.5 * largura, df_scores["score_suporte"], width=largura, label="Suporte (20%)", color="#16a085")

ax2.set_title("Desempenho por Critério Normalizado (1 a 10)", fontsize=12, fontweight="bold")
ax2.set_xlabel("Fornecedor", fontsize=10, fontweight="bold")
ax2.set_ylabel("Nota do Critério", fontsize=10, fontweight="bold")
ax2.set_xticks(posicoes)
ax2.set_xticklabels(df_scores["fornecedor"])
ax2.set_ylim(0, 12)
ax2.grid(axis="y", linestyle="--", alpha=0.5)
ax2.legend(loc="upper right", framealpha=0.9, fontsize=9)

# Nota de rodapé da skill chart-image
fig.text(0.01, 0.01, "Fonte: dados/fornecedores.csv | Metodologia: Decision Matrix (Pesos: Preço 30%, Defeitos 30%, Prazo 20%, Suporte 20%)", fontsize=8, color="#555555")

plt.tight_layout(rect=[0, 0.03, 1, 1])
caminho_grafico1 = os.path.join("resultados", "grafico_fornecedores.png")
plt.savefig(caminho_grafico1, dpi=160)
plt.close()

# -------------------------------------------------------------
# NOVO GRÁFICO 2: Radar Chart (Comparação Multidimensional)
# -------------------------------------------------------------
categorias = ["Preço", "Defeitos", "Prazo", "Suporte"]
N = len(categorias)
angulos = [n / float(N) * 2 * np.pi for n in range(N)]
angulos += angulos[:1]  # Fechar o círculo

fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
paleta = {"Delta": "#27ae60", "Beta": "#2980b9", "Alfa": "#e67e22", "Gama": "#8e44ad"}

for _, row in df_scores.iterrows():
    f = row["fornecedor"]
    valores = [row["score_preco"], row["score_defeitos"], row["score_prazo"], row["score_suporte"]]
    valores += valores[:1]
    estilo = "-" if f == "Delta" else "--"
    largura_linha = 3 if f == "Delta" else 1.8
    ax.plot(angulos, valores, linewidth=largura_linha, linestyle=estilo, label=f"{f} ({row['nota_final']:.2f})", color=paleta[f])
    ax.fill(angulos, valores, color=paleta[f], alpha=0.15 if f == "Delta" else 0.05)

ax.set_xticks(angulos[:-1])
ax.set_xticklabels(categorias, fontsize=11, fontweight="bold")
ax.set_ylim(0, 10.5)
ax.set_yticks([2, 4, 6, 8, 10])
ax.set_yticklabels(["2", "4", "6", "8", "10"], color="#666666", size=8)
ax.set_title("Perfil Comparativo 360° dos Fornecedores (Radar)", fontsize=13, fontweight="bold", pad=20)
ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1), title="Fornecedor (Nota Final)")

fig.text(0.01, 0.01, "Fonte: dados/fornecedores.csv | Escala normalizada de 0 a 10", fontsize=8, color="#555555")
plt.tight_layout()
caminho_radar = os.path.join("resultados", "grafico_radar_fornecedores.png")
plt.savefig(caminho_radar, dpi=160, bbox_inches="tight")
plt.close()

# -------------------------------------------------------------
# NOVO GRÁFICO 3: Trade-off Preço Unitário vs Taxa de Defeitos
# -------------------------------------------------------------
plt.figure(figsize=(9, 6))
df_merged = pd.merge(df, df_scores[["fornecedor", "nota_final", "rank"]], on="fornecedor")

for _, row in df_merged.iterrows():
    cor = "#27ae60" if row["fornecedor"] == "Delta" else "#2980b9"
    # Tamanho do ponto baseado na nota de suporte (ex: 8 -> 80)
    plt.scatter(row["preco_unitario"], row["defeitos_pct"], s=row["suporte_nota"] * 45, color=cor, alpha=0.8, edgecolors="black", linewidth=1.5, zorder=4)
    # Rótulo de cada ponto com fornecedor, prazo e nota final
    plt.annotate(
        f"{row['fornecedor']} (Rank #{int(row['rank'])})\nPrazo: {row['prazo_dias']}d | Sup: {row['suporte_nota']}/10",
        (row["preco_unitario"], row["defeitos_pct"]),
        textcoords="offset points",
        xytext=(10, 10),
        fontsize=9,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#cccccc", alpha=0.9)
    )

plt.title("Trade-off de Negócio: Preço Unitário vs. Taxa de Defeitos", fontsize=13, fontweight="bold")
plt.xlabel("Preço Unitário (R$) - [Menor é Melhor]", fontsize=10, fontweight="bold")
plt.ylabel("Taxa de Defeitos (%) - [Menor é Melhor]", fontsize=10, fontweight="bold")
plt.grid(True, linestyle="--", alpha=0.6)

# Destacar a área ideal (baixo custo e baixo defeito)
plt.axhspan(0, 1.5, xmin=0, xmax=0.5, color="#27ae60", alpha=0.08)
plt.text(86, 0.2, "Quadrante Ideal:\nBaixo Preço & Baixo Defeito", fontsize=9, color="#1e8449", fontstyle="italic")

plt.figtext(0.01, 0.01, "Fonte: dados/fornecedores.csv | Tamanho da bolha indica nota de suporte", fontsize=8, color="#555555")
plt.tight_layout(rect=[0, 0.03, 1, 1])
caminho_tradeoff = os.path.join("resultados", "grafico_tradeoff.png")
plt.savefig(caminho_tradeoff, dpi=160)
plt.close()

print("Sucesso! Gráficos gerados com padrão chart-image:")
print(f"1. {caminho_grafico1}")
print(f"2. {caminho_radar}")
print(f"3. {caminho_tradeoff}")
