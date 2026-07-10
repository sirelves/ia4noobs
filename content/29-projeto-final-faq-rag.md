# 29 - Projeto final: um assistente de FAQ com RAG

Chegou a hora de juntar tudo. Este capítulo não ensina um conceito novo — ele te guia a **construir um projetinho de ponta a ponta** usando o que você aprendeu: prompts, embeddings, RAG, escolha de modelo, custo e avaliação.

A meta: um **assistente que responde perguntas sobre os SEUS documentos** (o FAQ de um produto, as regras de um projeto, suas anotações). É o "Hello World" das aplicações de IA sérias — e, quando funciona, dá aquela sensação de "eu construí isso".

## O que vamos construir

```
PERGUNTA do usuário
      |
      v
[1] Quebrar seus documentos em pedaços (chunks) e virar embeddings
      |
      v
[2] Buscar os trechos mais parecidos com a pergunta (top-k)
      |
      v
[3] Montar um prompt: trechos + pergunta + regra anti-alucinação
      |
      v
[4] Chamar um LLM para responder com base SÓ nos trechos
      |
      v
RESPOSTA citando de qual documento veio
```

Isso é **RAG** (*Retrieval-Augmented Generation*): em vez de confiar na memória do modelo, você **entrega a fonte junto com a pergunta**. Se algum passo soou estranho, volte: embeddings ([cap. 13](13-o-que-sao-embeddings.md)), RAG ([cap. 14](14-o-que-e-rag.md)) e escolha de modelo ([cap. 07](07-escolhendo-o-modelo-certo.md)) são a base disto aqui.

## Passo a passo

### 1. Junte os documentos

Comece pequeno. Pegue de 3 a 10 textos sobre um assunto que você conhece — pode ser um FAQ, regras de um jogo, a documentação de uma ferramenta. Salve como arquivos de texto simples.

> Dica: qualidade > quantidade. Documento confuso gera resposta confusa ("lixo entra, lixo sai").

### 2. Quebre em pedaços (chunks)

Documentos grandes viram pedaços menores para a busca funcionar bem. Isso se chama **chunking** ([cap. 14](14-o-que-e-rag.md)), e o tamanho do pedaço é um **trade-off**:

- **Chunk grande** (uma página inteira): traz muito contexto, mas mistura vários assuntos — a busca fica imprecisa e o prompt fica caro em tokens.
- **Chunk pequeno** (uma frase): é preciso, mas pode cortar a informação no meio e perder o contexto.

Um bom começo é **um parágrafo ou algumas frases por pedaço**. Não existe número mágico: você vai ajustar isso depois, medindo (mais abaixo).

### 3. Gere embeddings e guarde

Cada pedaço vira um **embedding** — um vetor de números que representa o *significado* do texto ([cap. 13](13-o-que-sao-embeddings.md)). Guarde a lista de (pedaço, embedding). Para um projeto de estudo, uma lista na memória já serve — você **não precisa** de um banco vetorial de produção para começar.

O exemplo [`examples/rag-mini`](../examples/rag-mini) mostra exatamente essa parte, comentada linha a linha.

### 4. Busque os trechos certos (top-k)

Quando chega a pergunta: gere o embedding **dela** e compare com o embedding de cada pedaço usando **similaridade de cosseno** ([cap. 13](13-o-que-sao-embeddings.md)) — quanto mais próximos os vetores apontam para a mesma direção, mais parecidos os significados. Pegue os **k** trechos mais parecidos (o famoso **top-k**; comece com `k = 3`).

Buscar por *significado*, e não por palavra exata, é o pulo do gato: a pergunta "quanto custa o plano?" acha o trecho sobre "valores da assinatura" mesmo sem repetir nenhuma palavra.

### 5. Monte o prompt com grounding

Junte os trechos recuperados e a pergunta num prompt que **amarra o modelo à fonte** (*grounding*) e o proíbe de inventar ([cap. 26](26-seguranca-em-ia.md)):

```text
Responda a pergunta usando APENAS os trechos abaixo.
Se a resposta não estiver nos trechos, diga "não encontrei isso nos documentos".
Não use conhecimento externo.

Trechos:
{aqui entram os pedaços recuperados}

Pergunta: {a pergunta do usuário}
```

Aquele "diga que não encontrou" não é detalhe: é a sua principal defesa **anti-alucinação**. Sem ela, o modelo tende a preencher o vazio com um chute confiante.

Para a chamada ao modelo, o exemplo [`examples/chamar-api`](../examples/chamar-api) tem o esqueleto pronto. Prefere sem custo e sem chave? Troque pela versão local do [`examples/modelo-local`](../examples/modelo-local).

### 6. Mostre a fonte

Faça a resposta indicar **de qual documento/trecho** ela veio (basta guardar o nome do arquivo junto de cada pedaço e imprimi-lo no fim). Isso é o que separa um brinquedo de algo confiável: a pessoa pode **conferir** — e você também, quando ele errar.

## Como saber se ficou bom

"Parece que funciona" não é medida. Antes de sair ajustando, monte um **mini-eval** ([cap. 27](27-como-avaliar-respostas-de-ia.md)): um conjunto fixo de **5 a 10 perguntas** com a resposta que você espera. Exemplo:

```text
Pergunta                                  | Resposta esperada
------------------------------------------|----------------------------------
Qual o prazo de garantia?                 | 12 meses
O plano Pro tem quantos usuários?         | Até 5
Vocês entregam no exterior?               | (NÃO está nos docs → deve admitir)
```

Repare na terceira linha: **inclua de propósito perguntas cuja resposta NÃO está nos documentos**. O comportamento certo ali é o assistente dizer "não encontrei isso nos documentos" — e não inventar. Um RAG que acerta as fáceis mas *alucina* nas que não sabe é pior que inútil: é enganoso.

Rode as perguntas, conte quantas ele acertou, anote. Agora você tem um **número**. Mudou o tamanho do chunk, o `k` ou o prompt? Rode de novo e compare. Isso transforma "achismo" em "essa mudança subiu de 6 para 8 acertos".

## Checklist de pronto

Considere o projeto ok quando ele:

- [ ] **Responde certo** quando a informação existe nos documentos.
- [ ] **Admite que não sabe** quando a informação não existe (não inventa).
- [ ] **Cita a fonte** (qual documento/trecho embasou a resposta).
- [ ] **Passou no mini-eval** (você mediu, não só "achou bom").

Bateu os quatro? Você tem um assistente de FAQ com RAG de verdade — feio, talvez, mas honesto e funcionando.

## Evoluções (quando o básico funcionar)

- Trocar a lista na memória por um **banco vetorial** de verdade ([cap. 15](15-o-que-e-banco-vetorial.md)) — necessário quando os documentos crescem.
- Transformar em um **agent** que decide quando buscar e quando responder direto ([cap. 16](16-o-que-e-um-agent.md)).
- Expor os documentos via **MCP** para outra IA usar como ferramenta ([cap. 21](21-o-que-e-mcp.md)).
- Colocar uma interface simples (web ou chat) na frente.

## Seja honesto: os limites

- **Não vai ficar perfeito de primeira.** RAG dá trabalho de ajustar: tamanho do chunk, quantos trechos buscar (`k`), o prompt. Itere — e deixe o mini-eval dizer se está melhorando.
- **Ele ainda pode errar.** Reduzir alucinação não é zerar. Por isso a fonte e a avaliação importam tanto.
- **Comece feio e funcionando.** Um script simples que responde certo vale mais que uma arquitetura linda que nunca fica pronta.

## Exercício

1. Monte o assistente com 3 a 5 documentos que você conhece bem. Faça uma pergunta cuja resposta **está** nos documentos e outra cuja resposta **não está**. Ele acertou os dois casos (inclusive admitindo quando não sabe)?
2. Crie um mini-eval: 5 perguntas com a resposta certa (pelo menos uma cuja resposta não esteja nos docs). Rode, conte quantas ele acertou. Mude o tamanho do chunk ou o prompt e rode de novo — subiu ou caiu?
3. Passe pelo **checklist de pronto** e marque cada item de verdade.
4. Escreva, com suas palavras, o que aconteceu em cada passo (chunk → embedding → busca top-k → prompt → resposta com fonte) quando você fez uma pergunta. Se conseguir explicar sem olhar, você entendeu RAG de verdade. 🎉

---

<div align="center">

[« 28 - Custos e Escalabilidade](28-custos-e-escalabilidade.md) — [Índice](../README.md#roadmap) — [Glossário »](glossario.md)

</div>
