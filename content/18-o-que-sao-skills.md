# 18 - O que são Skills

No [capítulo 17](17-o-que-e-uma-tool.md) vimos que uma **tool** dá ao agent uma **ação**: uma função que roda de verdade — buscar na web, mandar um e-mail, rodar um cálculo. A tool é a **mão**. Agora vamos ao complemento: as **skills**, que são o **manual**. Uma tool sabe *fazer* uma coisa; uma skill sabe *como* uma tarefa deve ser feita direito. São peças diferentes que se encaixam, e confundir as duas é o erro número um de quem começa.

## A ideia: um módulo de know-how que entra sob demanda

Uma **skill** é um **módulo de instruções e recursos** — um passo a passo, exemplos, templates, uma checklist — que o agent **carrega para dentro do seu contexto quando a tarefa combina** com aquele módulo.

Repare na palavra **carrega**. Uma skill não é código que executa. É texto especializado que entra na "memória de trabalho" do modelo (a janela de contexto, [capítulo 06](06-o-que-e-janela-de-contexto.md)) no momento em que ele vai precisar. Antes disso, ela fica guardada, sem ocupar espaço.

Uma skill típica reúne quatro coisas, empacotadas com um nome:

- **Um procedimento** — "faça nesta ordem: primeiro isto, depois aquilo".
- **Exemplos** — casos já resolvidos, do jeito certo (é o mesmo princípio do *few-shot*, [capítulo 10](10-few-shot-e-chain-of-thought.md)).
- **Templates** — modelos prontos para preencher (um formato de e-mail, a estrutura de um laudo).
- **Uma checklist** — o que conferir antes de dar a tarefa por concluída.

## Tool vs. Skill: a diferença que importa

Essa distinção é o coração do capítulo, então vamos deixá-la nítida numa tabela:

| | **Tool** | **Skill** |
|---|---|---|
| O que é | Código que **executa** uma ação | Instruções + recursos que **ensinam** a fazer |
| Metáfora | A **mão** que age | O **manual** de como agir |
| Onde vive | Fora do modelo (roda no sistema) | **Dentro do contexto** do modelo (ele lê) |
| O que entrega | Um resultado concreto (um dado, um arquivo) | Conhecimento de **como** fazer bem |
| Exemplo | `gerar_pdf(html)` — vira um PDF | "revisar-contrato" — como revisar passo a passo |

O resumo de bolso: **a tool faz, a skill orienta.** E elas trabalham juntas. Uma skill de "gerar relatório" pode, lá no meio do procedimento, mandar o agent *usar* a tool `gerar_pdf`. A skill é a receita; a tool é o fogão. Você precisa das duas para o jantar sair.

## Por que não jogar tudo no prompt e pronto?

Aqui está o problema que as skills resolvem. Imagine que seu agent precisa saber fazer dez tarefas especializadas: revisar contrato, montar relatório financeiro, responder ticket de suporte, formatar um post... A tentação do iniciante é escrever **todas** as instruções de uma vez no prompt principal.

Isso quebra por dois motivos. Primeiro, **custa caro**: cada token no prompt é pago em toda chamada ([capítulo 05](05-o-que-sao-tokens.md)), e você estaria mandando o manual de revisão de contrato mesmo quando o usuário só quer formatar um post. Segundo, **confunde o modelo**: um prompt gigante com dez procedimentos misturados dilui a atenção — o modelo se perde no meio de instruções que não têm nada a ver com a tarefa da vez.

A saída tem um nome: **progressive disclosure** (divulgação progressiva). Em vez de despejar tudo, o agent enxerga só um **índice** — uma lista curta de skills, cada uma com um nome e uma frase de "quando me usar". Ele lê esse cardápio, percebe qual skill combina com o pedido e **abre só aquela**. As outras nove continuam fechadas.

```
        ┌───────────────────────────────────────────┐
        │   AGENT — prompt base (enxuto)            │
        │   + ÍNDICE de skills disponíveis:         │
        │     · revisar-contrato — quando há contrato
        │     · relatorio-financeiro — fechar o mês  │
        │     · responder-ticket — suporte           │
        └───────────────────────────────────────────┘
                        │
          chegou um contrato? abre só ▼
        ┌───────────────────────────────────────────┐
        │   SKILL: revisar-contrato                 │
        │   ├─ procedimento.md   (passo a passo)     │
        │   ├─ exemplos/         (contratos revisados)
        │   ├─ modelo-parecer.md (template)          │
        │   └─ checklist.md      (o que conferir)    │
        └───────────────────────────────────────────┘
```

*(O diagrama acima é uma ilustração da ideia, não a estrutura exata de nenhuma ferramenta específica.)*

## Um exemplo concreto: a skill "revisar-contrato"

Digamos que você trabalha num escritório e sempre revisa contratos do mesmo tipo. Você cria uma skill assim:

- **Nome**: `revisar-contrato`.
- **Quando carregar**: "quando o usuário anexar ou colar um contrato para análise".
- **Procedimento**: "1) Identifique as partes e o objeto. 2) Cheque prazo, valor e multa. 3) Marque cláusulas de rescisão e foro. 4) Sinalize qualquer termo fora do padrão da casa. 5) Escreva o parecer no modelo."
- **Exemplos**: dois contratos já revisados, mostrando o nível de detalhe esperado.
- **Template**: `modelo-parecer.md`, com as seções do parecer na ordem certa.
- **Checklist**: "conferiu multa? conferiu foro? apontou os riscos em vermelho?".

No dia a dia, você manda: *"revisa esse contrato pra mim"* e anexa o arquivo. O agent percebe que o assunto bate com `revisar-contrato`, **carrega a skill inteira** e segue o manual — aplica o procedimento, se espelha nos exemplos, preenche o template e roda a checklist antes de te entregar. Você não reexplicou nada. E quando, no mesmo dia, você pedir para ele resumir um e-mail, essa skill nem aparece: o contexto fica limpo para a outra tarefa.

## Por dentro

Por baixo do capô, uma skill é simplesmente **injeção de instruções especializadas no contexto, sob demanda**. Quando o agent "carrega" a skill `revisar-contrato`, o que acontece de concreto é: o texto daquele procedimento, dos exemplos e do template é **colado dentro da janela de contexto** antes do modelo gerar a resposta. É isso. Nada mais mágico do que isso.

Duas consequências valem ouro para não criar expectativa errada:

1. **O modelo não é re-treinado.** Carregar uma skill **não muda os pesos** do modelo, não o ensina permanentemente nada. Muda apenas o que ele **lê naquele momento**. Feche a conversa e a skill "desaparece" — ela não vira parte do modelo. É o mesmo mecanismo do *in-context learning* que vimos no [capítulo 10](10-few-shot-e-chain-of-thought.md): o modelo aprende a fazer a tarefa **lendo** o exemplo ali na hora, não estudando para uma prova.

2. **O poder está no texto, e o texto tem que ser bom.** Como a skill é literalmente instrução que o modelo lê, uma skill **mal escrita** — ambígua, contraditória, prolixa — não ajuda: atrapalha. Ela ocupa contexto e ainda empurra o modelo na direção errada. Skill boa é objetiva, na ordem certa, com exemplos que não deixam dúvida.

## Limites honestos

Vale a franqueza: **skill é um conceito mais novo e menos padronizado que tool.** Ferramentas de tool já têm formatos bem estabelecidos; skills, não. Cada plataforma implementa a ideia à sua maneira e com nomes diferentes — umas chamam de "skills", outras de "capabilities", "extensions", "playbooks". Se você trocar de ferramenta, o nome e os detalhes mudam. O **conceito** — empacotar know-how reutilizável e carregar sob demanda — é que se mantém em todas.

E há um limite que nenhuma skill apaga: no fim, tudo depende de o **modelo seguir** as instruções. A skill entrega o manual perfeito; ainda assim, um modelo mais fraco pode pular um passo ou "esquecer" a checklist no meio de uma tarefa longa. Skill aumenta muito a chance de acerto — não é uma garantia de obediência.

## Exercício

Pense em uma tarefa que você faz repetidamente e sempre do mesmo jeito (montar um e-mail padrão, formatar um documento, fechar um relatório).

1. Dê um **nome** à skill e escreva a frase de **quando carregar** ("use esta skill quando...").
2. Liste o **procedimento** (o passo a passo) e diga que **recursos** ela levaria junto (templates, exemplos, checklist).
3. Para fixar a diferença do capítulo, classifique cada caso abaixo como **tool** ou **skill** — e justifique em uma linha:
   - (a) Uma função que envia uma mensagem no WhatsApp.
   - (b) Um guia de "como escrever a mensagem de cobrança educada da empresa".
   - (c) Um programinha que converte uma planilha em gráfico.

---

<div align="center">

[« 17 - O que é uma Tool](17-o-que-e-uma-tool.md) — [Índice](../README.md#roadmap) — [19 - Arquitetura básica de Agents »](19-arquitetura-basica-de-agents.md)

</div>
