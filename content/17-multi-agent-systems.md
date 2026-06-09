# 17 - Multi-Agent Systems

Até agora falamos de **um** agent resolvendo uma tarefa. Mas e se você juntar **vários** agents, cada um bom em uma coisa? É disso que tratam os **multi-agent systems** (sistemas multi-agente).

## A ideia: um time de especialistas

Um único agent tentando fazer tudo pode se atrapalhar — é muita coisa na cabeça ao mesmo tempo. A ideia do multi-agente é **dividir o trabalho** entre vários agents, cada um **especializado** numa parte.

A analogia mais fácil é um **time de pessoas**. Numa empresa, você não tem uma pessoa só fazendo tudo: tem quem pesquisa, quem escreve, quem revisa, quem gerencia. Cada um foca no que faz bem, e o resultado final sai melhor.

Com agents é igual: em vez de um "faz-tudo", você monta um time onde cada agent tem um **papel** e instruções próprias para aquele papel.

## Padrões comuns

Existem algumas formas clássicas de organizar esse time.

### Orquestrador + trabalhadores

Um agent **orquestrador** (o "gerente") recebe a tarefa grande, quebra em pedaços e **distribui** para agents **trabalhadores**. Quando eles terminam, o orquestrador junta os resultados.

```
                ┌──────────────────┐
                │   ORQUESTRADOR   │
                │   (o gerente)    │
                └───┬────┬────┬────┘
            divide  │    │    │  e distribui
          ┌─────────┘    │    └─────────┐
          ▼              ▼              ▼
   ┌────────────┐ ┌────────────┐ ┌────────────┐
   │ Trabalhador│ │ Trabalhador│ │ Trabalhador│
   │  (pesquisa)│ │  (escreve) │ │  (revisa)  │
   └────────────┘ └────────────┘ └────────────┘
```

### Pipeline / linha de montagem

Os agents ficam **em sequência**, como numa fábrica. A **saída de um vira a entrada do próximo**.

```
[Agent Pesquisa] ──► [Agent Redator] ──► [Agent Revisor] ──► resultado
   reúne dados        escreve texto       corrige erros
```

Cada agent faz sua etapa e passa adiante. Bom quando a tarefa tem passos bem definidos e em ordem.

### Especialistas que se revisam

Dois ou mais agents **conversam ou se criticam** para melhorar o resultado. Um produz, outro revisa e aponta problemas, o primeiro corrige. É como ter um autor e um editor trabalhando juntos.

```
[Agent Autor] ──► produz rascunho ──► [Agent Crítico]
       ▲                                     │
       └────── "melhore isto e aquilo" ◄─────┘
```

## Quando vale a pena (e quando não)

Multi-agente **parece** sempre melhor, mas não é. Use a cabeça.

**Vale a pena quando:**

- A tarefa é **grande** e dá para quebrar em partes bem definidas.
- As partes são **paralelizáveis** — vários agents podem trabalhar ao mesmo tempo, ganhando velocidade.
- A tarefa **precisa de revisão** ou de pontos de vista diferentes (alguém produz, alguém critica).
- Cada parte se beneficia de um **especialista** com instruções próprias.

**NÃO vale a pena quando:**

- A tarefa é **simples** — um único agent resolve de boa. Vários agents só adicionam complicação.
- Você não pode arcar com o **custo maior** — mais agents = mais chamadas ao modelo = mais dinheiro e mais tempo.
- Você quer poucos **pontos de falha** — quanto mais agents conversando, mais lugares onde algo pode dar errado (um passa informação errada, outro entende errado, e o erro se espalha).

## Prós e contras

Para fechar, a lista honesta:

**Prós:**

- Especialização: cada agent foca no que faz bem.
- Paralelismo: tarefas independentes rodam ao mesmo tempo.
- Revisão embutida: agents podem checar o trabalho uns dos outros.
- Modularidade: fica mais fácil entender e trocar uma parte.

**Contras:**

- **Mais custo**: várias chamadas ao modelo em vez de uma.
- **Mais complexidade**: coordenar vários agents é mais difícil que rodar um só.
- **Mais pontos de falha**: erro de um agent pode contaminar os outros.
- **Mais lento às vezes**: a coordenação e a troca de mensagens têm seu próprio custo de tempo.

A regra de ouro: **comece com um agent só**. Só parta para multi-agente quando a tarefa realmente pedir — e quando o ganho compensar o custo e a complicação a mais.

## Exercício

Escolha uma tarefa grande (ex: "escrever um artigo de blog pesquisado e revisado").

1. Quebre a tarefa em **papéis** de agents (ex: pesquisador, redator, revisor).
2. Escolha um **padrão** de organização (orquestrador, pipeline ou especialistas que se revisam) e justifique a escolha.
3. Desenhe o fluxo em texto (como os diagramas acima).
4. Liste **2 prós** e **2 contras** de resolver assim, em vez de usar um único agent.
5. Reflita: essa tarefa **realmente** precisava de vários agents, ou um só daria conta?

---

<div align="center">

[« 16 - Arquitetura básica de Agents](16-arquitetura-basica-de-agents.md) — [Índice](../README.md#roadmap) — [18 - O que é MCP »](18-o-que-e-mcp.md)

</div>
