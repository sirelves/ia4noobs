# 04 - O que são Tokens

No capítulo anterior, dissemos que o ChatGPT prevê "a próxima palavra". Foi uma simplificação útil. Na verdade, ele não trabalha com palavras inteiras: trabalha com **tokens**. Entender isso vai te ajudar a economizar dinheiro e a não bater de cabeça nos limites das ferramentas.

## O que é um token

Um **token** é um pedacinho de texto. Pode ser:

- uma palavra inteira (`gato`),
- um pedaço de palavra (`incrível` pode virar `in` + `crível`),
- um espaço ou um sinal de pontuação (`,`, `.`, `!`).

O modelo quebra todo o texto nesses pedaços antes de processar. Esse processo de "picar o texto" se chama **tokenização**.

Por que não usar palavras inteiras? Porque pedaços menores permitem lidar com **qualquer** palavra, até as que o modelo nunca viu (nomes estranhos, gírias, palavras inventadas). Ele monta tudo a partir das peças que conhece, como peças de Lego.

## Vendo uma frase virar tokens

Imagine a frase:

```text
Eu adoro programar!
```

Uma forma possível de quebrá-la em tokens seria:

```text
["Eu"] [" ador"] ["ar"]  ...
```

Para deixar mais visual, com uma frase em português:

```text
Frase:  Olá, mundo!
Tokens: [Olá] [,] [ mundo] [!]
        →  4 tokens
```

Repare que a vírgula virou um token sozinho, e o espaço antes de "mundo" foi junto com a palavra. A divisão exata depende do modelo, mas a ideia é sempre essa: **texto vira uma sequência de pedacinhos**.

## Regra de bolso

Você não precisa contar token por token na mão. Use esta estimativa:

- Em **inglês**, mais ou menos **1 token ≈ 4 caracteres**, ou cerca de **¾ de palavra**.
- Em **português**, costumamos gastar **um pouco mais** de tokens para o mesmo conteúdo. Acentos, palavras mais longas e a forma como o modelo foi treinado fazem o texto se quebrar em mais pedaços.

Tradução prática: a mesma ideia escrita em português normalmente **consome mais tokens** do que em inglês. Bom saber na hora de calcular custos.

## Por que tokens importam

Tokens não são só curiosidade técnica. Eles têm impacto direto:

- **Custo**: quando você usa uma API de IA (programando), você **paga por token** — tanto pelo texto que envia quanto pelo que recebe. Mais tokens = mais caro.
- **Limites de contexto**: cada modelo aguenta uma quantidade máxima de tokens por vez. Esse é o tema do próximo capítulo (a "janela de contexto"). Textos muito longos podem estourar esse limite.

Ou seja: ser **objetivo** no que você escreve não é só elegância — economiza dinheiro e evita problemas de limite.

## Dá para visualizar

Existem ferramentas chamadas **tokenizers** (tokenizadores) que mostram, ao vivo, como uma frase é quebrada e quantos tokens ela consome. A OpenAI tem o "Tokenizer", e outras empresas têm os seus. Vale brincar: cole uma frase em português e outra em inglês e compare a contagem. É a melhor forma de pegar a intuição.

## Recapitulando

- Token = pedaço de texto (palavra, parte de palavra ou pontuação).
- O modelo tokeniza tudo antes de processar.
- Regra de bolso: ~4 caracteres por token em inglês; português gasta um pouco mais.
- Tokens definem **custo** (em APIs) e **limite de contexto**.

## Exercício

1. Sem usar ferramenta, **estime** quantos tokens tem a frase em inglês `I love to code` usando a regra de ~4 caracteres por token.
2. Por que a mesma mensagem em português tende a consumir mais tokens do que em inglês?
3. Cite **dois** motivos pelos quais a contagem de tokens importa na prática.

---

<div align="center">

[« 03 - Como o ChatGPT funciona](03-como-o-chatgpt-funciona.md) — [Índice](../README.md#roadmap) — [05 - O que é Janela de Contexto »](05-o-que-e-janela-de-contexto.md)

</div>
