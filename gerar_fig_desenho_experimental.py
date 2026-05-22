"""
Generate fig_desenho_experimental.png — Desenho Experimental para Avaliação de LLMs.

Updates from previous version:
  Box 1 (Coleta de Dados): "Google Reviews" -> "Coco Bambu (Manaus)"
  Box 3 (Modelos Avaliados): GPT-4 -> GPT 5.5, Gemini -> Gemini 3.1, Llama 3 -> Llama 4
  Arrows: redesenhadas com roteamento ortogonal (sem cruzar caixas);
          origem e destino claramente identificados.
"""
from pathlib import Path as FsPath

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, PathPatch
from matplotlib.path import Path

OUT_DIR = FsPath(
    r"C:\Users\t-ddasilva\FilesPersonal\Trabalho de Conclusão de Curso\tcc_img_assets\new_assets"
)
OUT_PNG = OUT_DIR / "fig_desenho_experimental.png"

# Palette ------------------------------------------------------------------
NAVY = "#1f3a5f"
NAVY_DARK = "#16294a"
BLUE_HL = "#1565c0"          # highlighted box (3 - Modelos Avaliados)
BODY_GRAY_BLUE = "#eaf0f5"
HEADER_TEXT = "white"
TEXT_DARK = "#1b1f24"
NAVY_PURPLE = "#1a237e"
LAVENDER_BODY = "#ede7f6"
GREEN_DARK = "#2e7d32"
GREEN_BODY = "#e8f5e9"
ARROW_COLOR = "#2c3e50"

HEADER_H = 0.55
NUM_RADIUS = 0.22


def draw_box(ax, x, y, w, h, *, header, body_lines, header_color=NAVY,
             body_color=BODY_GRAY_BLUE, edge_color=NAVY, italic_body=False,
             body_font=15, header_font=17):
    # Outer body
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.12",
        linewidth=1.6, edgecolor=edge_color, facecolor=body_color, zorder=2,
    ))
    # Header bar
    ax.add_patch(FancyBboxPatch(
        (x + 0.08, y + h - HEADER_H - 0.08), w - 0.16, HEADER_H,
        boxstyle="round,pad=0.0,rounding_size=0.08",
        linewidth=0, facecolor=header_color, zorder=3,
    ))
    ax.text(x + w / 2, y + h - HEADER_H / 2 - 0.08, header,
            ha="center", va="center", color=HEADER_TEXT,
            fontsize=header_font, fontweight="bold", zorder=4)
    # Body lines
    if body_lines:
        n = len(body_lines)
        top = y + h - HEADER_H - 0.35
        bottom = y + 0.35
        if n == 1:
            ys = [(top + bottom) / 2]
        else:
            step = (top - bottom) / (n - 1)
            ys = [top - i * step for i in range(n)]
        for line, ly in zip(body_lines, ys):
            ax.text(x + w / 2, ly, line,
                    ha="center", va="center", color=TEXT_DARK,
                    fontsize=body_font,
                    fontstyle="italic" if italic_body else "normal", zorder=4)


def draw_number(ax, x, y, n):
    ax.add_patch(Circle((x, y), NUM_RADIUS, facecolor=NAVY_DARK,
                        edgecolor="white", linewidth=2, zorder=6))
    ax.text(x, y, str(n), ha="center", va="center",
            color="white", fontsize=14, fontweight="bold", zorder=7)


def ortho_arrow(ax, points, *, color=ARROW_COLOR, lw=2.2, zorder=5,
                head_length=0.18, head_width=0.12):
    """Desenha seta ortogonal seguindo a sequência de pontos.

    A última coordenada recebe a ponta da seta (triângulo cheio).
    Os segmentos são unidos com cantos arredondados (joinstyle round).
    """
    if len(points) < 2:
        return
    codes = [Path.MOVETO] + [Path.LINETO] * (len(points) - 1)
    path = Path(points, codes)
    ax.add_patch(PathPatch(
        path, facecolor="none", edgecolor=color, linewidth=lw,
        capstyle="round", joinstyle="round", zorder=zorder,
    ))
    # Arrowhead at the last point, pointing in the direction of last segment
    px, py = points[-2]
    tx, ty = points[-1]
    import numpy as np
    dx, dy = tx - px, ty - py
    norm = (dx ** 2 + dy ** 2) ** 0.5
    if norm == 0:
        return
    ux, uy = dx / norm, dy / norm
    # Perpendicular
    nx, ny = -uy, ux
    # Triangle vertices
    tip = (tx, ty)
    base_center = (tx - ux * head_length, ty - uy * head_length)
    left = (base_center[0] + nx * head_width / 2,
            base_center[1] + ny * head_width / 2)
    right = (base_center[0] - nx * head_width / 2,
             base_center[1] - ny * head_width / 2)
    tri = Path([tip, left, right, tip],
               [Path.MOVETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY])
    ax.add_patch(PathPatch(tri, facecolor=color, edgecolor=color,
                           linewidth=0.5, zorder=zorder + 0.1))


def main() -> None:
    fig, ax = plt.subplots(figsize=(19.2, 11.4), dpi=220)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9.5)
    ax.set_axis_off()

    # Title -----------------------------------------------------------------
    ax.text(8, 9.15, "Desenho Experimental para Avaliação de LLMs",
            ha="center", va="center",
            fontsize=24, fontweight="bold", color=NAVY_DARK)
    ax.text(8, 8.65, "Engenharia de Prompts para Respostas de Restaurantes em Português",
            ha="center", va="center",
            fontsize=15, fontstyle="italic", color="#4a5460")

    # Top row boxes ---------------------------------------------------------
    top_y = 4.7
    top_h = 3.6
    top_w = 3.55
    gaps = [0.30, 4.05, 7.80, 11.55]  # x positions

    draw_box(ax, gaps[0], top_y, top_w, top_h,
             header="Coleta de Dados",
             body_lines=[
                 "Comentários de Restaurantes",
                 "Coco Bambu (Manaus)",
                 "Before LLM Release",
                 "After LLM Release",
             ])
    draw_number(ax, gaps[0] + 0.45, top_y + top_h + 0.05, 1)

    draw_box(ax, gaps[1], top_y, top_w, top_h,
             header="Engenharia de Prompts",
             body_lines=[
                 "Zero-Shot",
                 "Few-Shot",
                 "Persona Formal",
                 "Persona Acolhedora",
             ])
    draw_number(ax, gaps[1] + 0.45, top_y + top_h + 0.05, 2)

    draw_box(ax, gaps[2], top_y, top_w, top_h,
             header="Modelos Avaliados",
             body_lines=[
                 "GPT 5.5",
                 "Gemini 3.1",
                 "Llama 4",
                 "3 LLMs",
             ],
             header_color=BLUE_HL,
             body_color="#e3f0fb",
             edge_color=BLUE_HL)
    draw_number(ax, gaps[2] + 0.45, top_y + top_h + 0.05, 3)

    draw_box(ax, gaps[3], top_y, top_w, top_h,
             header="Geração de Respostas",
             body_lines=[
                 "Respostas Geradas",
                 "Corpus Resultante",
                 "(2.400 respostas)",
                 "24 cenários",
             ])
    draw_number(ax, gaps[3] + 0.45, top_y + top_h + 0.05, 4)

    # Top-row arrows (1 -> 2 -> 3 -> 4) -------------------------------------
    for i in range(3):
        x_start = gaps[i] + top_w
        x_end = gaps[i + 1]
        y_mid = top_y + top_h / 2
        ortho_arrow(ax, [(x_start + 0.02, y_mid), (x_end - 0.02, y_mid)])

    # Bottom row boxes ------------------------------------------------------
    bot_y = 0.30
    bot_h = 3.85

    # Box 5: Avaliação Automática (wide, with 4 sub-boxes)
    b5_x, b5_w = 0.30, 7.55
    draw_box(ax, b5_x, bot_y, b5_w, bot_h,
             header="Avaliação Automática",
             body_lines=[])
    draw_number(ax, b5_x + 0.45, bot_y + bot_h + 0.05, 5)

    sub_y = bot_y + 0.45
    sub_h = bot_h - HEADER_H - 0.75
    sub_w = (b5_w - 0.50 - 3 * 0.18) / 4
    sub_titles = [
        ("Adequação", "de Tom", "ToneCal (TQS)"),
        ("Empatia", "Percebida", "WASSA"),
        ("Fluência", "", "Perplexidade\nGPT-2 PT-BR"),
        ("Similaridade", "Estilométrica", "Writeprints"),
    ]
    for i, (t1, t2, metric) in enumerate(sub_titles):
        sx = b5_x + 0.25 + i * (sub_w + 0.18)
        ax.add_patch(FancyBboxPatch(
            (sx, sub_y), sub_w, sub_h,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            linewidth=1.3, edgecolor=NAVY, facecolor="white",
            linestyle="--", zorder=3,
        ))
        ax.text(sx + sub_w / 2, sub_y + sub_h - 0.30, t1,
                ha="center", va="center", color=NAVY_DARK,
                fontsize=14, fontweight="bold")
        if t2:
            ax.text(sx + sub_w / 2, sub_y + sub_h - 0.65, t2,
                    ha="center", va="center", color=NAVY_DARK,
                    fontsize=14, fontweight="bold")
        ax.text(sx + sub_w / 2, sub_y + 0.45, metric,
                ha="center", va="center", color=TEXT_DARK,
                fontsize=12, fontstyle="italic")

    # Box 6: Avaliação Humana
    b6_x, b6_w = 8.05, 3.55
    draw_box(ax, b6_x, bot_y, b6_w, bot_h,
             header="Avaliação Humana",
             body_lines=[
                 "15 Avaliadores Humanos",
                 "Escala Likert (1–5)",
                 "Fleiss Kappa",
                 "Krippendorff α | ICC",
             ],
             header_color=NAVY_PURPLE,
             body_color=LAVENDER_BODY,
             edge_color=NAVY_PURPLE)
    draw_number(ax, b6_x + 0.45, bot_y + bot_h + 0.05, 6)

    # Box 7: Análise Comparativa
    b7_x, b7_w = 11.80, 3.90
    draw_box(ax, b7_x, bot_y, b7_w, bot_h,
             header="Análise Comparativa",
             body_lines=[
                 "Comparação entre Modelos",
                 "Análise Estratificada",
                 "Before vs After",
                 "Zero-Shot vs Few-Shot",
                 "Personas",
             ],
             header_color=GREEN_DARK,
             body_color=GREEN_BODY,
             edge_color=GREEN_DARK)
    draw_number(ax, b7_x + 0.45, bot_y + bot_h + 0.05, 7)

    # ------------------------------------------------------------------
    # Cross arrows (orthogonal routing through inter-row channel)
    # Channel between rows: y in [bot_y + bot_h, top_y] = [4.15, 4.70]
    # Three horizontal levels (parallel, sem cruzamento):
    #     y = 4.28  -> seta  4 -> 5
    #     y = 4.42  -> seta  4 -> 6
    #     y = 4.58  -> seta  5 -> 7  (passa por cima da caixa 6)
    # ------------------------------------------------------------------
    top_bot = top_y                       # y do fundo da fileira de cima
    box_top = bot_y + bot_h               # y do topo da fileira de baixo

    y_arr_45 = 4.28
    y_arr_46 = 4.42
    y_arr_57 = 4.58

    # ---- 4 -> 5 (do canto inferior-esquerdo da caixa 4 até o topo da 5)
    x_out_45 = gaps[3] + 0.80             # sai do fundo da caixa 4 (esquerda)
    x_in_5 = b5_x + b5_w / 2 - 1.0        # entra na caixa 5 (centro-esquerda)
    ortho_arrow(ax, [
        (x_out_45, top_bot),
        (x_out_45, y_arr_45),
        (x_in_5,  y_arr_45),
        (x_in_5,  box_top),
    ])

    # ---- 4 -> 6 (do fundo da caixa 4 até o topo da 6)
    x_out_46 = gaps[3] + top_w / 2 + 0.20
    x_in_6 = b6_x + b6_w / 2
    ortho_arrow(ax, [
        (x_out_46, top_bot),
        (x_out_46, y_arr_46),
        (x_in_6,  y_arr_46),
        (x_in_6,  box_top),
    ])

    # ---- 5 -> 7  (rota: gap entre 5 e 6, sobe pelo canal, atravessa
    #              acima da caixa 6, e desce no topo da 7)
    gap_56_x = (b5_x + b5_w + b6_x) / 2   # meio do gap entre 5 e 6 (x ≈ 7.95)
    x_in_7 = b7_x + 0.9
    y_out_5 = bot_y + bot_h / 2 + 0.35
    ortho_arrow(ax, [
        (b5_x + b5_w, y_out_5),
        (gap_56_x,   y_out_5),
        (gap_56_x,   y_arr_57),
        (x_in_7,     y_arr_57),
        (x_in_7,     box_top),
    ])

    # ---- 6 -> 7 (curta, horizontal no gap entre 6 e 7)
    y_67 = bot_y + bot_h / 2
    ortho_arrow(ax, [
        (b6_x + b6_w, y_67),
        (b7_x,        y_67),
    ])

    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.savefig(OUT_PNG, dpi=300, bbox_inches="tight", pad_inches=0.15,
                facecolor="white")
    plt.close(fig)
    print(f"Saved: {OUT_PNG} ({OUT_PNG.stat().st_size/1024:.1f} KB)")


if __name__ == "__main__":
    main()
