# -*- coding: utf-8 -*-
"""
TCC2 - Regeração de 5 figuras com FONTES MAIORES
(sem alterar conteúdo / valores / layout-base).

Figuras (na mesma ordem em que o usuário pediu):
  1. Arquitetura Experimental — Pipeline de Avaliação  (FIG 6)
  2. Processo de Avaliação Humana                       (FIG 7)
  3. Boxplots Likert por dimensão                       (FIG 5)
  4. Barras Comparativas (Humana + Automática)          (FIG 2)
  5. Dispersão Humano x Automático por persona          (FIG 4)

Saída: ./figuras_formatadas_fonte/
"""

import os
import warnings
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------
BASE = r"C:\Users\t-ddasilva\FilesPersonal\Trabalho de Conclusão de Curso"
OUT_DIR = os.path.join(BASE, "figuras_formatadas_fonte")
DATA_DIR = os.path.join(BASE, "tcc_coding_files")
os.makedirs(OUT_DIR, exist_ok=True)

# ------------------------------------------------------------
# Estilo global — fontes maiores
# ------------------------------------------------------------
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 15,
    "axes.titlesize": 19,
    "axes.labelsize": 16,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "legend.fontsize": 14,
    "figure.dpi": 200,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.35,
    "figure.facecolor": "white",
})

# ------------------------------------------------------------
# Paleta + nomes ATUALIZADOS dos modelos
# ------------------------------------------------------------
COLORS = {"GPT-5.5": "#2E86AB", "Gemini 3.1 Pro": "#A23B72", "Llama 4": "#F18F01"}
MODEL_ORDER = ["GPT-5.5", "Gemini 3.1 Pro", "Llama 4"]
MODEL_MAP = {"gpt5": "GPT-5.5", "gemini": "Gemini 3.1 Pro", "llama4": "Llama 4"}

# ------------------------------------------------------------
# Carga de dados (mesma do script original)
# ------------------------------------------------------------
human_df = pd.read_csv(os.path.join(DATA_DIR, "data", "human_scores_consolidated.csv"))
human_df["model_label"] = human_df["model"].map(MODEL_MAP)

auto_metrics = {
    "GPT-5.5":        {"PPL": 118.3, "TQS": 0.544, "WASSA": 3.360, "Stylometric": 0.061},
    "Gemini 3.1 Pro": {"PPL": 179.5, "TQS": 0.513, "WASSA": 3.113, "Stylometric": 0.070},
    "Llama 4":        {"PPL": 229.4, "TQS": 0.582, "WASSA": 3.280, "Stylometric": 0.052},
}

human_means = (
    human_df.groupby("model_label")[
        ["empatia", "consistencia_de_marca", "adequacao_de_tom", "fluencia"]
    ]
    .mean()
    .reindex(MODEL_ORDER)
)

print("Data loaded.")
print(human_means)

# ============================================================
# FIG 1 — Arquitetura Experimental (era FIG 6 do original)
# ============================================================
print("\n--- FIG 1: Arquitetura Experimental ---")

fig, ax = plt.subplots(figsize=(20, 11))
ax.set_xlim(0, 14)
ax.set_ylim(0, 8)
ax.axis("off")

def add_box(ax, x, y, w, h, text,
            color="#E8F4FD", border="#2E86AB", fontsize=13, bold=False,
            pad=0.08):
    box = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad={pad}",
                         facecolor=color, edgecolor=border, linewidth=1.8)
    ax.add_patch(box)
    weight = "bold" if bold else "normal"
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fontsize, fontweight=weight, wrap=True)

def add_arrow(ax, x1, y1, x2, y2, color="#555555"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color=color, lw=2.0))

ax.text(7, 7.7, "Arquitetura Experimental — Pipeline de Avaliação",
        ha="center", va="center", fontsize=22, fontweight="bold")

# Row 1
add_box(ax, 0.3, 6.15, 2.7, 1.05,
        "Coleta de Dados\n200 comentários\nCoco Bambu Manaus\n(100 before + 100 after)",
        color="#FFF3CD", border="#F18F01", fontsize=12, bold=True)
add_arrow(ax, 3.05, 6.70, 3.85, 6.70)

add_box(ax, 3.9, 6.15, 2.7, 1.05,
        "Engenharia de Prompts\n2 Personas × 2 Estratégias\n(Zero-Shot + Few-Shot)",
        color="#D4EDDA", border="#28A745", fontsize=12, bold=True)
add_arrow(ax, 6.65, 6.70, 7.45, 6.70)

add_box(ax, 7.5, 6.15, 2.7, 1.05,
        "Geração de Respostas\n3 LLMs × 8 cenários\n= 24 condições\n× 100 = 2.400 respostas",
        color="#E8F4FD", border="#2E86AB", fontsize=12, bold=True)

# LLM boxes (à direita)
for i, (model, color) in enumerate([("GPT-5.5", "#2E86AB"),
                                    ("Gemini 3.1 Pro", "#A23B72"),
                                    ("Llama 4", "#F18F01")]):
    y_base = 6.95 - i * 0.62
    box = FancyBboxPatch((10.8, y_base), 2.4, 0.5, boxstyle="round,pad=0.10",
                         facecolor=color, edgecolor=color, linewidth=1.5)
    ax.add_patch(box)
    ax.text(10.8 + 1.2, y_base + 0.25, model,
            ha="center", va="center", color="white",
            fontsize=12, fontweight="bold")

add_arrow(ax, 10.2, 6.70, 10.75, 7.20)
add_arrow(ax, 10.2, 6.70, 10.75, 6.58)
add_arrow(ax, 10.2, 6.55, 10.75, 5.96)

# Avaliação
ax.text(7, 5.05, "AVALIAÇÃO", ha="center", va="center",
        fontsize=18, fontweight="bold", color="#333")

# Branch automática
add_arrow(ax, 5.0, 4.95, 5.0, 4.45)
ax.text(5.0, 4.65, "Métricas Automáticas",
        ha="center", va="center", fontsize=14, fontweight="bold", color="#6F42C1")

add_box(ax, 0.15, 3.10, 2.05, 1.10,
        "Fluência\nPerplexidade\n(GPT-2 PT-BR)",
        color="#F0E6FF", border="#6F42C1", fontsize=12, bold=True, pad=0.06)
add_box(ax, 2.50, 3.10, 2.05, 1.10,
        "Adequação de Tom\nToneCal TQS\n(0–1)",
        color="#F0E6FF", border="#6F42C1", fontsize=12, bold=True, pad=0.06)
add_box(ax, 4.85, 3.10, 2.05, 1.10,
        "Consistência\nWriteprints\nStylometric Sim.",
        color="#F0E6FF", border="#6F42C1", fontsize=12, bold=True, pad=0.06)
add_box(ax, 7.20, 3.10, 2.05, 1.10,
        "Empatia\nWASSA\nPerceived Empathy",
        color="#F0E6FF", border="#6F42C1", fontsize=12, bold=True, pad=0.06)

# Branch humana
add_arrow(ax, 11.3, 4.95, 11.3, 4.45)
ax.text(11.3, 4.65, "Avaliação Humana",
        ha="center", va="center", fontsize=14, fontweight="bold", color="#E74C3C")

add_box(ax, 9.65, 3.10, 3.30, 1.10,
        "Avaliação Humana\n15 avaliadores reais\n72 itens × Likert 1–5\n4 dimensões",
        color="#FFDDD2", border="#E74C3C", fontsize=12, bold=True, pad=0.06)

# Análise comparativa
add_arrow(ax, 5.0, 3.10, 6.8, 1.95)
add_arrow(ax, 11.3, 3.10, 7.2, 1.95)
add_box(ax, 4.3, 0.65, 5.4, 1.20,
        "Análise Comparativa\nKruskal-Wallis + Mann-Whitney\nCorrelação Humano × Automático\nFleiss κ + Krippendorff α + ICC",
        color="#FFF3CD", border="#F18F01", fontsize=13, bold=True)

plt.tight_layout()
fig.savefig(os.path.join(OUT_DIR, "01_arquitetura_experimental.png"))
plt.close()
print("  -> 01_arquitetura_experimental.png")

# ============================================================
# FIG 2 — Processo de Avaliação Humana (era FIG 7 do original)
# ============================================================
print("\n--- FIG 2: Processo de Avaliação Humana ---")

fig, ax = plt.subplots(figsize=(17, 10))
ax.set_xlim(0, 12)
ax.set_ylim(0, 7)
ax.axis("off")

ax.text(6, 6.6, "Processo de Avaliação Humana",
        ha="center", fontsize=22, fontweight="bold")

add_box(ax, 0.4, 5.10, 2.7, 1.10,
        "Seleção de Amostra\n72 pares\n(comentário + resposta)\namostragem estratificada",
        color="#E8F4FD", border="#2E86AB", fontsize=12, bold=True, pad=0.08)
add_arrow(ax, 3.15, 5.65, 3.95, 5.65)

add_box(ax, 4.0, 5.10, 2.7, 1.10,
        "Distribuição\nPlanilhas individuais\nOrdem aleatorizada\nCego ao modelo/persona",
        color="#D4EDDA", border="#28A745", fontsize=12, bold=True, pad=0.08)
add_arrow(ax, 6.75, 5.65, 7.55, 5.65)

add_box(ax, 7.6, 5.10, 2.8, 1.10,
        "15 Avaliadores\nHumanos Reais\nEscala Likert 1–5\n4 dimensões",
        color="#FFDDD2", border="#E74C3C", fontsize=12, bold=True, pad=0.08)

# Dimensões (4 boxes na linha de baixo, com mais respiro)
dims_box_y = 3.05
dim_specs = [
    ("Empatia", "A resposta demonstra\ncompreensão emocional?"),
    ("Consistência\nde Marca", "A resposta mantém a\nidentidade do restaurante?"),
    ("Adequação\nde Tom", "O tom é apropriado\nao contexto?"),
    ("Fluência", "O texto é gramaticalmente\ncorreto e natural?"),
]
for i, (dim, desc) in enumerate(dim_specs):
    x_pos = 0.20 + i * 2.95
    add_box(ax, x_pos, dims_box_y, 2.45, 1.30, f"{dim}\n{desc}",
            color="#F0E6FF", border="#6F42C1", fontsize=11.5, bold=False, pad=0.06)
    add_arrow(ax, 9.0, 5.10, x_pos + 1.22, dims_box_y + 1.30)

# Concordância
add_arrow(ax, 6.0, 3.05, 6.0, 2.05)
add_box(ax, 3.10, 0.55, 5.8, 1.30,
        "Concordância Inter-Avaliadores\n"
        "Fleiss κ = 0.76–0.86 (Substancial–Quase Perfeita)\n"
        "Krippendorff α = 0.82–0.94\n"
        "ICC(2,1) = 0.88–0.94",
        color="#FFF3CD", border="#F18F01", fontsize=12, bold=True, pad=0.08)

plt.tight_layout()
fig.savefig(os.path.join(OUT_DIR, "02_processo_avaliacao_humana.png"))
plt.close()
print("  -> 02_processo_avaliacao_humana.png")

# ============================================================
# FIG 3 — Boxplots Likert (era FIG 5 do original)
# ============================================================
print("\n--- FIG 3: Boxplot Likert ---")

fig, axes = plt.subplots(1, 4, figsize=(20, 7), sharey=True)
dims = ["empatia", "consistencia_de_marca", "adequacao_de_tom", "fluencia"]
dim_titles = ["Empatia", "Consistência de Marca", "Adequação de Tom", "Fluência"]

# 72 itens por modelo (média entre avaliadores)
human_item_means = (
    human_df.groupby(["model_label", "unique_id"])[dims].mean().reset_index()
)

for idx, (dim, title) in enumerate(zip(dims, dim_titles)):
    ax = axes[idx]
    box_data = [human_item_means[human_item_means["model_label"] == m][dim].values
                for m in MODEL_ORDER]

    bp = ax.boxplot(
        box_data,
        labels=["GPT-5.5", "Gemini\n3.1 Pro", "Llama 4"],
        patch_artist=True, widths=0.6,
        medianprops=dict(color="black", linewidth=2.4),
        whiskerprops=dict(linewidth=1.6),
        capprops=dict(linewidth=1.6),
        flierprops=dict(marker="o", markersize=6, alpha=0.5),
    )
    for patch, model in zip(bp["boxes"], MODEL_ORDER):
        patch.set_facecolor(COLORS[model])
        patch.set_alpha(0.7)

    ax.set_title(title, fontweight="bold", fontsize=17, pad=12)
    ax.set_ylim(0.5, 5.5)
    ax.axhline(y=3, color="gray", linestyle="--", alpha=0.35, linewidth=1.0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.2)
    ax.tick_params(axis="x", labelsize=14)
    ax.tick_params(axis="y", labelsize=14)

    if idx == 0:
        ax.set_ylabel("Score Likert (1–5)", fontsize=16)

plt.tight_layout()
fig.savefig(os.path.join(OUT_DIR, "03_boxplot_likert.png"))
plt.close()
print("  -> 03_boxplot_likert.png")

# ============================================================
# FIG 4 — Barras Comparativas (era FIG 2 do original)
# ============================================================
print("\n--- FIG 4: Barras Comparativas ---")

from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(24, 9))
gs = GridSpec(1, 5, width_ratios=[3.0, 1.0, 1.0, 1.0, 1.0], wspace=0.55,
              left=0.05, right=0.985, top=0.82, bottom=0.14)

ax_h = fig.add_subplot(gs[0])
ax_ppl = fig.add_subplot(gs[1])
ax_tqs = fig.add_subplot(gs[2])
ax_wassa = fig.add_subplot(gs[3])
ax_stylo = fig.add_subplot(gs[4])

# --- Painel esquerdo: Avaliação Humana
dims_human = ["empatia", "consistencia_de_marca", "adequacao_de_tom", "fluencia"]
labels_human = ["Empatia", "Consistência\nde Marca", "Adequação\nde Tom", "Fluência"]
x = np.arange(len(dims_human))
width = 0.26

for i, model in enumerate(MODEL_ORDER):
    vals = [human_means.loc[model, d] for d in dims_human]
    bars = ax_h.bar(x + i * width, vals, width, label=model,
                    color=COLORS[model], edgecolor="white", linewidth=0.7)
    for bar, val in zip(bars, vals):
        ax_h.text(bar.get_x() + bar.get_width() / 2,
                  bar.get_height() + 0.08,
                  f"{val:.2f}", ha="center", va="bottom",
                  fontsize=12, fontweight="bold")

ax_h.set_xticks(x + width)
ax_h.set_xticklabels(labels_human, fontsize=14)
ax_h.set_ylim(0, 5.7)
ax_h.set_ylabel("Média Likert (1–5)", fontsize=16)
ax_h.legend(fontsize=13, loc="upper left", frameon=True)
ax_h.axhline(y=3, color="gray", linestyle="--", alpha=0.35, linewidth=1.0)
ax_h.spines["top"].set_visible(False)
ax_h.spines["right"].set_visible(False)
ax_h.tick_params(axis="y", labelsize=13)

# --- Painéis direitos: Métricas Automáticas (1 sub-painel por métrica)
def _draw_metric_panel(ax, title, values_dict, fmt, invert=False):
    xs = np.arange(len(MODEL_ORDER))
    vals = [values_dict[m] for m in MODEL_ORDER]
    bars = ax.bar(xs, vals, width=0.65,
                  color=[COLORS[m] for m in MODEL_ORDER],
                  edgecolor="white", linewidth=0.7)
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                fmt.format(val),
                ha="center",
                va="bottom" if not invert else "top",
                fontsize=12, fontweight="bold",
                clip_on=False)
    ax.set_xticks(xs)
    ax.set_xticklabels(["GPT-5.5", "Gemini\n3.1 Pro", "Llama 4"],
                       fontsize=11, rotation=0)
    ax.set_title(title, fontweight="bold", fontsize=14, pad=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis="y", labelsize=11)
    if invert:
        ax.invert_yaxis()

ppl_vals = {m: auto_metrics[m]["PPL"] for m in MODEL_ORDER}
tqs_vals = {m: auto_metrics[m]["TQS"] for m in MODEL_ORDER}
wassa_vals = {m: auto_metrics[m]["WASSA"] for m in MODEL_ORDER}
stylo_vals = {m: auto_metrics[m]["Stylometric"] for m in MODEL_ORDER}

_draw_metric_panel(ax_ppl, "Perplexidade\n(↓ melhor)", ppl_vals, "{:.1f}", invert=True)
ax_ppl.set_ylim(max(ppl_vals.values()) * 1.15, 0)

_draw_metric_panel(ax_tqs, "TQS\n(Tom ↑)", tqs_vals, "{:.3f}")
ax_tqs.set_ylim(0, max(tqs_vals.values()) * 1.18)

_draw_metric_panel(ax_wassa, "WASSA\n(Empatia ↑)", wassa_vals, "{:.3f}")
ax_wassa.set_ylim(0, max(wassa_vals.values()) * 1.18)

_draw_metric_panel(ax_stylo, "Stylometric\n(Consist. ↑)", stylo_vals, "{:.3f}")
ax_stylo.set_ylim(0, max(stylo_vals.values()) * 1.22)

# Cabeçalhos de seção no topo (acima dos titulos individuais dos painéis)
# Centro do painel humano (gs[0]) e centro dos 4 painéis automáticos
bbox_h = ax_h.get_position()
bbox_ppl = ax_ppl.get_position()
bbox_stylo = ax_stylo.get_position()

center_h = (bbox_h.x0 + bbox_h.x1) / 2
center_auto = (bbox_ppl.x0 + bbox_stylo.x1) / 2

fig.text(center_h, 0.94, "Avaliação Humana",
         ha="center", va="center", fontsize=22, fontweight="bold")
fig.text(center_auto, 0.94, "Métricas Automáticas",
         ha="center", va="center", fontsize=22, fontweight="bold")

fig.savefig(os.path.join(OUT_DIR, "04_barras_comparativas.png"))
plt.close()
print("  -> 04_barras_comparativas.png")

# ============================================================
# FIG 5 — Dispersão Humano x Automático (era FIG 4 do original)
# ============================================================
print("\n--- FIG 5: Dispersão Humano x Automático ---")

fig, axes = plt.subplots(2, 2, figsize=(16, 14))

scatter_pairs = [
    ("empatia", "WASSA",
     "Empatia Humana (Likert)", "Empatia Automática (WASSA)", axes[0, 0]),
    ("adequacao_de_tom", "TQS",
     "Adequação de Tom Humana (Likert)", "Adequação de Tom Automática (TQS)", axes[0, 1]),
    ("consistencia_de_marca", "Stylometric",
     "Consistência Humana (Likert)", "Consistência Automática (Stylometric)", axes[1, 0]),
    ("fluencia", "PPL_inv",
     "Fluência Humana (Likert)", "Fluência Automática (1/PPL)", axes[1, 1]),
]

human_grouped = human_df.groupby(["model_label", "persona"]).agg(
    empatia=("empatia", "mean"),
    consistencia_de_marca=("consistencia_de_marca", "mean"),
    adequacao_de_tom=("adequacao_de_tom", "mean"),
    fluencia=("fluencia", "mean"),
).reset_index()

auto_persona = {
    ("GPT-5.5", "persona_1"):        {"WASSA": 3.38, "TQS": 0.567, "Stylometric": 0.063, "PPL_inv": 1 / 109.1},
    ("GPT-5.5", "persona_2"):        {"WASSA": 3.34, "TQS": 0.521, "Stylometric": 0.059, "PPL_inv": 1 / 127.4},
    ("Gemini 3.1 Pro", "persona_1"): {"WASSA": 3.14, "TQS": 0.538, "Stylometric": 0.072, "PPL_inv": 1 / 150.3},
    ("Gemini 3.1 Pro", "persona_2"): {"WASSA": 3.09, "TQS": 0.489, "Stylometric": 0.068, "PPL_inv": 1 / 208.8},
    ("Llama 4", "persona_1"):        {"WASSA": 3.31, "TQS": 0.608, "Stylometric": 0.054, "PPL_inv": 1 / 196.2},
    ("Llama 4", "persona_2"):        {"WASSA": 3.25, "TQS": 0.556, "Stylometric": 0.050, "PPL_inv": 1 / 262.5},
}

persona_markers = {"persona_1": "s", "persona_2": "o"}
persona_short = {"persona_1": "For", "persona_2": "Inf"}

for h_dim, a_dim, xlabel, ylabel, ax in scatter_pairs:
    for _, row in human_grouped.iterrows():
        model = row["model_label"]
        persona = row["persona"]
        key = (model, persona)
        if key not in auto_persona:
            continue
        h_val = row[h_dim]
        a_val = auto_persona[key][a_dim]
        ax.scatter(h_val, a_val, c=COLORS[model],
                   marker=persona_markers[persona],
                   s=240, edgecolors="black", linewidth=1.1, zorder=5)
        ax.annotate(f"{model.split()[0]} {persona_short[persona]}",
                    (h_val, a_val), fontsize=12,
                    textcoords="offset points", xytext=(8, 8),
                    ha="left", alpha=0.85, fontweight="bold")

    ax.set_xlabel(xlabel, fontsize=15)
    ax.set_ylabel(ylabel, fontsize=15)
    ax.tick_params(axis="x", labelsize=13)
    ax.tick_params(axis="y", labelsize=13)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(alpha=0.22)

# Legenda combinada na parte de baixo
legend_elements = [
    Line2D([0], [0], marker="o", color="w",
           markerfacecolor=COLORS[m], markersize=14, label=m)
    for m in MODEL_ORDER
]
legend_elements += [
    Line2D([0], [0], marker="s", color="w",
           markerfacecolor="gray", markeredgecolor="black",
           markersize=12, label="Formal (P1)"),
    Line2D([0], [0], marker="o", color="w",
           markerfacecolor="gray", markeredgecolor="black",
           markersize=12, label="Informal (P2)"),
]
fig.legend(handles=legend_elements, loc="lower center",
           ncol=5, fontsize=14, bbox_to_anchor=(0.5, -0.01),
           frameon=True)

plt.tight_layout(rect=[0, 0.06, 1, 1])
fig.savefig(os.path.join(OUT_DIR, "05_dispersao_humano_automatico.png"))
plt.close()
print("  -> 05_dispersao_humano_automatico.png")

print("\n========================================")
print("DONE. 5 figuras salvas em:")
print(OUT_DIR)
print("========================================")
