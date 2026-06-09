# 13 - O que é um Agent

Até aqui, você viu o modelo de linguagem (LLM) como uma máquina de **pergunta → resposta**. Você manda um texto, ele te devolve outro texto. Simples assim.

Um **agent** é um passo além disso. Em vez de só responder, ele recebe um **objetivo** e **age em passos** para alcançá-lo, tomando decisões pelo caminho.

## Chatbot simples vs. Agent

Vamos comparar os dois lado a lado.

**Chatbot simples:**

```
Você:   "Qual a capital da França?"
Chatbot: "Paris."
```

Uma pergunta, uma resposta. Acabou. O chatbot só sabe o que estava na memória dele (o que foi treinado).

**Agent:**

```
Você:   "Descubra qual foi o filme mais assistido na semana passada
         e me escreva um resumo da história dele."
Agent:  (pensa) Preciso de dados atuais. Vou buscar na web.
        (age)   busca_web("filme mais assistido semana passada")
        (observa) Resultado: "Filme X"
        (pensa) Agora preciso da sinopse do Filme X.
        (age)   busca_web("sinopse Filme X")
        (observa) Resultado: "..."
        (pensa) Tenho tudo. Vou escrever o resumo.
        "O filme mais assistido foi o Filme X. A história conta..."
```

Repare a diferença: o agent **não respondeu de cara**. Ele quebrou o objetivo em passos, foi atrás de informação que não tinha e só então respondeu.

## O loop: pensar → agir → observar → repetir

O coração de um agent é um **loop**. Ele fica girando até concluir a tarefa:

```
        ┌─────────────────────────────────┐
        │                                 │
        ▼                                 │
   1. PENSAR  ──►  2. AGIR  ──►  3. OBSERVAR
   (o que fazer    (executa uma  (lê o resultado
    agora?)         ação/tool)    da ação)
        ▲                                 │
        │                                 │
        └──── ainda não terminei? ────────┘
                      │
                      ▼
                  CONCLUIR
              (objetivo alcançado)
```

- **Pensar**: o LLM decide qual é o próximo passo.
- **Agir**: ele executa uma ação no mundo (buscar algo, ler um arquivo, calcular).
- **Observar**: ele lê o resultado da ação.
- **Repetir**: com a nova informação, ele pensa de novo. Isso continua até a tarefa estar pronta.

Esse ciclo é o que dá ao agent a aparência de estar "trabalhando" em algo, em vez de só cuspir uma resposta.

## O que dá autonomia: as Tools

Sozinho, um LLM só sabe gerar texto. Ele não consulta a internet, não lê seus arquivos, não roda contas de verdade.

O que permite o agent **agir** são as **tools** (ferramentas). Uma tool é uma capacidade que você dá ao agent: buscar na web, ler um arquivo, chamar uma API, rodar um cálculo. Cada "AGIR" do loop é, na prática, o agent chamando uma tool.

Sem tools, um agent é só um chatbot pensando em voz alta. Com tools, ele consegue mexer no mundo de verdade. Vamos ver tools em detalhe no próximo capítulo.

## Exemplos de agents

Para deixar concreto, alguns tipos comuns:

- **Agent de pesquisa**: recebe uma pergunta, busca em várias fontes na web, lê os resultados e te entrega um resumo com as informações reunidas.
- **Agent que mexe em arquivos**: você pede "organize esta pasta" e ele lista os arquivos, decide categorias, cria pastas e move cada arquivo.
- **Assistente de código** (como este aqui): recebe "conserte esse bug", procura no código, lê os arquivos relevantes, edita o que for preciso e roda os testes para conferir.

Em todos eles, o padrão é o mesmo: um objetivo grande, quebrado em passos, com tools sendo chamadas a cada passo.

## Por baixo, ainda é um LLM

Apesar de parecer "inteligente e autônomo", é importante entender: **por baixo de tudo, ainda é um LLM decidindo o próximo passo**.

Não existe mágica. A cada volta do loop, o sistema mostra ao modelo:

- o objetivo original,
- o que já foi feito,
- os resultados das ações anteriores,

e pergunta: "qual o próximo passo?". O LLM responde com a próxima ação. O sistema executa, junta o resultado e pergunta de novo.

Isso também explica as **limitações**: como é um LLM decidindo, o agent **pode errar**, escolher uma ação ruim, ou até **entrar em loop** repetindo a mesma coisa. E, como ele chama o modelo várias vezes (uma por passo), um agent **custa mais** que uma única pergunta a um chatbot. Vamos falar mais disso no capítulo de arquitetura.

## Exercício

Pense em uma tarefa do seu dia a dia que **não** dá para resolver com uma única pergunta a um chatbot — algo que exige ir buscar informação ou fazer várias etapas.

1. Escreva o **objetivo** em uma frase.
2. Liste, em passos, o ciclo **pensar → agir → observar** que um agent seguiria para resolver.
3. Para cada "agir", anote qual **tool** o agent precisaria ter (buscar na web? ler arquivo? chamar uma API?).

Guarde sua lista de tools: ela vai fazer sentido no próximo capítulo.

---

<div align="center">

[« 12 - O que é Banco Vetorial](12-o-que-e-banco-vetorial.md) — [Índice](../README.md#roadmap) — [14 - O que é uma Tool »](14-o-que-e-uma-tool.md)

</div>
