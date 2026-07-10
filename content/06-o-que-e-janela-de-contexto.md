# 06 - O que é Janela de Contexto

No capítulo anterior você viu que o modelo enxerga tudo em **tokens**. Agora vem a pergunta natural: quantos tokens ele consegue olhar de uma vez? A resposta tem nome: **janela de contexto**. É ela que explica por que conversas longas começam a "dar branco" e por que a IA às vezes esquece o que você disse lá no começo.

## A definição

A **janela de contexto** é o total de tokens que o modelo consegue "enxergar" ao mesmo tempo para gerar a próxima resposta. E o detalhe que quase ninguém percebe: ela conta **tudo junto**. Não é só a sua mensagem.

O que ocupa a janela, somado, a cada chamada:

```text
┌──────────────────────── JANELA DE CONTEXTO (limite fixo) ────────────────────────┐
│                                                                                    │
│  [ System prompt ]   as instruções invisíveis ("você é um assistente...")          │
│  [ Histórico     ]   todas as mensagens anteriores da conversa (suas + dele)       │
│  [ Sua mensagem  ]   o que você acabou de escrever agora                           │
│  [ Resposta      ]   o espaço reservado para o que o modelo VAI gerar              │
│                                                                                    │
└────────────────────────────────────────────────────────────────────────────────┘
        Tudo isso precisa caber AO MESMO TEMPO dentro do limite.
```

O que fica **fora** da janela é, para o modelo, como se não existisse. Ele não "lembra" — ele só processa o que está dentro da janela naquele instante.

## A analogia da mesa de trabalho

Pense na janela como uma **mesa de trabalho** de tamanho fixo. Você vai colocando papéis: as instruções, sua pergunta, os documentos que colou, as respostas anteriores. Enquanto tudo cabe, o modelo olha o conjunto inteiro e responde considerando tudo.

O problema aparece quando a mesa enche. Aí **algo precisa sair para abrir espaço** — e quem sai primeiro é geralmente o **começo** da conversa, as mensagens mais antigas. Na prática você vê:

- A IA "esquece" um detalhe que você deu lá no início.
- Ela se repete ou perde o fio da meada.
- O sistema corta (trunca) parte do texto sem avisar.

Não é preguiça nem má vontade: é conteúdo antigo caindo da mesa para o novo caber.

## Tamanhos reais (ordens de grandeza — mudam rápido)

Cada modelo tem uma janela diferente. Estes números são **aproximados, por volta de 2025-2026, e mudam a cada versão nova** — trate como ordem de grandeza, não como verdade cravada:

```text
Modelos GPT recentes   →  por volta de  ~128 mil tokens     mesa grande
Modelos Claude         →  por volta de  ~200 mil tokens     mesa maior
Modelos Gemini         →  chegando a    ~1 milhão+ tokens   mesa enorme
```

Isso ainda é abstrato. Vamos traduzir para algo que dá para sentir, usando uma regra de bolso: **~750 palavras ≈ 1.000 tokens**.

```text
128 mil tokens  ≈  128 × 750 palavras  ≈  96 mil palavras
96 mil palavras ÷ ~320 palavras por página  ≈  300 páginas
```

Ou seja: uma janela de ~128 mil tokens cabe **um livro inteiro de umas 300 páginas** — de uma vez só. A janela de ~1 milhão de tokens cabe algo como **uma coleção de vários livros**. É muita coisa. Mas, como você vai ver, "caber" não é o mesmo que "usar bem".

## O fenômeno "perdido no meio" (lost in the middle)

Aqui está o achado mais importante — e mais contraintuitivo — deste capítulo. Ter uma janela gigante **não** significa que o modelo presta atenção igual em tudo que está nela.

Pesquisas conhecidas sobre modelos de linguagem mostram um padrão claro: o modelo costuma lembrar melhor do que está no **começo** e no **fim** do contexto, e tende a "perder" informação enfiada bem no **meio** de um contexto muito longo. É o efeito apelidado de **lost in the middle** ("perdido no meio").

```text
Atenção do modelo ao longo do contexto (intuição):

  forte  ██                                          ██
         ███                                        ███
         ████░░░░░░░  o meio "some"  ░░░░░░░░░░░░░████
  fraca  │      ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░      │
         └────────────────────────────────────────────
         começo             MEIO                    fim
```

**Implicação prática, direto ao ponto:** coloque o que é mais importante no **começo** ou no **fim** do seu prompt — nunca soterrado no meio de um textão. Se você cola um documento de 50 páginas e faz a pergunta crucial no meio dele, aumenta a chance de o modelo passar batido.

## Por dentro: por que esse limite existe?

Por que simplesmente não fazem a janela infinita? A resposta está em como o transformer processa o texto — aquele mecanismo que citamos no [capítulo 04](04-como-o-chatgpt-funciona.md).

O coração do transformer é a **atenção** (*attention*). A intuição, sem fórmula: para processar o texto, **cada token "olha" para todos os outros tokens** da janela para decidir o que é relevante. É isso que dá ao modelo a noção de contexto — a palavra "banco" olha para "sentei no" ou para "fui ao" e entende de qual banco você fala.

O problema: se cada token olha para todos os outros, o custo **não cresce em linha reta com o tamanho do contexto — cresce muito mais rápido**. Dobrar o número de tokens é muito mais que dobrar o trabalho, porque o número de "olhares" entre pares de tokens explode. Intuitivamente: 10 pessoas se cumprimentando dão 45 apertos de mão; 20 pessoas dão 190, não 90. É por isso que existe um teto — a certa altura fica caro e lento demais processar mais.

E isso liga direto no seu bolso. Como você viu no [capítulo 05 - Tokens](05-o-que-sao-tokens.md), você paga **por token** — e a conta inclui **todo** o contexto reenviado a cada mensagem. Contexto grande significa:

- **Mais lento:** mais tokens para processar = resposta demora mais.
- **Mais caro:** você paga pela janela inteira a cada chamada, não só pela sua última frase. Numa conversa longa, o histórico é reenviado repetidas vezes. Veremos essa conta a fundo no [capítulo 28 - Custos](28-custos-e-escalabilidade.md).

## Estratégias para não estourar (nem desperdiçar) a janela

Você não precisa decorar números. Precisa de bons hábitos:

- **Seja objetivo.** Mande só o que importa; corte enrolação e repetição. Cada token cortado é mais rápido e mais barato.
- **Resuma o histórico antigo.** Em conversas longas, peça à IA um resumo do que já foi combinado e siga a partir dele. Você troca centenas de mensagens antigas por um parágrafo — a mesa esvazia sem perder o essencial.
- **Recomece quando travar.** Se a conversa está confusa ou "esquecida", abra um chat novo e cole só o resumo essencial.
- **Use RAG em vez de enfiar tudo.** Quando você tem uma base enorme (uma pasta de PDFs, uma wiki inteira), a jogada não é despejar tudo na janela. É buscar **só o trecho relevante** para a pergunta e mandar apenas ele. Essa técnica se chama **RAG**, e é o assunto do [capítulo 14 - RAG](14-o-que-e-rag.md).
- **Posicione bem.** Lembre do *lost in the middle*: o mais importante vai no começo ou no fim.

## Limites honestos

Três verdades para você levar deste capítulo:

1. **Janela grande ≠ usa bem tudo.** Por causa do *lost in the middle*, um modelo com 1 milhão de tokens ainda pode ignorar algo importante no meio. Espaço não é atenção.
2. **Mais contexto custa mais** — em dinheiro e em tempo. Encher a janela "porque cabe" é desperdício.
3. **Não é memória permanente.** A janela é memória de curto prazo. O que sai dela **some** — o modelo não guarda nada entre conversas por conta própria. (Alguns produtos criam uma "memória" por cima disso, mas é um truque extra, não o modelo lembrando.)

## Recapitulando

- Janela de contexto = total de tokens que o modelo enxerga de uma vez: **system prompt + histórico + sua mensagem + a resposta que ele vai gerar**.
- Tamanhos hoje giram na ordem de **~128 mil** (GPT), **~200 mil** (Claude) e **~1 milhão+** (Gemini) — aproximados e mudando sempre.
- **~128 mil tokens ≈ 300 páginas** de livro.
- *Lost in the middle*: o modelo lembra melhor do começo e do fim; ponha o importante nas pontas.
- O limite existe porque a **atenção** custa cada vez mais conforme o contexto cresce — mais lento e mais caro.
- Para lidar: seja objetivo, resuma o histórico e use **RAG** para buscar só o relevante.

## Exercício

1. Pegue uma conversa longa sua com uma IA (ou imagine uma com umas 40 mensagens). Usando a regra **~750 palavras ≈ 1.000 tokens**, estime quantos tokens ela já consumiu. Isso está perto de estourar uma janela de ~128 mil?
2. Você precisa caber um contexto que passou do limite. Liste, em ordem, **o que você cortaria primeiro** e por quê — e diga o que jamais cortaria.
3. Cole um texto bem grande numa IA (um capítulo de livro, por exemplo), esconda uma frase estranha no **meio** dele (tipo "o código secreto é 4271") e no **fim** faça uma pergunta que dependa dela. O modelo achou? Depois teste o mesmo com a frase no **começo**. Deu diferença? Você acabou de ver o *lost in the middle* ao vivo.

---

<div align="center">

[« 05 - O que são Tokens](05-o-que-sao-tokens.md) — [Índice](../README.md#roadmap) — [07 - Escolhendo o modelo certo »](07-escolhendo-o-modelo-certo.md)

</div>
