# 16 - O que é um Agent

Até aqui, você viu o modelo de linguagem (LLM) como uma máquina de **pergunta → resposta**. Você manda um texto, ele te devolve outro texto. Simples assim.

Um **agent** é um passo além disso. Em vez de só responder, ele recebe um **objetivo** e **age em passos** para alcançá-lo, tomando decisões pelo caminho.

## Chatbot simples vs. Agent

Vamos comparar os dois lado a lado.

**Chatbot simples:**

```text
Você:   "Qual a capital da França?"
Chatbot: "Paris."
```

Uma pergunta, uma resposta. Acabou. O chatbot só sabe o que estava na memória dele (o que foi treinado).

**Agent:**

```text
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

*(Trace ilustrativo — o formato é real, os textos são inventados para o exemplo.)*

Repare a diferença: o agent **não respondeu de cara**. Ele quebrou o objetivo em passos, foi atrás de informação que não tinha e só então respondeu.

## O loop: pensar → agir → observar → repetir

O coração de um agent é um **loop**. Ele fica girando até concluir a tarefa:

```text
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

### Esse padrão tem nome: ReAct

Alternar "pensar" e "agir" não é um truque solto — é um padrão bem conhecido, chamado **ReAct**, de *Reasoning + Acting* (raciocinar e agir intercalados). A ideia central é simples e poderosa:

> Em vez de o modelo tentar planejar tudo de uma vez no escuro, ele dá **um passo de raciocínio**, **uma ação**, **observa o resultado** — e só então decide o próximo passo com base no que realmente aconteceu.

Por que isso funciona tão bem? Porque o modelo **ajusta o plano à realidade**. Se a busca voltou vazia, ele percebe na hora e tenta outro termo. Se o resultado contradiz o que ele esperava, ele corrige a rota. Um plano feito de cara, sem ver nenhum resultado, erra assim que o mundo não coincide com o palpite inicial. O ReAct evita isso porque cada decisão é tomada já sabendo o que a anterior produziu.

### O "agir" é, na prática, uma chamada de ferramenta

Falamos em "agir" de forma abstrata, mas vale ser concreto sobre o mecanismo real. Quando o agent decide agir, o LLM não sai executando nada sozinho: ele **emite uma chamada de ferramenta** (*tool call*) — um pedido estruturado do tipo "execute `busca_web` com o argumento `filme mais assistido`". Quem realmente roda essa busca é o código ao redor (o sistema que hospeda o agent). O resultado volta e é **colocado de novo no contexto** do modelo — isso é o "observar".

Ou seja, no loop ReAct:

- **agir** = o modelo emitir uma *tool call*;
- **observar** = o resultado dessa tool voltar para o contexto, para o modelo ler.

É exatamente essa mecânica de *tool call* que veremos em detalhe no [capítulo 17](17-o-que-e-uma-tool.md).

## O que dá autonomia: as Tools

Sozinho, um LLM só sabe gerar texto. Ele não consulta a internet, não lê seus arquivos, não roda contas de verdade.

O que permite o agent **agir** são as **tools** (ferramentas). Uma tool é uma capacidade que você dá ao agent: buscar na web, ler um arquivo, chamar uma API, rodar um cálculo. Cada "AGIR" do loop é, na prática, o agent chamando uma tool.

Sem tools, um agent é só um chatbot pensando em voz alta. Com tools, ele consegue mexer no mundo de verdade. Vamos ver tools em detalhe no próximo capítulo.

## Por dentro: o loop é re-chamar o LLM com o histórico crescendo

Aqui está o ponto que desfaz toda a mágica. Cada volta do loop é, **literalmente, uma nova chamada ao mesmo LLM** — não existe um "cérebro" rodando por trás entre os passos. O que muda de uma volta para a outra é só uma coisa: **o histórico enviado ao modelo cresce**.

A cada volta, o sistema monta um texto que contém:

- o **objetivo** original,
- todas as **ações passadas** que o agent tomou,
- os **resultados** (observações) de cada uma delas,

e pergunta ao modelo: "diante disso tudo, qual o próximo passo?". O LLM responde com a próxima ação. O sistema executa, **anexa** o resultado ao histórico e chama o modelo **de novo** — agora com um histórico um pouco maior. E assim por diante.

```text
Chamada 1:  [objetivo]
            → modelo responde: AGIR busca_web(...)

Chamada 2:  [objetivo] + [ação 1] + [resultado 1]
            → modelo responde: AGIR busca_web(...)

Chamada 3:  [objetivo] + [ação 1] + [resultado 1] + [ação 2] + [resultado 2]
            → modelo responde: CONCLUIR + resposta final
```

*(Ilustração do que entra em cada chamada — não é a saída literal de um sistema real.)*

Três consequências práticas caem direto dessa estrutura:

1. **Custa mais.** Uma tarefa não é uma chamada, são **várias** — uma por passo. E cada chamada carrega o histórico inteiro (que só cresce), então você paga tokens repetidos a cada volta. É por isso que um agent é sensivelmente mais caro que uma pergunta única a um chatbot. Reveja o peso disso no [capítulo 05](05-o-que-sao-tokens.md) e no [capítulo 28](28-custos-e-escalabilidade.md).
2. **O histórico pode encher a janela.** Como o contexto só cresce a cada passo, uma tarefa longa pode estourar a **janela de contexto** ([capítulo 06](06-o-que-e-janela-de-contexto.md)) — e aí o agent começa a "esquecer" os primeiros passos.
3. **Precisa de uma condição de parada.** Nada garante sozinho que o loop termina. O sistema precisa de uma regra explícita: parar quando o **objetivo foi cumprido** ou quando bater um **número máximo de passos**. Sem isso, um agent confuso pode rodar para sempre (e queimar dinheiro).

## Exemplos de agents

Para deixar concreto, alguns tipos comuns:

- **Agent de pesquisa**: recebe uma pergunta, busca em várias fontes na web, lê os resultados e te entrega um resumo com as informações reunidas.
- **Agent que mexe em arquivos**: você pede "organize esta pasta" e ele lista os arquivos, decide categorias, cria pastas e move cada arquivo.
- **Assistente de código** (como este aqui): recebe "conserte esse bug", procura no código, lê os arquivos relevantes, edita o que for preciso e roda os testes para conferir.

Em todos eles, o padrão é o mesmo: um objetivo grande, quebrado em passos ReAct, com tools sendo chamadas a cada passo.

## Por baixo, ainda é um LLM (e por isso erra)

Apesar de parecer "inteligente e autônomo", é importante fixar: **por baixo de tudo, ainda é um LLM decidindo o próximo passo**. Não há planejamento infalível, não há garantia. É o mesmo modelo do [capítulo 04](04-como-o-chatgpt-funciona.md) prevendo texto — só que o texto que ele prevê agora é "qual ferramenta chamar em seguida".

Isso explica direto as **limitações**:

- ele **pode errar** o passo, escolher uma **ação ruim** ou chamar a tool errada;
- pode **entrar em loop**, repetindo a mesma ação sem progredir (por isso o limite de passos existe);
- pode "achar" que terminou sem ter terminado, ou insistir num caminho que não leva a lugar nenhum.

O ReAct e as tools tornam o agent muito mais capaz que um chatbot — mas não o tornam confiável por mágica. Continua sendo um modelo de probabilidade decidindo, passo a passo, o que fazer.

## Exercício

Pense em uma tarefa do seu dia a dia que **não** dá para resolver com uma única pergunta a um chatbot — algo que exige ir buscar informação ou fazer várias etapas.

1. Escreva o **objetivo** em uma frase.
2. Liste, em passos, o ciclo **pensar → agir → observar** (o padrão ReAct) que um agent seguiria para resolver.
3. Para cada "agir", anote qual **tool** o agent precisaria ter (buscar na web? ler arquivo? chamar uma API?) — lembrando que, por baixo, cada "agir" é uma *tool call*.
4. Defina uma **condição de parada**: como o agent saberia que terminou? E qual seria um número máximo de passos razoável para essa tarefa não rodar para sempre?

Guarde sua lista de tools: ela vai fazer sentido no próximo capítulo.

---

<div align="center">

[« 15 - O que é Banco Vetorial](15-o-que-e-banco-vetorial.md) — [Índice](../README.md#roadmap) — [17 - O que é uma Tool »](17-o-que-e-uma-tool.md)

</div>
