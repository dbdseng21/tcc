# tcc2_files

Materiais de reprodução do TCC2:

> **Engenharia de Prompts para Respostas de Restaurantes em Português:
> Avaliação de Tom, Empatia e Consistência de Marca com LLMs**
>
> Danilo Bruno da Silva — Universidade do Estado do Amazonas (UEA), 2026.

## Conteúdo

| Caminho | Descrição |
|---|---|
| `monografia_DaniloBrunoDaSilva_TCC_2.tex` | Fonte LaTeX da monografia |
| `sbc_monografia.bib`, `tcc2_catalogo_referencias.bib` | Referências bibliográficas |
| `img/`, `figuras_formatadas_fonte/` | Figuras utilizadas no documento |
| `forms_avaliadores.pdf` | Formulário de avaliação aplicado aos 15 avaliadores |
| `fig_desenho_experimental.pdf` | Diagrama do desenho experimental |
| `gerar_fig_desenho_experimental.py`, `gerar_figuras_fonte_grande.py`, `gerar_figuras_prompts_v2.py`, `enhance_image.py` | *Scripts* utilitários de geração de figuras |
| `tcc_coding_files/` | Código das métricas, *prompts*, escores e sumários — ver [README específico](tcc_coding_files/README.md) |

## Compilação

A monografia foi escrita em LaTeX, usando o modelo SBC. Para compilar:

```bash
pdflatex monografia_DaniloBrunoDaSilva_TCC_2.tex
biber monografia_DaniloBrunoDaSilva_TCC_2
pdflatex monografia_DaniloBrunoDaSilva_TCC_2.tex
pdflatex monografia_DaniloBrunoDaSilva_TCC_2.tex
```

## Reprodutibilidade

Os artefatos de reprodução (código das métricas, *prompts*, escores Likert
agregados e sumários estatísticos) estão em [`tcc_coding_files/`](tcc_coding_files/).
Consulte o README desse diretório para detalhes sobre o desenho experimental
e as instruções de execução.

## Licença e uso

Material acadêmico de propriedade do autor. Reprodução parcial autorizada
para fins acadêmicos, com a devida citação.
