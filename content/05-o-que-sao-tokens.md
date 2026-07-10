# 05 - O que são Tokens

No capítulo anterior, dissemos que o ChatGPT prevê "a próxima palavra". Foi uma simplificação útil. Na verdade, ele não trabalha com palavras inteiras: trabalha com **tokens**. Entender isso vai te ajudar a economizar dinheiro, a não bater de cabeça nos limites das ferramentas e a entender por que a mesma frase em português custa mais que em inglês.

## O que é um token

Um **token** é um pedacinho de texto — a unidade que o modelo realmente enxerga. Um token pode ser uma palavra inteira, um pedaço de palavra, um espaço junto com a palavra ou um sinal de pontuação sozinho.

Em vez de explicar no abstrato, vamos ver **de verdade**. Estes são os tokens que o tokenizador do GPT (o `cl100k_base`, usado no GPT-3.5 e GPT-4) produz — não é exemplo inventado, é a saída real:

```text
"Eu adoro programar!"
→ ['Eu'] [' ad'] ['oro'] [' program'] ['ar'] ['!']
→ 6 tokens
```

Repare em três coisas que quase ninguém imagina antes de ver:

1. **"adoro" virou dois tokens**: `ad` + `oro`. Não é uma palavra só.
2. **O espaço vai grudado na palavra seguinte**: é `' program'` (com espaço), não `program`.
3. **`programar` virou `program` + `ar`** — o modelo reaproveita o pedaço `program`, que ele já conhece bem.

Esse processo de picar o texto se chama **tokenização**.

## Por que não usar palavras inteiras?

Porque nenhuma lista de palavras dá conta de **todas** as palavras do mundo: nomes próprios, gírias, código, palavras inventadas, erros de digitação. Se o modelo só conhecesse palavras inteiras, ele travaria na primeira palavra estranha.

A solução é um algoritmo chamado **BPE** (*Byte Pair Encoding*). A intuição, sem matemática:

> O tokenizador aprende, lendo bilhões de textos, quais **pedaços** aparecem juntos com mais frequência. Pedaços super comuns (`program`, ` the`, `ção`) viram um token só. O resto é montado juntando pedaços menores.

É como Lego: com um conjunto finito de peças (~100 mil, no caso do GPT), você monta **qualquer** palavra. Uma palavra comum usa uma peça grande; uma palavra rara é montada com várias peças pequenas — até, no limite, letra por letra.

## Português custa mais que inglês (com número real)

Aqui está algo com impacto direto no seu bolso. A **mesma frase**, nos dois idiomas, tokenizada de verdade:

```text
"A Inteligência Artificial está mudando o mundo do trabalho."   → 13 tokens
"Artificial Intelligence is changing the world of work."        → 10 tokens
```

Mesma ideia, **30% mais tokens em português**. Por quê? O tokenizador do GPT foi treinado majoritariamente em inglês, então ele tem "peças grandes" para o inglês e precisa quebrar o português em mais pedaços. Veja `Inteligência` sozinha:

```text
"Inteligência Artificial"
→ ['Int'] ['elig'] ['ência'] [' Artificial']
→ 4 tokens (sendo 3 só para "Inteligência")
```

`Artificial` é uma peça só (aparece muito em inglês). `Inteligência`, com acento e menos comum no treino, precisa de três pedaços. **Consequência prática**: escrever a mesma coisa em português consome mais tokens — logo, custa mais e enche mais rápido a janela de contexto.

## Tokens = dinheiro (a conta real)

Quando você usa uma **API** de IA (programando), paga **por token** — tanto pelos que envia (*input*) quanto pelos que recebe (*output*). Vamos fazer uma conta de verdade com um modelo barato, tipo o `gpt-4o-mini`.

Digamos um preço na ordem de **US$ 0,15 por 1 milhão de tokens de entrada** e **US$ 0,60 por 1 milhão de tokens de saída** (os valores mudam com o tempo — sempre confira na página de preços). Imagine um resumo de texto:

```text
Entrada:  2.000 tokens  →  2.000 / 1.000.000 × US$ 0,15  = US$ 0,0003
Saída:      500 tokens  →    500 / 1.000.000 × US$ 0,60  = US$ 0,0003
                                                   Total ≈ US$ 0,0006
```

Parece nada — e é, para **uma** chamada. Mas multiplique por 100 mil chamadas/mês e viram US$ 60. Agora imagine que você mandou junto, sem precisar, um manual de 50 mil tokens de contexto em toda chamada. A conta explode. **É por isso que ser objetivo não é só elegância: é a diferença entre uma feature barata e uma cara.** Veremos isso a fundo no [capítulo 28](28-custos-e-escalabilidade.md).

## Por dentro: de token a "próxima palavra"

Você já sabe que o modelo "prevê a próxima palavra". Agora dá pra ser preciso: ele prevê o **próximo token**. E os tokens são o começo de uma cadeia. Por alto, o que acontece dentro do modelo:

```text
"O gato subiu no"
   │
   ▼
[1] Tokenizar → [O] [ gato] [ subiu] [ no]      (texto vira tokens)
   │
   ▼
[2] Virar IDs → [46, 76543, 90211, 634]          (cada token tem um número de identidade)
   │
   ▼
[3] Cada ID vira um EMBEDDING (um vetor)          (o próximo capítulo... e o cap. 13)
   │
   ▼
[4] O transformer processa tudo junto
   │
   ▼
[5] Sai uma PROBABILIDADE para cada token possível:
        " telhado"  → 34%
        " muro"     → 22%
        " sofá"     →  9%
        ... (mais ~100 mil opções)
   │
   ▼
[6] Escolhe um, anexa ao texto e repete o processo
```

Ou seja: o token é a **entrada** e a **saída** da máquina. O modelo não gera frases de uma vez — ele gera **um token por vez**, sempre perguntando "qual o próximo token mais provável?", e realimenta o resultado. É por isso que a resposta aparece "digitando" na tela: cada pedacinho é um token recém-escolhido.

> Aquele parâmetro de **temperatura** que você talvez já tenha visto mexe justo no passo [5]: com temperatura baixa, o modelo quase sempre pega o token de maior probabilidade (mais previsível); com temperatura alta, ele arrisca tokens menos prováveis (mais criativo).

### Por que a IA erra contas

Isso explica um mistério comum: por que um modelo tão avançado erra `4327 × 8`? Porque números **também viram tokens**, e de um jeito bagunçado — `4327` pode virar `43` + `27`, ou `4` + `327`, dependendo do que apareceu no treino. O modelo não "faz a conta": ele tenta **prever os tokens** de um resultado plausível. Para contas de verdade, o certo é dar a ele uma **tool** de calculadora (veremos no [capítulo 17](17-o-que-e-uma-tool.md)) em vez de confiar no chute.

## Veja com seus próprios olhos

Duas formas de pegar a intuição na prática:

1. **Tokenizer visual**: a OpenAI tem o [Tokenizer](https://platform.openai.com/tokenizer) online. Cole uma frase em português e a mesma em inglês e compare a contagem.
2. **No código**: o exemplo [`examples/chamar-api`](../examples/chamar-api) imprime o campo `usage` da resposta — ou seja, quantos tokens *aquela* chamada gastou de entrada e de saída. É exatamente o número pelo qual você é cobrado.

Quer contar em Python direto? Com a biblioteca `tiktoken`:

```python
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")
ids = enc.encode("A Inteligência Artificial está mudando o mundo do trabalho.")
print(len(ids))                       # 13
print([enc.decode([i]) for i in ids]) # mostra cada token separado
```

## Recapitulando

- Token = a unidade real que o modelo processa (palavra, pedaço de palavra, espaço+palavra ou pontuação).
- A tokenização usa **BPE**: pedaços comuns viram um token; palavras raras são montadas com vários.
- **Português gasta mais tokens** que inglês para o mesmo conteúdo (~30% no exemplo).
- Tokens definem **custo** (você paga por token, entrada e saída) e **limite de contexto** (próximo capítulo).

## Exercício

1. Abra o [Tokenizer da OpenAI](https://platform.openai.com/tokenizer). Cole `Inteligência Artificial` e depois `Artificial Intelligence`. Anote a contagem de cada um. A diferença bate com o que vimos aqui?
2. Escreva um parágrafo seu (umas 3 frases) em português, cole no tokenizer e anote o total. Depois traduza para o inglês e compare. Quantos % de tokens você economizaria escrevendo em inglês?
3. Usando o preço do exemplo (US$ 0,15 por milhão de tokens de entrada), quanto custaria enviar **10.000 vezes** um prompt de 1.500 tokens? Faça a conta.

---

<div align="center">

[« 04 - Como o ChatGPT funciona](04-como-o-chatgpt-funciona.md) — [Índice](../README.md#roadmap) — [06 - O que é Janela de Contexto »](06-o-que-e-janela-de-contexto.md)

</div>
