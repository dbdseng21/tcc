# TCC — Comparação de LLMs para Geração de Respostas a Comentários de Restaurante

Projeto de TCC que compara 3 LLMs (GPT-4, Gemini, Llama3) na geração de respostas a comentários de clientes do restaurante Coco Bambu Manaus, avaliando com 4 métricas: adequação de tom, consistência de marca, empatia percebida e fluência.

## Estrutura do Projeto

```
tcc_coding_files/
├── data/
│   ├── raw/                        # Comentários originais coletados (~19 cada)
│   ├── expanded/                   # Comentários expandidos para 100 cada
│   └── generated_responses/        # Respostas geradas pelos 3 LLMs (8 arquivos × 100 comentários)
│
├── tcc1/                           # Agentes LLM para geração de respostas
│   ├── main.py                     # Ponto de entrada
│   └── src/
│       ├── config.py               # Configurações
│       ├── execute.py              # Orquestrador de execução
│       ├── llm/                    # Implementações dos modelos (GPT-4, Gemini, Llama3)
│       ├── metrics/                # ROUGE score
│       └── prompt_engineering/     # Gerenciador de prompts
│
├── tcc2/algorithms/                # Métricas de avaliação
│   ├── adequacao_de_tom/           # Politeness Score (rubric-based, 7 dimensões)
│   ├── consistencia_de_marca/      # Stylometric Similarity (Writeprints + PCA + cosine)
│   ├── empatia/                    # Perceived Empathy (simulação de 7 avaliadores, Likert 1-5)
│   └── fluencia/                   # Fluência via perplexidade GPT-2 português
│
├── results/                        # Resultados das métricas
│   ├── politeness_score/           # Resultados de adequação de tom
│   ├── stylometric_similarity/     # Resultados de consistência de marca
│   ├── perceived_empathy/          # Resultados de empatia percebida
│   ├── fluency/                    # Resultados de fluência (perplexidade)
│   └── legacy/                     # Resultados antigos (ROUGE, BERTScore)
│
├── prompts/                        # Prompts utilizados por modelo e estratégia
│   ├── gpt/                        # Prompts para GPT-4
│   ├── gemini/                     # Prompts para Gemini
│   └── llama3/                     # Prompts para Llama3
│
├── docs/                           # Análises e documentação
│   ├── Métricas.xlsx               # Planilha de métricas
│   └── analise_completa_*.md       # Análises consolidadas
│
└── requirements.txt
```

## Variáveis do Experimento

| Variável | Valores |
|---|---|
| **Modelo** | GPT-4, Gemini, Llama3 |
| **Persona** | 1 (sofisticada e formal), 2 (acolhedora e informal) |
| **Estratégia** | zero-shot, few-shot |
| **Período** | before_llm_release, after_llm_release |

Total: 3 modelos × 2 personas × 2 estratégias × 2 períodos = **24 cenários**, cada um com 100 comentários.

## Executando as Métricas

Todas executadas a partir da raiz do projeto:

```bash
# Adequação de Tom (Politeness Score)
python tcc2/algorithms/adequacao_de_tom/politeness_score_metric.py run \
  --project-root . --output-dir results/politeness_score

# Consistência de Marca (Stylometric Similarity)
python tcc2/algorithms/consistência_de_marca/run_stylometric_similarity_project.py \
  --project-root .

# Empatia Percebida (3 etapas)
python tcc2/algorithms/empatia/perceived_empathy_metric.py build-template \
  --project-root . --output results/perceived_empathy/empathy_template.csv
python tcc2/algorithms/empatia/simulate_evaluators.py \
  --template results/perceived_empathy/empathy_template.csv \
  --output results/perceived_empathy/empathy_evaluations.csv
python tcc2/algorithms/empatia/perceived_empathy_metric.py summarize \
  --annotated-csv results/perceived_empathy/empathy_evaluations.csv \
  --output-dir results/perceived_empathy

# Fluência (Perplexidade GPT-2) — baixa modelo ~510MB na primeira execução
python tcc2/algorithms/fluencia/entity_based_local_coherence.py
```

## Requisitos

```bash
pip install -r requirements.txt
```

Python 3.10+ recomendado. A métrica de fluência requer `torch` e `transformers`.
