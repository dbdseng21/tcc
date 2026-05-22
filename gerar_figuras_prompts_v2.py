# -*- coding: utf-8 -*-
"""
Reconstrói os templates dos prompts Zero-Shot e Few-Shot com fontes
GRANDES e contraste forte. Usa um cursor vertical para impedir sobreposições.
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

BASE = r"C:\Users\t-ddasilva\FilesPersonal\Trabalho de Conclusão de Curso"
OUT = os.path.join(BASE, "figuras_formatadas_fonte")
os.makedirs(OUT, exist_ok=True)

# Paleta
HEADER_BG = "#1F4E79"
TITLE_BG = "#173758"
BODY_FG = "#0F1419"
BG = "#FAFCFE"
EXAMPLE_BG = "#E8F5E9"
EXAMPLE_FG = "#1B5E20"
INPUT_BG = "#FFF8DC"
INPUT_FG = "#B8651A"
BORDER = "#0E3D6E"

# Fontes
F_TITLE = 30
F_HEADER = 22
F_BODY = 19
F_EXAMPLE = 22
F_INPUT = 22

# Layout
PAGE_W = 16.0
LEFT, RIGHT = 0.7, 15.3             # margens horizontais do conteúdo (mais espaço)
BULLET_X, TEXT_X = 1.3, 1.7         # posição dos bullets
HEAD_H = 0.75                       # altura padrão do cabeçalho azul
LINE_H = 0.50                       # altura de uma linha de texto/bullet
GAP_AFTER_HEAD = 0.40               # respiro abaixo do cabeçalho antes do conteúdo
GAP_BELOW = 0.40                    # respiro entre fim de uma seção e próximo cabeçalho


class Renderer:
    def __init__(self, fig_w=16.0, fig_h=30):
        self.fig = plt.figure(figsize=(fig_w, fig_h))
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(0, PAGE_W)
        self.ax.set_ylim(0, fig_h)
        self.ax.axis("off")
        self.h = fig_h
        # Cursor começa no topo (dentro da margem)
        self.y = fig_h - 0.30

    def title(self, text):
        h = 1.0
        self.y -= 0.20  # respiro do topo
        rect = Rectangle((LEFT, self.y - h), RIGHT - LEFT, h,
                         facecolor=TITLE_BG, edgecolor=TITLE_BG)
        self.ax.add_patch(rect)
        self.ax.text((LEFT + RIGHT) / 2, self.y - h / 2, text,
                     ha="center", va="center", color="white",
                     fontsize=F_TITLE, fontweight="bold")
        self.y -= h + 0.35  # respiro abaixo do título principal

    def section(self, text):
        rect = Rectangle((LEFT, self.y - HEAD_H), RIGHT - LEFT, HEAD_H,
                         facecolor=HEADER_BG, edgecolor=HEADER_BG)
        self.ax.add_patch(rect)
        self.ax.text((LEFT + RIGHT) / 2, self.y - HEAD_H / 2, text,
                     ha="center", va="center", color="white",
                     fontsize=F_HEADER, fontweight="bold")
        self.y -= HEAD_H + GAP_AFTER_HEAD

    def body(self, text, indent=1.0, color=BODY_FG, fontsize=F_BODY,
             weight="normal"):
        self.ax.text(indent, self.y, text, ha="left", va="top",
                     fontsize=fontsize, color=color, fontweight=weight)
        self.y -= LINE_H

    def bullet(self, text):
        self.ax.text(BULLET_X, self.y, "•", ha="center", va="top",
                     fontsize=F_BODY + 4, color=HEADER_BG, fontweight="bold")
        self.ax.text(TEXT_X, self.y, text, ha="left", va="top",
                     fontsize=F_BODY, color=BODY_FG)
        self.y -= LINE_H

    def dashed_line(self):
        self.y -= 0.10
        self.ax.plot([1.0, RIGHT - 0.3], [self.y, self.y], "--",
                     color="#999", linewidth=1.0)
        self.y -= 0.30

    def spacer(self, amount=0.40):
        self.y -= amount

    def example_badge(self, text):
        # Caixa verde clarinha para o cabeçalho "EXEMPLO X"
        h = 0.65
        box = FancyBboxPatch((LEFT, self.y - h), RIGHT - LEFT, h,
                             boxstyle="round,pad=0.02,rounding_size=0.04",
                             facecolor=EXAMPLE_BG, edgecolor=EXAMPLE_FG,
                             linewidth=1.5)
        self.ax.add_patch(box)
        self.ax.text((LEFT + RIGHT) / 2, self.y - h / 2, text,
                     ha="center", va="center", color=EXAMPLE_FG,
                     fontsize=F_EXAMPLE, fontweight="bold")
        self.y -= h + 0.35

    def input_box(self, text):
        # Cabeçalho "Entrada" depois caixa amarela
        self.section("Entrada")
        h = 0.7
        box = FancyBboxPatch((LEFT, self.y - h), RIGHT - LEFT, h,
                             boxstyle="round,pad=0.02,rounding_size=0.04",
                             facecolor=INPUT_BG, edgecolor=INPUT_FG, linewidth=1.5)
        self.ax.add_patch(box)
        self.ax.text((LEFT + RIGHT) / 2, self.y - h / 2, text,
                     ha="center", va="center", color=INPUT_FG,
                     fontsize=F_INPUT, fontweight="bold", family="monospace")
        self.y -= h + 0.60

    def finish(self, out_path):
        bottom = max(self.y - 0.40, 0.05)
        outer = FancyBboxPatch((0.05, bottom), PAGE_W - 0.10, self.h - 0.15 - bottom,
                               boxstyle="round,pad=0.02,rounding_size=0.05",
                               facecolor="none", edgecolor=BORDER, linewidth=2.2)
        self.ax.add_patch(outer)
        self.ax.set_ylim(bottom - 0.20, self.h - 0.05)
        used = self.h - bottom + 0.30
        self.fig.set_size_inches(PAGE_W, used)
        self.fig.savefig(out_path, dpi=300, bbox_inches="tight",
                         pad_inches=0.30, facecolor=BG)
        plt.close(self.fig)


# ============================================================
# Zero-Shot
# ============================================================
print("--- Zero-Shot ---")
r = Renderer(fig_w=16.0, fig_h=30)

r.title("Template do Prompt Zero-Shot")

r.section("Contexto e Papel")
r.body("Você é o gerente de mídias sociais de um restaurante em Manaus")
r.body("e responde comentários públicos de clientes em português do Brasil.")
r.dashed_line()
r.body("Persona de marca: {PERSONA}")
r.body("→  sofisticada e formal  |  acolhedora e informal",
       indent=2.6, color="#333")
r.spacer(0.35)

r.section("Objetivo")
r.body("Escrever uma resposta curta, contextualizada ao comentário, preservando:")
for b in ["adequação de tom", "percepção de empatia",
          "consistência de marca", "fluência em português"]:
    r.bullet(b)
r.spacer(GAP_BELOW)

r.section("Instruções de Comportamento")
for b in [
    "Soe formal/refinada (ou próxima/calorosa, conforme persona)",
    "Demonstre consideração genuína pela experiência do cliente",
    "Evite soar fria, genérica ou mecanicamente corporativa",
    "Leia o comentário com atenção e responda aos pontos mencionados",
    "Não copie a resposta de referência humana",
    "Não invente fatos, políticas, compensações, nomes ou promessas",
    "Não use emojis, hashtags ou aspas",
]:
    r.bullet(b)
r.spacer(GAP_BELOW)

r.section("Regras de Adaptação")
for b in [
    "Comentário positivo → agradeça, valorize elogios, convide a retornar",
    "Comentário negativo → reconheça insatisfação, expresse pesar, acolha feedback",
    "Comentário misto → reconheça elogios e pontos de insatisfação",
    "Ocasião especial/frustração → sensibilidade e sobriedade",
    "Menção a prato/ambiente/demora → responda esses elementos",
]:
    r.bullet(b)
r.spacer(GAP_BELOW)

r.section("Restrições de Saída")
for b in [
    "Apenas uma resposta final ao cliente",
    "Entre 2 e 4 frases",
    "Específica para o comentário recebido",
    "Evite estruturas repetitivas",
]:
    r.bullet(b)
r.spacer(GAP_BELOW)

r.input_box("[Comentário do cliente: {customer_comment}]")
r.finish(os.path.join(OUT, "zeroshot.png"))
print("  -> zeroshot.png")


# ============================================================
# Few-Shot
# ============================================================
print("--- Few-Shot ---")
r = Renderer(fig_w=16.0, fig_h=30)

r.title("Template do Prompt Few-Shot")

r.section("Contexto, Papel e Objetivo")
r.body("Você é o gerente de mídias sociais de um restaurante em Manaus.")
r.body("Persona de marca: {PERSONA}")
r.body("→  sofisticada e formal  |  acolhedora e informal",
       indent=2.6, color="#333")
r.dashed_line()
r.body("Preservar: adequação de tom  |  empatia  |  consistência de marca  |  fluência")
r.spacer(GAP_BELOW)

r.section("Exemplos Demonstrativos  (In-Context Learning)")

r.example_badge("EXEMPLO 1")
r.body('Comentário: "Amei a experiência e o atendimento foi incrível."')
r.body('Resposta: "Ficamos honrados com seu retorno tão positivo.')
r.body("É uma satisfação saber que sua experiência foi marcante e que o",
       indent=2.4)
r.body('atendimento atendeu às suas expectativas. Esperamos recebê-lo novamente."',
       indent=2.4)
r.dashed_line()

r.example_badge("EXEMPLO 2")
r.body('Comentário: "A comida estava boa, mas o atendimento demorou bastante."')
r.body('Resposta: "Agradecemos por compartilhar sua experiência conosco.')
r.body("Ficamos satisfeitos que apreciou a refeição, mas lamentamos pela",
       indent=2.4)
r.body('demora. Esperamos proporcionar uma experiência mais harmoniosa."',
       indent=2.4)
r.spacer(GAP_BELOW)

r.section("Instrução Final")
r.body("Responda ao comentário abaixo sem copiar os exemplos.")
r.spacer(GAP_BELOW)

r.section("Regras")
for b in [
    "Não invente fatos, compensações, contatos ou promessas",
    "Não use emojis, hashtags ou aspas",
    "Responda em 2 a 4 frases",
    "Seja específica para o comentário",
]:
    r.bullet(b)
r.spacer(GAP_BELOW)

r.input_box("[Comentário do cliente: {customer_comment}]")
r.finish(os.path.join(OUT, "fewshot.png"))
print("  -> fewshot.png")

print("\nOK — arquivos em:", OUT)
