# 15 - O que são Skills

Já vimos que uma **tool** é uma função que o agent chama para executar algo. Agora vamos para um conceito parecido, mas diferente: as **skills**.

## A ideia: capacidades empacotadas

Uma **skill** é uma **capacidade empacotada e reutilizável** que ensina o agent a fazer **bem** uma tarefa específica.

Pense assim: uma tool é uma ferramenta solta na bancada. Uma skill é um **kit completo** com um manual de instruções, materiais e, às vezes, ferramentas próprias — tudo organizado para uma tarefa específica.

Na prática, uma skill costuma ser um conjunto de:

- **Instruções** — um passo a passo de como fazer a tarefa direito.
- **Recursos** — modelos (templates), exemplos, tabelas de referência, regras de estilo.
- **Às vezes tools/scripts** — funções ou pequenos programas que ajudam na tarefa.

Tudo isso fica guardado junto, com um nome, pronto para o agent usar quando o assunto aparecer.

## Tool vs. Skill: qual a diferença?

Essa confusão é comum, então vamos deixar bem claro:

| | **Tool** | **Skill** |
|---|---|---|
| O que é | Uma função que **executa** algo | Um "manual" + recursos que **ensinam** a fazer algo |
| Analogia | A furadeira | O kit de montar o móvel (manual + parafusos + a furadeira) |
| O que entrega | Um resultado (um dado, um arquivo) | Conhecimento de **como** fazer a tarefa bem |
| Exemplo | `buscar_web(...)` | "Como escrever um relatório financeiro padrão da empresa" |

Resumindo: a **tool faz**, a **skill orienta** (e pode até incluir tools dentro dela). Uma skill bem-feita junta o conhecimento ("faça assim, nesta ordem, com este formato") com os recursos necessários para executar.

## Por que isso é útil

Empacotar capacidades em skills traz benefícios concretos:

- **Reuso**: escreveu uma vez como fazer um relatório? Toda vez que precisar, o agent puxa a mesma skill. Não precisa re-explicar.
- **Conhecimento especializado**: a skill carrega regras e detalhes que o agent não saberia sozinho (o formato exato que sua empresa usa, por exemplo).
- **Prompt principal enxuto**: você não precisa enfiar TODAS as instruções no prompt o tempo todo. As skills ficam guardadas e entram só quando necessário.
- **Carrega só quando precisa**: se a conversa é sobre relatórios, o agent carrega a skill de relatórios. Se é sobre outra coisa, ela fica de fora, economizando espaço e dinheiro.

Esse último ponto é importante. Em vez de o agent saber tudo de uma vez (o que deixaria o prompt gigante e caro), ele carrega o "manual" certo **na hora certa**.

```
        ┌──────────────────────────────────┐
        │         AGENT (prompt base)       │
        │   instruções gerais, enxutas      │
        └──────────────────────────────────┘
                        │
         assunto é "relatório"? carrega ▼
        ┌──────────────────────────────────┐
        │   SKILL: gerar-relatorio-pdf      │
        │   ├─ instrucoes.md                │
        │   ├─ template.html                │
        │   └─ gerar_pdf.py (script)        │
        └──────────────────────────────────┘
```

## Exemplo conceitual de uma skill

Imagine uma skill chamada **"gerar relatório PDF"**. Ela poderia conter:

- **Instruções** (um arquivo de texto): "Reúna os dados do mês, agrupe por categoria, preencha o template, gere o PDF e salve na pasta de relatórios."
- **Template** (`template.html`): o layout pronto do relatório, com logo e seções na ordem certa.
- **Script** (`gerar_pdf.py`): um programinha que pega o HTML preenchido e produz o arquivo PDF.

Quando você pede "me gera o relatório de maio", o agent percebe que o assunto é relatório, **carrega essa skill** e segue o manual: aplica as instruções, usa o template e roda o script. O resultado sai padronizado, do jeito certo, sem você precisar explicar nada disso de novo.

## Cada plataforma faz à sua maneira

Vale uma nota de honestidade: **skills não são um padrão único**. Diferentes ferramentas e plataformas de IA implementam essa ideia de formas parecidas, mas com nomes e detalhes diferentes — algumas chamam de "skills", outras de "capabilities", "extensions" ou coisa do tipo.

O conceito central, porém, é sempre o mesmo: **empacotar instruções + recursos reutilizáveis** para o agent fazer bem uma tarefa, carregando esse pacote só quando o assunto for relevante. Se você entendeu a ideia, vai reconhecê-la em qualquer plataforma, independente do nome.

## Exercício

Pense em uma tarefa que você faz de forma repetida e sempre do mesmo jeito (montar um e-mail padrão, formatar um documento, gerar um relatório).

1. Dê um **nome** à skill.
2. Liste as **instruções** (o passo a passo de como fazer a tarefa).
3. Liste os **recursos** que ela precisaria (templates, exemplos, tabelas).
4. Tem alguma parte que daria para virar um **script ou tool** dentro da skill? Qual?
5. Por fim: explique em uma frase por que essa skill deveria carregar **só quando o assunto aparece**, e não estar sempre no prompt.

---

<div align="center">

[« 14 - O que é uma Tool](14-o-que-e-uma-tool.md) — [Índice](../README.md#roadmap) — [16 - Arquitetura básica de Agents »](16-arquitetura-basica-de-agents.md)

</div>
