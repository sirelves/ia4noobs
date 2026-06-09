# 10 - O que são Embeddings

Até agora você viu como conversar com uma IA. Agora vamos entender uma peça que está por trás de muita coisa: os **embeddings**.

A ideia é simples de sentir, mesmo que o nome assuste. Bora?

## A ideia central

Computador não entende texto. Ele entende número.

Um **embedding** é o jeito de transformar um texto (uma palavra, uma frase ou um documento inteiro) em uma **lista de números** que representa o **significado** daquele texto.

Essa lista de números a gente chama de **vetor**.

```
"gato"  ->  [0.81, 0.20, -0.05, 0.77, ...]
"frase" ->  [0.12, -0.66, 0.40, 0.09, ...]
```

Não precisa entender cada número. O importante é a ideia:

> Textos com significados **parecidos** viram listas de números **parecidas**.

## A analogia do mapa

Pense em um mapa de cidades.

Cada cidade tem uma coordenada (latitude e longitude). Cidades que ficam **perto** no mapa estão **próximas** de verdade. Cidades distantes estão longe.

Embeddings fazem o mesmo, mas com **significados** em vez de lugares:

- Coisas parecidas ficam **perto**.
- Coisas diferentes ficam **longe**.

Veja um mapa imaginário de palavras (usando só 2 coordenadas pra facilitar):

```
        ^  (eixo "animais")
        |
  felino ● gato ● gatinho
        |        ● cachorro
        |
--------+-----------------------> (eixo "veículos")
        |        ● carro
        |   caminhão ●  ônibus ●
        |
```

Repare: `gato`, `gatinho` e `felino` ficam **agrupados**. `caminhão`, `carro` e `ônibus` formam **outro grupo**, bem longe dos bichos.

O modelo não foi "ensinado" manualmente a isso. Ele aprendeu lendo muito texto e percebendo que essas palavras aparecem em contextos parecidos.

## Similaridade semântica

"Semântico" é só uma palavra chique pra **significado**.

**Similaridade semântica** é medir o quanto dois textos têm significados parecidos olhando o quão **perto** os vetores deles estão no mapa.

- `gato` e `gatinho` -> vetores pertinho -> alta similaridade.
- `gato` e `caminhão` -> vetores distantes -> baixa similaridade.

O legal: isso funciona mesmo quando as **palavras são diferentes**. Veja:

- "Como troco minha senha?"
- "Onde altero minha credencial de acesso?"

Quase nenhuma palavra em comum, mas o **significado** é o mesmo. Os embeddings dessas duas frases ficam pertinho no mapa.

## Pra que isso serve?

Embeddings destravam coisas muito úteis:

- **Busca por significado** (busca semântica): em vez de procurar a palavra exata, você acha o que **quer dizer** o mesmo. Procurar "carro quebrado" pode trazer "veículo com defeito".
- **Recomendação**: itens parecidos ficam perto. "Quem gostou disso, também gostou daquilo."
- **Agrupamento (clustering)**: juntar automaticamente textos parecidos, tipo separar tickets de suporte por assunto.
- **Base do RAG**: usado pra achar trechos de documentos relevantes (você vê isso no próximo capítulo).

## Quem gera os embeddings?

São os **modelos de embedding**. Eles são diferentes dos modelos de chat (como o que conversa com você).

O trabalho deles é um só: você manda um texto, e eles devolvem o vetor.

Em pseudo-código fica assim:

```python
# Pseudo-código só pra ilustrar a ideia
vetor_gato     = modelo_embedding("gato")
vetor_gatinho  = modelo_embedding("gatinho")
vetor_caminhao = modelo_embedding("caminhão")

# Comparando significados (quanto maior, mais parecido)
similaridade(vetor_gato, vetor_gatinho)   # -> alto
similaridade(vetor_gato, vetor_caminhao)  # -> baixo
```

Na prática, esses vetores não têm 2 números como no nosso mapa de exemplo. Eles têm **centenas ou milhares** de números (centenas de "coordenadas"). É impossível desenhar isso num papel, mas a ideia continua exatamente a mesma: **coisas parecidas ficam perto**.

## Seja honesto: os limites

- Embeddings capturam **padrões de uso da linguagem**, não a verdade. Eles não "sabem" o que é certo ou errado.
- A qualidade depende do modelo e dos dados em que ele foi treinado. Idiomas e assuntos pouco representados saem piores.
- Eles podem carregar **vieses** dos textos de treino.
- Comparar significados não é o mesmo que **entender** de verdade. É estatística bem feita, não consciência.

## Exercício

Pense em 6 palavras: três de um grupo (ex: comidas) e três de outro (ex: esportes).

1. Desenhe um mapa 2D no papel, como o do exemplo, e posicione as 6 palavras. Coloque as parecidas perto e as diferentes longe.
2. Escreva por que `pizza` e `lasanha` deveriam ficar perto, e por que `pizza` e `futebol` deveriam ficar longe.
3. Bônus: pense em duas frases que dizem a **mesma coisa** com **palavras diferentes**. Por que os embeddings delas ficariam perto?

---

<div align="center">

[« 09 - Principais erros ao usar IA](09-principais-erros-ao-usar-ia.md) — [Índice](../README.md#roadmap) — [11 - O que é RAG »](11-o-que-e-rag.md)

</div>
