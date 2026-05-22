# Guia de Geração de Respostas LLM - Dataset 100 Comentários

## Estrutura dos Arquivos

### CSVs Template (em `generated_comments/`)
Cada arquivo tem a coluna `comment` preenchida + colunas vazias para Gpt4, Gemini e Llama3.

| # | Arquivo CSV | Período | Persona | Shot |
|---|------------|---------|---------|------|
| 1 | `coco_bambu_..._before_100_generated_responses_persona_1_zero_shot.csv` | before | Sofisticada e formal | zero_shot |
| 2 | `coco_bambu_..._before_100_generated_responses_persona_1_few_shot.csv`  | before | Sofisticada e formal | few_shot  |
| 3 | `coco_bambu_..._before_100_generated_responses_persona_2_zero_shot.csv` | before | Acolhedora e informal | zero_shot |
| 4 | `coco_bambu_..._before_100_generated_responses_persona_2_few_shot.csv`  | before | Acolhedora e informal | few_shot  |
| 5 | `coco_bambu_..._after_100_generated_responses_persona_1_zero_shot.csv`  | after  | Sofisticada e formal | zero_shot |
| 6 | `coco_bambu_..._after_100_generated_responses_persona_1_few_shot.csv`   | after  | Sofisticada e formal | few_shot  |
| 7 | `coco_bambu_..._after_100_generated_responses_persona_2_zero_shot.csv`  | after  | Acolhedora e informal | zero_shot |
| 8 | `coco_bambu_..._after_100_generated_responses_persona_2_few_shot.csv`   | after  | Acolhedora e informal | few_shot  |

### Prompts (em `prompts_for_llm/`)
```
prompts_for_llm/
  gpt/
    persona_1_zero_shot.txt   → Sofisticada formal, sem exemplos
    persona_1_few_shot.txt    → Sofisticada formal, com exemplos
    persona_2_zero_shot.txt   → Acolhedora informal, sem exemplos
    persona_2_few_shot.txt    → Acolhedora informal, com exemplos
  gemini/
    (mesmos 4 arquivos, com coluna alvo trocada para "Gemini Generated Response...")
```

---

## Passo a Passo

### PASSO 1: GPT-4 (ChatGPT)
Para cada um dos 8 CSVs:
1. Abra o ChatGPT (chat.openai.com)
2. Anexe o CSV template correspondente
3. Cole o prompt de `prompts_for_llm/gpt/` que corresponde à persona + shot do arquivo
4. Aguarde a resposta e baixe o CSV gerado
5. Substitua o arquivo original em `generated_comments/` pelo CSV baixado

**Combinações:**
| CSV (persona_1_zero_shot) | → Prompt: `gpt/persona_1_zero_shot.txt` |
| CSV (persona_1_few_shot)  | → Prompt: `gpt/persona_1_few_shot.txt`  |
| CSV (persona_2_zero_shot) | → Prompt: `gpt/persona_2_zero_shot.txt` |
| CSV (persona_2_few_shot)  | → Prompt: `gpt/persona_2_few_shot.txt`  |

Repita para os 4 CSVs de "before" e os 4 de "after" (mesmo prompt, CSV diferente).

### PASSO 2: Gemini
Para cada um dos 8 CSVs (já com a coluna Gpt4 preenchida):
1. Abra o Google AI Studio ou Gemini (gemini.google.com)
2. Anexe o CSV (que já tem as respostas do GPT)
3. Cole o prompt de `prompts_for_llm/gemini/` correspondente
4. Baixe o CSV e substitua em `generated_comments/`

### PASSO 3: Llama3 (eu rodo aqui)
Quando os 8 CSVs tiverem as colunas Gpt4 e Gemini preenchidas, me avise que eu rodo o Llama3 localmente para preencher a coluna restante.

---

## Mapeamento Persona ↔ Número
- **Persona 1** = Sofisticada e formal
- **Persona 2** = Acolhedora e informal
