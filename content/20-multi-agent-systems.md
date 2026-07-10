# 20 - Multi-Agent Systems

No [capítulo 19](19-arquitetura-basica-de-agents.md) montamos **um** agent: um modelo num loop, com um objetivo e um punhado de [tools](17-o-que-e-uma-tool.md). Ele resolve muita coisa sozinho. Mas às vezes a tarefa é grande demais, ou pede papéis que brigam entre si (quem escreve empolgado x quem revisa desconfiado). Aí entra a ideia dos **multi-agent systems** (sistemas multi-agente): em vez de um faz-tudo, **vários agents especializados**, cada um com um papel.

Adianto a moral da história, porque ela é o coração deste capítulo: **na maioria dos casos você NÃO precisa disso.** Um agent bom com boas tools resolve. Multi-agente é uma ferramenta cara, e a maior parte deste capítulo é sobre quando ela paga o próprio custo — e quando é só hype.

## A ideia: um time com funções

A analogia é um **time de pessoas**. Uma redação de jornal não tem uma pessoa fazendo tudo: tem quem **apura** (pesquisa), quem **escreve**, quem **edita/revisa** e quem **coordena** a pauta. Cada um tem um foco e um jeito de trabalhar, e o texto final sai melhor do que se uma pessoa só corresse atrás de tudo ao mesmo tempo.

Com agents é igual. Você dá a cada agent um **papel** e um prompt próprio pra aquele papel:

- **Planejador** — quebra a tarefa em passos.
- **Pesquisador** — busca informação (tools de busca, leitura de arquivo).
- **Escritor** — transforma o material em texto.
- **Crítico/revisor** — procura erro, aponta o que melhorar.

O ganho não é mágica do modelo: é **foco**. Um prompt curto e específico ("seu único trabalho é achar erros factuais neste texto") costuma render melhor que um prompt gigante pedindo pra mesma instância pesquisar, escrever e revisar de uma vez.

## Padrões de coordenação

Ter vários agents não adianta se eles não se organizam. Existem três arranjos clássicos — e a diferença entre eles é **quem fala com quem**.

### 1. Orquestrador + trabalhadores

Um agent **orquestrador** (o "gerente") recebe a tarefa grande, quebra em pedaços e **distribui** para agents **trabalhadores**. Cada um devolve seu resultado, e o orquestrador **junta tudo** numa resposta só. Bom quando os pedaços são **independentes** e podem rodar em paralelo.

```
                 ┌──────────────────┐
       tarefa ──►│   ORQUESTRADOR   │◄── junta os resultados
                 └──┬─────┬─────┬───┘
          divide &  │     │     │
          distribui │     │     │
             ┌──────┘     │     └──────┐
             ▼            ▼            ▼
      ┌───────────┐┌───────────┐┌───────────┐
      │Trabalhador││Trabalhador││Trabalhador│
      │ (busca A) ││ (busca B) ││ (busca C) │
      └───────────┘└───────────┘└───────────┘
```

### 2. Pipeline (linha de montagem)

Os agents ficam **em sequência**. A **saída de um é a entrada do próximo** — como numa fábrica. Bom quando os passos têm ordem natural e cada etapa depende da anterior.

```
 ┌──────────┐   texto   ┌──────────┐  rascunho  ┌──────────┐
 │ Pesquisa │ ────────► │ Escritor │ ─────────► │ Revisor  │ ──► resultado
 │  (dados) │           │ (redige) │            │ (corrige)│
 └──────────┘           └──────────┘            └──────────┘
```

### 3. Crítico / debate

Um agent **produz**, outro **critica** e manda melhorar. O primeiro corrige, o crítico olha de novo. Um loop de "autor x editor" que roda algumas rodadas até ficar bom (ou até bater um limite de tentativas — senão ficam de conversa fiada gastando [tokens](05-o-que-sao-tokens.md) pra sempre).

```
 ┌──────────┐   rascunho    ┌──────────┐
 │  Autor   │ ────────────► │ Crítico  │
 │          │ ◄──────────── │          │
 └──────────┘  "melhore X,  └──────────┘
                erro em Y"    (repete N vezes)
```

## Comunicação: eles trocam mensagens

O que "liga" os agents é **texto**. Um agent produz uma saída (uma pesquisa, um rascunho, uma lista de problemas), e essa saída **entra no contexto do outro** como mais uma mensagem. Não há telepatia nem memória compartilhada mágica: o pesquisador entrega um texto, e esse texto vira parte do prompt do escritor. O orquestrador é quem costura — decide o que mandar pra quem e junta o que volta.

## Exemplo: uma pesquisa em três papéis

Tarefa: *"Escreva um resumo confiável sobre os riscos de segurança de senhas fracas."* Um pipeline de três agents (ilustrativo, pra você ver o fluxo):

```
[Agent A — Pesquisador]
   tool: busca na web
   saída: 5 fontes + trechos citados
        │
        ▼   (a saída de A vira a entrada de B)
[Agent B — Escritor]
   recebe os trechos de A
   saída: rascunho de 2 parágrafos
        │
        ▼   (o rascunho de B vai pra C junto das fontes de A)
[Agent C — Revisor]
   confere: cada afirmação bate com as fontes?
   saída: "parágrafo 2 exagera; a fonte 3 não diz isso" ──► volta pro B corrigir
```

Repare no ganho real: o **Revisor** tem um prompt que só pensa em "isto está sustentado pelas fontes?". Ele não está apaixonado pelo texto, porque não foi ele que escreveu — e por isso pega exageros que o escritor deixaria passar. Essa é a intuição por trás de separar papéis.

## Por dentro

Aqui está a parte desmistificadora. **Não existe tecnologia nova em "multi-agente".** Cada "agent" é exatamente o que você viu no [capítulo 19](19-arquitetura-basica-de-agents.md): uma **instância de LLM + um prompt de papel + tools**, rodando seu loop. "Multi-agente" é só **orquestrar várias dessas instâncias** e passar a saída de uma pra outra.

```
UM AGENT (cap. 19):
   [ LLM ] + [ prompt/papel ] + [ tools ] ──► loop até terminar

MULTI-AGENTE:
   Agent 1 ─► (saída vira mensagem) ─► Agent 2 ─► ... ─► Agent N
   \_________________ cada um é o bloco de cima ________________/

   Quem chama quem, em que ordem e o que passar adiante
   é código NORMAL que VOCÊ escreve — não é o modelo se
   auto-organizando por mágica.
```

Ou seja: a "inteligência de time" não está dentro do modelo. Está na **fiação** que você monta em volta — chamadas de API comuns, texto entrando e saindo. Entender isso te protege do hype: multi-agente é **organização**, não um poder novo do modelo.

## Os custos honestos (leia isto antes de se empolgar)

Cada agent é **pelo menos uma** chamada ao modelo — e agents em loop ou em debate são **várias**. Isso tem preço real:

- **Tokens/custo explodem.** Onde um agent gastava, digamos, 3 chamadas, um time de 4 agents com revisão pode gastar 15, 20. O contexto ainda é repassado de um pro outro, inflando cada chamada. Isso vira dinheiro rápido — veja o [capítulo 28](28-custos-e-escalabilidade.md).
- **Mais lento.** Pipeline é sequencial: você espera A, depois B, depois C. A troca de mensagens tem seu próprio custo de tempo.
- **Mais pontos de falha.** Se o Pesquisador traz um fato errado, o Escritor escreve em cima dele e o Revisor pode não pegar. **Um agent erra e contamina os outros** — o erro vira "verdade" no contexto de quem vem depois.
- **Coordenação é difícil.** Quem decide quando parar? E se dois discordam? Você acaba escrevendo lógica de gente-grande pra mediar máquinas.

A regra, alinhada com o princípio *boring technology*: **comece com um agent só, com boas tools.** Na dúvida, ele resolve. Só vá pra multi-agente quando o problema **realmente pedir**, e os bons motivos são poucos:

- **Especialização** que um prompt só não dá conta — papéis tão diferentes que juntá-los num prompt piora o resultado (ex.: autor x crítico adversarial).
- **Paralelismo** que corta tempo de verdade — partes independentes rodando ao mesmo tempo.

Fora disso — tarefa simples, linear, orçamento apertado, ou quando você quer o mínimo de coisas dando errado — um agent bem-feito ganha. Nunca vá pra multi-agente por hype, nem porque "parece mais avançado".

## Exercício

Pegue uma tarefa que pareça pedir vários papéis (ex.: *"pesquisar, escrever e revisar um artigo de blog"*).

1. Liste os **papéis** de agents que ela teria (ex.: pesquisador, escritor, crítico).
2. Escolha **um padrão** de coordenação (orquestrador, pipeline ou crítico/debate) e justifique por que ele encaixa melhor nesta tarefa.
3. Desenhe o **fluxo em texto**, como os diagramas acima — mostre o que cada agent recebe e o que entrega.
4. Estime, por alto, **quantas chamadas ao modelo** o seu desenho faria contra **um agent só**. Onde o custo cresce?
5. A pergunta que separa engenharia de hype: **dava pra fazer com um agent só e boas tools?** Se sim, faça — e guarde o multi-agente pro dia em que a tarefa realmente exigir.

---

<div align="center">

[« 19 - Arquitetura básica de Agents](19-arquitetura-basica-de-agents.md) — [Índice](../README.md#roadmap) — [21 - O que é MCP »](21-o-que-e-mcp.md)

</div>
