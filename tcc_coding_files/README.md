# Materiais de Reprodutibilidade — TCC2

> Engenharia de Prompts para Respostas de Restaurantes em Português:
> Avaliação de Tom, Empatia e Consistência de Marca com LLMs.
>
> Danilo Bruno da Silva — Universidade do Estado do Amazonas (UEA).

Este diretório contém os artefatos públicos do experimento descrito no TCC:
*prompts*, código das métricas automáticas, escores agregados da avaliação
humana e sumários estatísticos por cenário. O *corpus* bruto, as respostas
geradas pelas *LLMs* e os arquivos de avaliação com texto integral não são
disponibilizados publicamente em razão de questões de privacidade (LGPD) e
de propriedade da informação dos estabelecimentos analisados.

## Desenho experimental

O estudo cruza três fatores em um experimento fatorial completo:

| Fator | Níveis |
|---|---|
| **Modelo** | GPT-5.5, Gemini 3.1, Llama 4 |
| **Persona** | P1 — sofisticada e formal; P2 — acolhedora e informal |
| **Estratégia de *prompt*** | *zero-shot*, *few-shot* |
| **Período do comentário** | *before* (pré-popularização das LLMs), *after* (pós) |

Total: **3 × 2 × 2 × 2 = 24 cenários experimentais**, cada um cobrindo 100
comentários do *Corpus de Origem*, totalizando **2.400 respostas avaliadas**
(*Corpus Resultante*).

A avaliação foi conduzida em duas frentes complementares:

* **Avaliação humana:** 15 avaliadores independentes, escala Likert de 1 a 5,
  72 itens em comum entre avaliadores (*gold standard*) para cálculo de
  concordância (Fleiss' Kappa, Krippendorff's Alpha ordinal, ICC(2,1)).
* **Métricas automáticas multidimensionais:**

  | Dimensão | Método |
  |---|---|
  | Fluência | Perplexidade com GPT-2 PT-BR |
  | Adequação de tom | ToneCal PT-BR |
  | Consistência de marca | Similaridade estilométrica *Writeprints-like* |
  | Empatia percebida | Modelo *WASSA* (análise exploratória) |

## Estrutura do diretório

```
tcc_coding_files/
├── data/
│   └── human_scores_consolidated.csv     # Escores Likert agregados dos
│                                         #   15 avaliadores (sem texto
│                                         #   das respostas)
│
├── docs/
│   ├── perfis_avaliadores.md             # Perfis demográficos dos 15
│   │                                     #   avaliadores
│   └── relatorio_concordancia.md         # Fleiss / Krippendorff / ICC
│
├── prompts/                              # Prompts utilizados na geração
│   ├── gpt/      persona_{1,2}_{zero,few}_shot.txt
│   ├── gemini/   persona_{1,2}_{zero,few}_shot.txt
│   └── llama4/   persona_{1,2}_{zero,few}_shot.txt
│
├── results/                              # Sumários estatísticos por cenário
│   ├── fluency/                          # Perplexidade GPT-2 PT-BR
│   ├── tonecal/                          # Adequação de tom (ToneCal)
│   ├── stylometric_similarity/           # Consistência de marca
│   └── perceived_empathy/                # WASSA (exploratório)
│
├── tcc2/algorithms/                      # Implementação das métricas
│   ├── adequacao_de_tom/                 # ToneCal PT-BR
│   ├── consistência_de_marca/            # Stylometric Similarity
│   ├── empatia/                          # WASSA empathy scoring
│   └── fluencia/                         # GPT-2 PT-BR perplexity
│
├── gerar_visualizacoes_tcc2.py           # Gera as figuras do TCC
├── requirements.txt
└── README.md
```

## Reproduzindo as métricas

Pré-requisitos: Python 3.10+ e as dependências em `requirements.txt`.

```bash
pip install -r requirements.txt
```

A partir da raiz `tcc_coding_files/`:

```bash
# Adequação de tom — ToneCal PT-BR
python tcc2/algorithms/adequacao_de_tom/run_tonecal_pipeline.py

# Consistência de marca — Writeprints + PCA + cosine
python tcc2/algorithms/consistência_de_marca/run_stylometric_similarity_project.py \
    --project-root .

# Empatia percebida — WASSA
python tcc2/algorithms/empatia/generate_empathy_scores_wassa.py

# Fluência — perplexidade GPT-2 PT-BR
#   (baixa ~510 MB do modelo na primeira execução)
python tcc2/algorithms/fluencia/entity_based_local_coherence.py
```

> Os *scripts* assumem que o *Corpus Resultante* (`data/generated_responses/`)
> existe localmente. Por questões de privacidade, esse diretório **não**
> acompanha este repositório; está disponível mediante solicitação ao autor
> para fins acadêmicos.

## O que **não** está aqui

Para preservar privacidade e propriedade da informação:

| Não disponibilizado | Motivo |
|---|---|
| `data/expanded/` — comentários reais coletados | LGPD / dados de terceiros |
| `data/generated_responses/` — respostas geradas | Mediante solicitação |
| Avaliações individualizadas com texto completo | Decorrente do item acima |
| Código de chamada às *APIs* das LLMs | Depende de credenciais privadas |

## Citação

Caso utilize estes materiais, por favor cite:

```
DA SILVA, D. B. Engenharia de Prompts para Respostas de Restaurantes em
Português: Avaliação de Tom, Empatia e Consistência de Marca com LLMs.
Manaus: Universidade do Estado do Amazonas, 2026. Trabalho de Conclusão
de Curso.
```

## Contato

Para acesso aos *corpora* ou dúvidas sobre o experimento, consulte o
endereço fornecido na monografia.
