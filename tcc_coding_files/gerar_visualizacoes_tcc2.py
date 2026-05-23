# -*- coding: utf-8 -*-
"""
TCC2 - Geração de Visualizações
Engenharia de Prompts para Respostas de Restaurantes em Português
7 figuras para a monografia
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import pandas as pd
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

# Paths
BASE = r'C:\Users\t-ddasilva\FilesPersonal\Trabalho de Conclusão de Curso'
IMG_DIR = os.path.join(BASE, 'img')
DATA_DIR = os.path.join(BASE, 'tcc_coding_files')
os.makedirs(IMG_DIR, exist_ok=True)

# Style
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.labelsize': 12,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'figure.facecolor': 'white',
})

# Color palette
COLORS = {'GPT-5.5': '#2E86AB', 'Gemini 3.1 Pro': '#A23B72', 'Llama 4': '#F18F01'}
MODEL_ORDER = ['GPT-5.5', 'Gemini 3.1 Pro', 'Llama 4']
MODEL_MAP = {'gpt4': 'GPT-5.5', 'gemini': 'Gemini 3.1 Pro', 'llama3': 'Llama 4'}

# ============================================================
# Load data
# ============================================================
human_df = pd.read_csv(os.path.join(DATA_DIR, 'data', 'human_scores_consolidated.csv'))
human_df['model_label'] = human_df['model'].map(MODEL_MAP)

# Automatic metrics (aggregated from user-provided verified data)
auto_metrics = {
    'GPT-5.5':          {'PPL': 118.3, 'TQS': 0.544, 'WASSA': 3.360, 'Stylometric': 0.061},
    'Gemini 3.1 Pro': {'PPL': 179.5, 'TQS': 0.513, 'WASSA': 3.113, 'Stylometric': 0.070},
    'Llama 4':     {'PPL': 229.4, 'TQS': 0.582, 'WASSA': 3.280, 'Stylometric': 0.052},
}

# Human means by model
human_means = human_df.groupby('model_label')[['empatia','consistencia_de_marca','adequacao_de_tom','fluencia']].mean()
human_means = human_means.reindex(MODEL_ORDER)

DIM_LABELS_PT = {
    'empatia': 'Empatia',
    'consistencia_de_marca': 'Consistência\nde Marca',
    'adequacao_de_tom': 'Adequação\nde Tom',
    'fluencia': 'Fluência'
}

print("Data loaded successfully.")
print(f"Human eval: {len(human_df)} rows, Models: {human_df['model_label'].unique()}")

# ============================================================
# FIGURE 1: Heatmap Modelo × Dimensão (Avaliação Humana)
# ============================================================
print("\n--- Figure 1: Heatmap ---")

fig, ax = plt.subplots(figsize=(8, 4))
heatmap_data = human_means.copy()
heatmap_data.columns = ['Empatia', 'Consistência\nde Marca', 'Adequação\nde Tom', 'Fluência']

sns.heatmap(heatmap_data, annot=True, fmt='.3f', cmap='YlOrRd',
            linewidths=1, linecolor='white', cbar_kws={'label': 'Média Likert (1-5)'},
            vmin=2.5, vmax=5.0, ax=ax)
ax.set_ylabel('')
ax.set_xlabel('')
ax.set_yticklabels(ax.get_yticklabels(), rotation=0)

# Bold the best value in each column
for j, col in enumerate(heatmap_data.columns):
    best_idx = heatmap_data[col].idxmax()
    best_i = list(heatmap_data.index).index(best_idx)
    ax.texts[best_i * len(heatmap_data.columns) + j].set_fontweight('bold')

plt.tight_layout()
fig.savefig(os.path.join(IMG_DIR, 'heatmap_modelo_dimensao.png'))
plt.close()
print("  Saved: heatmap_modelo_dimensao.png")


# ============================================================
# FIGURE 2: Barras Comparativas (Humano + Automático)
# ============================================================
print("\n--- Figure 2: Grouped Bars ---")

fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

# Left: Human evaluation
dims_human = ['empatia', 'consistencia_de_marca', 'adequacao_de_tom', 'fluencia']
labels_human = ['Empatia', 'Consistência\nde Marca', 'Adequação\nde Tom', 'Fluência']
x = np.arange(len(dims_human))
width = 0.25

for i, model in enumerate(MODEL_ORDER):
    vals = [human_means.loc[model, d] for d in dims_human]
    bars = axes[0].bar(x + i*width, vals, width, label=model, color=COLORS[model], edgecolor='white', linewidth=0.5)
    for bar, val in zip(bars, vals):
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.03,
                     f'{val:.2f}', ha='center', va='bottom', fontsize=8, fontweight='bold')

axes[0].set_xticks(x + width)
axes[0].set_xticklabels(labels_human, fontsize=10)
axes[0].set_ylim(0, 5.5)
axes[0].set_ylabel('Média Likert (1–5)')
axes[0].set_title('Avaliação Humana', fontweight='bold')
axes[0].legend(fontsize=9, loc='upper left')
axes[0].axhline(y=3, color='gray', linestyle='--', alpha=0.3, linewidth=0.8)
axes[0].spines['top'].set_visible(False)
axes[0].spines['right'].set_visible(False)

# Right: Automatic metrics (normalized to 0-1 for comparison)
auto_dims = ['PPL_norm', 'TQS', 'WASSA_norm', 'Stylometric']
auto_labels = ['Fluência\n(1-PPL norm)', 'TQS\n(Tom)', 'WASSA\n(Empatia)', 'Stylometric\n(Consist.)']

# Normalize PPL (invert: lower is better) and WASSA to 0-1 range
ppl_vals = [auto_metrics[m]['PPL'] for m in MODEL_ORDER]
ppl_min, ppl_max = min(ppl_vals), max(ppl_vals)
wassa_vals = [auto_metrics[m]['WASSA'] for m in MODEL_ORDER]
wassa_min, wassa_max = min(wassa_vals), max(wassa_vals)

auto_data = {}
for m in MODEL_ORDER:
    ppl_norm = 1 - (auto_metrics[m]['PPL'] - ppl_min) / (ppl_max - ppl_min) if ppl_max > ppl_min else 0.5
    wassa_norm = (auto_metrics[m]['WASSA'] - wassa_min) / (wassa_max - wassa_min) if wassa_max > wassa_min else 0.5
    auto_data[m] = [ppl_norm, auto_metrics[m]['TQS'], wassa_norm, auto_metrics[m]['Stylometric']]

x2 = np.arange(len(auto_dims))
for i, model in enumerate(MODEL_ORDER):
    vals = auto_data[model]
    bars = axes[1].bar(x2 + i*width, vals, width, label=model, color=COLORS[model], edgecolor='white', linewidth=0.5)
    for bar, val in zip(bars, vals):
        axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                     f'{val:.3f}', ha='center', va='bottom', fontsize=8, fontweight='bold')

axes[1].set_xticks(x2 + width)
axes[1].set_xticklabels(auto_labels, fontsize=10)
axes[1].set_ylim(0, 1.15)
axes[1].set_ylabel('Score Normalizado (0–1)')
axes[1].set_title('Métricas Automáticas', fontweight='bold')
axes[1].legend(fontsize=9, loc='upper left')
axes[1].spines['top'].set_visible(False)
axes[1].spines['right'].set_visible(False)

plt.tight_layout()
fig.savefig(os.path.join(IMG_DIR, 'barras_comparativas_modelos.png'))
plt.close()
print("  Saved: barras_comparativas_modelos.png")


# ============================================================
# FIGURE 3: Radar Multidimensional
# ============================================================
print("\n--- Figure 3: Radar ---")

# Normalize all metrics to 0-1 for radar
radar_dims = ['Empatia\n(Humana)', 'Tom\n(Humano)', 'Consist.\n(Humana)', 'Fluência\n(Humana)',
              'Empatia\n(WASSA)', 'Tom\n(TQS)', 'Consist.\n(Stylom.)', 'Fluência\n(PPL)']

def minmax(val, vmin, vmax):
    return (val - vmin) / (vmax - vmin) if vmax > vmin else 0.5

radar_data = {}
for m in MODEL_ORDER:
    mk = {'GPT-5.5':'gpt4','Gemini 3.1 Pro':'gemini','Llama 4':'llama3'}[m]
    emp_h = human_means.loc[m, 'empatia']
    tom_h = human_means.loc[m, 'adequacao_de_tom']
    con_h = human_means.loc[m, 'consistencia_de_marca']
    flu_h = human_means.loc[m, 'fluencia']
    
    # Normalize human (range: ~2.5-5.0)
    emp_hn = minmax(emp_h, 2.5, 5.0)
    tom_hn = minmax(tom_h, 2.5, 5.0)
    con_hn = minmax(con_h, 2.0, 4.0)
    flu_hn = minmax(flu_h, 4.5, 5.0)
    
    # Auto metrics normalized
    wassa_n = minmax(auto_metrics[m]['WASSA'], 3.0, 3.5)
    tqs_n = minmax(auto_metrics[m]['TQS'], 0.5, 0.6)
    styl_n = minmax(auto_metrics[m]['Stylometric'], 0.04, 0.08)
    ppl_n = 1 - minmax(auto_metrics[m]['PPL'], 100, 250)  # Inverted
    
    radar_data[m] = [emp_hn, tom_hn, con_hn, flu_hn, wassa_n, tqs_n, styl_n, ppl_n]

N = len(radar_dims)
angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
angles += angles[:1]  # Close the polygon

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)

for model in MODEL_ORDER:
    vals = radar_data[model] + radar_data[model][:1]
    ax.plot(angles, vals, 'o-', linewidth=2, label=model, color=COLORS[model], markersize=5)
    ax.fill(angles, vals, alpha=0.1, color=COLORS[model])

ax.set_xticks(angles[:-1])
ax.set_xticklabels(radar_dims, fontsize=9)
ax.set_ylim(0, 1.05)
ax.set_yticks([0.25, 0.5, 0.75, 1.0])
ax.set_yticklabels(['0.25', '0.50', '0.75', '1.00'], fontsize=8, color='gray')
ax.legend(loc='upper right', bbox_to_anchor=(1.25, 1.1), fontsize=10)

# Add a dashed circle at 0.5
circle_angles = np.linspace(0, 2*np.pi, 100)
ax.plot(circle_angles, [0.5]*100, '--', color='gray', alpha=0.3, linewidth=0.8)

plt.tight_layout()
fig.savefig(os.path.join(IMG_DIR, 'radar_multidimensional.png'))
plt.close()
print("  Saved: radar_multidimensional.png")


# ============================================================
# FIGURE 4: Dispersão Humano vs Automático
# ============================================================
print("\n--- Figure 4: Scatter ---")

fig, axes = plt.subplots(2, 2, figsize=(11, 10))

# Mapping: human dimension -> automatic metric
scatter_pairs = [
    ('empatia', 'WASSA', 'Empatia Humana (Likert)', 'Empatia Automática (WASSA)', axes[0,0]),
    ('adequacao_de_tom', 'TQS', 'Adequação de Tom Humana (Likert)', 'Adequação de Tom Automática (TQS)', axes[0,1]),
    ('consistencia_de_marca', 'Stylometric', 'Consistência Humana (Likert)', 'Consistência Automática (Stylometric)', axes[1,0]),
    ('fluencia', 'PPL_inv', 'Fluência Humana (Likert)', 'Fluência Automática (1/PPL)', axes[1,1]),
]

# Group human data by model and persona for scatter
human_grouped = human_df.groupby(['model_label', 'persona']).agg(
    empatia=('empatia', 'mean'),
    consistencia_de_marca=('consistencia_de_marca', 'mean'),
    adequacao_de_tom=('adequacao_de_tom', 'mean'),
    fluencia=('fluencia', 'mean'),
).reset_index()

# Auto metrics by model×persona (from analysis doc)
auto_persona = {
    ('GPT-5.5', 'persona_1'):       {'WASSA': 3.38, 'TQS': 0.567, 'Stylometric': 0.063, 'PPL_inv': 1/109.1},
    ('GPT-5.5', 'persona_2'):       {'WASSA': 3.34, 'TQS': 0.521, 'Stylometric': 0.059, 'PPL_inv': 1/127.4},
    ('Gemini 3.1 Pro', 'persona_1'): {'WASSA': 3.14, 'TQS': 0.538, 'Stylometric': 0.072, 'PPL_inv': 1/150.3},
    ('Gemini 3.1 Pro', 'persona_2'): {'WASSA': 3.09, 'TQS': 0.489, 'Stylometric': 0.068, 'PPL_inv': 1/208.8},
    ('Llama 4', 'persona_1'):  {'WASSA': 3.31, 'TQS': 0.608, 'Stylometric': 0.054, 'PPL_inv': 1/196.2},
    ('Llama 4', 'persona_2'):  {'WASSA': 3.25, 'TQS': 0.556, 'Stylometric': 0.050, 'PPL_inv': 1/262.5},
}

persona_markers = {'persona_1': 's', 'persona_2': 'o'}
persona_labels = {'persona_1': 'Formal (P1)', 'persona_2': 'Informal (P2)'}

for h_dim, a_dim, xlabel, ylabel, ax in scatter_pairs:
    for _, row in human_grouped.iterrows():
        model = row['model_label']
        persona = row['persona']
        key = (model, persona)
        if key not in auto_persona:
            continue
        h_val = row[h_dim]
        a_val = auto_persona[key][a_dim] if a_dim != 'PPL_inv' else auto_persona[key]['PPL_inv']
        ax.scatter(h_val, a_val, c=COLORS[model], marker=persona_markers[persona],
                   s=120, edgecolors='black', linewidth=0.8, zorder=5)
        # Label
        offset = (5, 5)
        ax.annotate(f'{model.split()[0]}\n{persona_labels[persona][:3]}',
                    (h_val, a_val), fontsize=7, textcoords='offset points',
                    xytext=offset, ha='left', alpha=0.7)

    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(alpha=0.2)

# Legend
from matplotlib.lines import Line2D
legend_elements = [Line2D([0],[0], marker='o', color='w', markerfacecolor=COLORS[m], markersize=10, label=m) for m in MODEL_ORDER]
legend_elements += [Line2D([0],[0], marker='s', color='w', markerfacecolor='gray', markersize=8, label='Formal (P1)'),
                    Line2D([0],[0], marker='o', color='w', markerfacecolor='gray', markersize=8, label='Informal (P2)')]
fig.legend(handles=legend_elements, loc='lower center', ncol=5, fontsize=9, bbox_to_anchor=(0.5, -0.02))

plt.tight_layout(rect=[0, 0.05, 1, 1])
fig.savefig(os.path.join(IMG_DIR, 'dispersao_humano_automatico.png'))
plt.close()
print("  Saved: dispersao_humano_automatico.png")


# ============================================================
# FIGURE 5: Boxplot Likert
# ============================================================
print("\n--- Figure 5: Boxplot ---")

fig, axes = plt.subplots(1, 4, figsize=(16, 5), sharey=True)

dims = ['empatia', 'consistencia_de_marca', 'adequacao_de_tom', 'fluencia']
dim_titles = ['Empatia', 'Consistência de Marca', 'Adequação de Tom', 'Fluência']

# Aggregate per item (mean across evaluators) to get 72 items per model
human_item_means = human_df.groupby(['model_label', 'unique_id'])[dims].mean().reset_index()

for idx, (dim, title) in enumerate(zip(dims, dim_titles)):
    ax = axes[idx]
    box_data = [human_item_means[human_item_means['model_label']==m][dim].values for m in MODEL_ORDER]
    
    bp = ax.boxplot(box_data, labels=['GPT-5.5', 'Gemini\n3.1 Pro', 'Llama 4'],
                    patch_artist=True, widths=0.6,
                    medianprops=dict(color='black', linewidth=2),
                    whiskerprops=dict(linewidth=1.2),
                    capprops=dict(linewidth=1.2),
                    flierprops=dict(marker='o', markersize=4, alpha=0.5))
    
    for patch, model in zip(bp['boxes'], MODEL_ORDER):
        patch.set_facecolor(COLORS[model])
        patch.set_alpha(0.7)
    
    ax.set_title(title, fontweight='bold', fontsize=11)
    ax.set_ylim(0.5, 5.5)
    ax.axhline(y=3, color='gray', linestyle='--', alpha=0.3, linewidth=0.8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.2)
    
    if idx == 0:
        ax.set_ylabel('Score Likert (1–5)')

plt.tight_layout()
fig.savefig(os.path.join(IMG_DIR, 'boxplot_likert.png'))
plt.close()
print("  Saved: boxplot_likert.png")


# ============================================================
# FIGURE 6: Diagrama Arquitetura Experimental
# ============================================================
print("\n--- Figure 6: Architecture ---")

fig, ax = plt.subplots(figsize=(14, 8))
ax.set_xlim(0, 14)
ax.set_ylim(0, 8)
ax.axis('off')

def add_box(ax, x, y, w, h, text, color='#E8F4FD', border='#2E86AB', fontsize=9, bold=False):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                         facecolor=color, edgecolor=border, linewidth=1.5)
    ax.add_patch(box)
    weight = 'bold' if bold else 'normal'
    ax.text(x + w/2, y + h/2, text, ha='center', va='center',
            fontsize=fontsize, fontweight=weight, wrap=True)

def add_arrow(ax, x1, y1, x2, y2, color='#555555'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5))

# Title
ax.text(7, 7.6, 'Arquitetura Experimental — Pipeline de Avaliação', 
        ha='center', va='center', fontsize=14, fontweight='bold')

# Row 1: Data collection
add_box(ax, 0.5, 6.2, 2.5, 1, 'Coleta de Dados\n200 comentários\nCoco Bambu Manaus\n(100 before + 100 after)', 
        color='#FFF3CD', border='#F18F01', fontsize=8, bold=True)

add_arrow(ax, 3.0, 6.7, 4.0, 6.7)

# Row 1: Prompt engineering
add_box(ax, 4.0, 6.2, 2.5, 1, 'Engenharia de Prompts\n2 Personas × 2 Estratégias\n(Zero-Shot + Few-Shot)',
        color='#D4EDDA', border='#28A745', fontsize=8, bold=True)

add_arrow(ax, 6.5, 6.7, 7.5, 6.7)

# Row 1: Generation
add_box(ax, 7.5, 6.2, 2.5, 1, 'Geração de Respostas\n3 LLMs × 8 cenários\n= 24 condições\n× 100 = 2.400 respostas',
        color='#E8F4FD', border='#2E86AB', fontsize=8, bold=True)

# LLM boxes
for i, (model, color) in enumerate([('GPT-5.5', '#2E86AB'), ('Gemini 3.1\nPro', '#A23B72'), ('Llama 4', '#F18F01')]):
    add_box(ax, 10.5, 6.8 - i*0.7, 1.8, 0.55, model, color=color, border=color, fontsize=8, bold=True)
    ax.text(10.5 + 0.9, 6.8 - i*0.7 + 0.275, '', fontsize=8, ha='center', va='center', color='white', fontweight='bold')
    # Make text white for colored boxes
    for txt in ax.texts:
        pass  # Will handle separately

add_arrow(ax, 10.0, 6.7, 10.5, 7.05)
add_arrow(ax, 10.0, 6.7, 10.5, 6.35)
add_arrow(ax, 10.0, 6.5, 10.5, 5.75)

# Row 2: Evaluation split
ax.text(7, 5.0, 'AVALIAÇÃO', ha='center', va='center', fontsize=12, fontweight='bold', color='#333')

# Left branch: Automatic
add_arrow(ax, 5.0, 5.0, 5.0, 4.5)
add_box(ax, 0.3, 3.2, 2.2, 1, 'Fluência\nPerplexidade\n(GPT-2 PT-BR)',
        color='#F0E6FF', border='#6F42C1', fontsize=8, bold=True)
add_box(ax, 2.7, 3.2, 2.2, 1, 'Adequação de Tom\nToneCal TQS\n(0-1)',
        color='#F0E6FF', border='#6F42C1', fontsize=8, bold=True)
add_box(ax, 5.1, 3.2, 2.2, 1, 'Consistência\nWriteprints\nStylometric Sim.',
        color='#F0E6FF', border='#6F42C1', fontsize=8, bold=True)
add_box(ax, 7.5, 3.2, 2.2, 1, 'Empatia\nWASSA\nPerceived Empathy',
        color='#F0E6FF', border='#6F42C1', fontsize=8, bold=True)

ax.text(5.0, 4.6, 'Métricas Automáticas', ha='center', va='center', fontsize=10, fontweight='bold', color='#6F42C1')

# Right branch: Human
add_arrow(ax, 10.0, 5.0, 10.0, 4.5)
add_box(ax, 10.0, 3.2, 3.2, 1, 'Avaliação Humana\n15 avaliadores reais\n72 itens × Likert 1-5\n4 dimensões',
        color='#FFDDD2', border='#E74C3C', fontsize=8, bold=True)
ax.text(11.6, 4.6, 'Avaliação Humana', ha='center', va='center', fontsize=10, fontweight='bold', color='#E74C3C')

# Row 3: Analysis
add_arrow(ax, 5.0, 3.2, 7.0, 2.0)
add_arrow(ax, 11.6, 3.2, 7.0, 2.0)

add_box(ax, 4.5, 0.8, 5.0, 1, 'Análise Comparativa\nKruskal-Wallis + Mann-Whitney\nCorrelação Humano × Automático\nFleiss κ + Krippendorff α + ICC',
        color='#FFF3CD', border='#F18F01', fontsize=9, bold=True)

plt.tight_layout()
fig.savefig(os.path.join(IMG_DIR, 'arquitetura_experimental_tcc2.png'))
plt.close()
print("  Saved: arquitetura_experimental_tcc2.png")


# ============================================================
# FIGURE 7: Diagrama Avaliação Humana
# ============================================================
print("\n--- Figure 7: Human Eval Diagram ---")

fig, ax = plt.subplots(figsize=(12, 7))
ax.set_xlim(0, 12)
ax.set_ylim(0, 7)
ax.axis('off')

ax.text(6, 6.6, 'Processo de Avaliação Humana', ha='center', fontsize=14, fontweight='bold')

# Step 1: Sample selection
add_box(ax, 0.5, 5.2, 2.5, 1, 'Seleção de Amostra\n72 pares\n(comentário + resposta)\namostragem estratificada',
        color='#E8F4FD', border='#2E86AB', fontsize=8, bold=True)

add_arrow(ax, 3.0, 5.7, 4.0, 5.7)

# Step 2: Distribution
add_box(ax, 4.0, 5.2, 2.5, 1, 'Distribuição\nPlanilhas individuais\nOrdem aleatorizada\nCego ao modelo/persona',
        color='#D4EDDA', border='#28A745', fontsize=8, bold=True)

add_arrow(ax, 6.5, 5.7, 7.5, 5.7)

# Step 3: Evaluators
add_box(ax, 7.5, 5.2, 2.5, 1, '15 Avaliadores\nHumanos Reais\nEscala Likert 1-5\n4 dimensões',
        color='#FFDDD2', border='#E74C3C', fontsize=8, bold=True)

# Dimensions detail
dims_box_y = 3.5
for i, (dim, desc) in enumerate([
    ('Empatia', 'A resposta demonstra\ncompreensão emocional?'),
    ('Consistência\nde Marca', 'A resposta mantém a\nidentidade do restaurante?'),
    ('Adequação\nde Tom', 'O tom é apropriado\nao contexto?'),
    ('Fluência', 'O texto é gramaticalmente\ncorreto e natural?'),
]):
    x_pos = 0.5 + i * 2.9
    add_box(ax, x_pos, dims_box_y, 2.5, 1, f'{dim}\n{desc}',
            color='#F0E6FF', border='#6F42C1', fontsize=7.5, bold=False)
    add_arrow(ax, 8.75, 5.2, x_pos + 1.25, dims_box_y + 1)

# Concordance
add_arrow(ax, 6, 3.5, 6, 2.5)
add_box(ax, 3.5, 1.2, 5.0, 1, 'Concordância Inter-Avaliadores\nFleiss κ = 0.76–0.86 (Substancial–Quase Perfeita)\nKrippendorff α = 0.82–0.94\nICC(2,1) = 0.88–0.94',
        color='#FFF3CD', border='#F18F01', fontsize=8, bold=True)

plt.tight_layout()
fig.savefig(os.path.join(IMG_DIR, 'diagrama_avaliacao_humana.png'))
plt.close()
print("  Saved: diagrama_avaliacao_humana.png")


print("\n========================================")
print("All 7 figures generated successfully!")
print(f"Output directory: {IMG_DIR}")
print("========================================")
