# 12 - O que é Banco Vetorial

No capítulo do RAG apareceu uma caixa chamada **Banco Vetorial**. Era ali que os embeddings ficavam guardados. Agora vamos entender o que é essa peça.

## O que é

Um **banco vetorial** é um banco de dados feito especialmente pra:

1. **Guardar** embeddings (aqueles vetores, as listas de números).
2. **Buscar** por **similaridade** — ou seja, achar os vetores mais **parecidos** com um vetor de busca.

Lembra da analogia do mapa? Um banco vetorial é como um mapa gigante onde cada documento é um ponto. A pergunta dele é sempre a mesma:

> "Quais pontos estão **mais perto** deste aqui?"

## Por que um banco SQL comum não resolve?

Um banco de dados tradicional (SQL) é ótimo pra buscas **exatas**:

```sql
SELECT * FROM produtos WHERE nome = 'camiseta azul';
```

Isso responde "é igual ou não é igual". Funciona perfeito pra ID, e-mail, preço.

Mas a busca por significado é diferente. Ela não pergunta "isto é **igual**?". Ela pergunta "qual é o **mais parecido**?". E "parecido" aqui significa **perto no mapa** de centenas de coordenadas.

Fazer isso num banco SQL comum seria muito lento: ele teria que comparar a sua busca com **cada item**, um por um, calculando distância. Com milhões de itens, vira um pesadelo.

O banco vetorial nasceu justamente pra resolver isso de forma rápida.

## Busca por vizinhos mais próximos

O nome técnico da busca é **nearest neighbors** (vizinhos mais próximos).

A ideia, em palavras simples:

- Você tem um ponto (o embedding da sua pergunta).
- Você quer os **N pontos mais próximos** dele no mapa.
- Esses vizinhos são os documentos mais **relevantes**.

```
              ● doc sobre gatos
   PERGUNTA ★   ● doc sobre felinos      <- vizinhos próximos (relevantes)
              ● doc sobre cães

                              ● doc sobre caminhões  <- longe (ignorado)
```

A estrela ★ é a sua pergunta. Os 3 pontos perto dela são as respostas que o banco devolve.

## Velocidade: a busca aproximada (ANN)

Comparar a sua busca com **todos** os pontos dá a resposta perfeita, mas é lento.

Por isso os bancos vetoriais usam **indexação aproximada**, chamada **ANN** (Approximate Nearest Neighbors — vizinhos mais próximos **aproximados**).

A ideia é organizar os vetores de um jeito esperto pra não precisar olhar todos. Em troca:

- Você **abre mão de um pouquinho de precisão**...
- ...e ganha **muita velocidade**.

Na prática, quase sempre vale a pena. Achar "os 5 mais relevantes" em milissegundos é melhor do que esperar muito por uma resposta 100% perfeita.

## Exemplos reais

Existem várias opções, cada uma com seu foco. Citando de forma neutra:

- **pgvector**: extensão que adiciona busca vetorial ao PostgreSQL (bom se você já usa Postgres).
- **Chroma**: leve e simples, popular pra começar e prototipar.
- **Qdrant**: open-source, focado em performance.
- **Weaviate**: open-source, com bastante recurso de busca.
- **Pinecone**: serviço gerenciado na nuvem (você não administra o servidor).
- **FAISS**: biblioteca da Meta pra busca por similaridade, muito usada em pesquisa.

Não existe "o melhor". A escolha depende do seu projeto, do tamanho dos dados e de quanto você quer gerenciar. Pra estudar, um simples como o Chroma já resolve.

## O papel dele dentro do RAG

Voltando ao fluxo do RAG, o banco vetorial é o **coração da busca**:

```
PREPARAÇÃO:
  documentos -> embeddings -> [ guardados no Banco Vetorial ]

NA PERGUNTA:
  pergunta -> embedding -> [ Banco Vetorial busca os vizinhos ] -> trechos relevantes
```

Ou seja: é **onde os embeddings ficam guardados** e **de onde os trechos relevantes são recuperados**. Sem ele, o passo "buscar os pedaços mais relevantes" do RAG não acontece bem.

## Conectando com a prática

Neste repositório existe o exemplo `examples/rag-mini`. Ele junta tudo o que você viu neste módulo:

- gera **embeddings** dos textos (capítulo 10),
- guarda esses vetores em um **banco vetorial** (este capítulo),
- e usa isso pra montar um **RAG** que responde perguntas (capítulo 11).

É um ótimo lugar pra ver os três conceitos funcionando juntos, num código pequeno e comentado.

## Seja honesto: os limites

- Banco vetorial **não pensa**: ele só acha o que está perto. Se o embedding for ruim, a busca será ruim.
- A busca aproximada (ANN) pode, de vez em quando, **deixar passar** um vizinho relevante. É o preço da velocidade.
- Ele guarda e busca, mas **não gera a resposta**. Quem responde é o LLM. O banco só entrega o material.

## Exercício

1. Explique, com suas palavras, por que um `SELECT ... WHERE nome = 'x'` não serve bem pra busca por significado.
2. Desenhe um mapa com 5 pontos e uma estrela (a pergunta). Marque quais 2 pontos o banco vetorial devolveria como "vizinhos mais próximos".
3. Pesquise rapidamente um dos bancos citados (ex: Chroma ou pgvector) e escreva uma frase sobre quando você o usaria.
4. Bônus: abra o exemplo `examples/rag-mini` e identifique no código onde os embeddings são **guardados** e onde eles são **buscados**.

---

<div align="center">

[« 11 - O que é RAG](11-o-que-e-rag.md) — [Índice](../README.md#roadmap) — [13 - O que é um Agent »](13-o-que-e-um-agent.md)

</div>
