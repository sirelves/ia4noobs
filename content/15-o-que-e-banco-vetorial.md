# 15 - O que é Banco Vetorial

No [capítulo do RAG](14-o-que-e-rag.md) apareceu uma caixa chamada **Banco Vetorial**. Era ali que os embeddings ficavam guardados e de onde saíam os trechos relevantes. Agora vamos abrir essa caixa. Ela existe pra resolver **um** problema bem específico — e vale a pena entender qual, porque isso decide se você precisa de um banco vetorial de verdade ou se uma lista e um pouco de código já resolvem.

## O que é

Um **banco vetorial** é um banco de dados feito pra duas tarefas:

1. **Guardar** embeddings (aqueles vetores, as listas de números do [capítulo 13](13-o-que-sao-embeddings.md)).
2. **Achar rápido** os vetores mais **parecidos** com um vetor de busca.

É a peça de **armazenamento e busca** do RAG. O gerador de resposta é o LLM; o banco vetorial é a estante organizada de onde ele puxa o material certo.

## O problema: comparar com todo mundo é caro

Buscar por similaridade significa achar os pontos mais **próximos** no mapa de embeddings. O jeito ingênuo — e correto — é a **força bruta**: pega o vetor da pergunta e compara com **cada um** dos vetores guardados, calcula a distância de todos, e ordena.

Funciona lindamente pra alguns milhares de itens. O problema aparece na escala:

```text
1 pergunta comparada com...
      10.000 vetores  → instantâneo
   1.000.000 vetores  → começa a pesar
  10.000.000 vetores  → inviável em tempo real, a cada busca
```

Imagine um site com 10 milhões de trechos indexados, recebendo várias buscas por segundo. Cada busca teria que percorrer os 10 milhões de vetores do zero. É como procurar uma pessoa numa cidade tocando a campainha de **todas** as casas, uma por uma, toda vez. A resposta é perfeita, mas ninguém tem esse tempo.

## A solução: busca aproximada (ANN)

A saída tem nome: **ANN** (*Approximate Nearest Neighbor* — vizinho mais próximo **aproximado**). Em vez de comparar com todos, você monta antes um **índice** esperto que permite pular direto pra região onde os vizinhos provavelmente estão.

O índice mais usado hoje chama-se **HNSW** (*Hierarchical Navigable Small World*). A intuição, sem fórmula:

> Imagine que cada vetor é uma cidade, ligada por estradas às suas cidades **vizinhas** mais parecidas — uma malha de estradas construída de antemão. Pra achar quem está perto da sua pergunta, você não visita a cidade inteira: você **salta** de vizinho em vizinho, e cada salto te deixa mais perto do alvo. Quando não dá mais pra chegar mais perto, parou: os vizinhos ali em volta são a resposta.

É "aproximado" porque, seguindo só as estradas, a busca pode — de vez em quando — passar reto pelo vizinho **perfeito** e devolver o segundo ou terceiro melhor. Em troca, ela olha algumas **centenas** de pontos em vez de **milhões**. Na prática de busca semântica, esse errinho raro quase nunca importa, e a velocidade muda tudo.

```text
FORÇA BRUTA (compara com todos)
  pergunta ─▶ v1  v2  v3  v4  v5  ...  v9.999.999  v10.000.000
             └──────── calcula distância de CADA um ────────┘
             correto, porém lento

ÍNDICE ANN / HNSW (salta pelos vizinhos)
  pergunta ─▶ entra num ponto qualquer
                 │  salta pro vizinho mais perto
                 ▼
                ●──▶●──▶●──▶★   chegou perto do alvo
             visita ~centenas de pontos, não milhões
             rápido, e quase sempre certo
```

## Você precisa mesmo de um banco vetorial?

Aqui vale a honestidade, e o princípio do *boring technology*: **nem todo projeto precisa de um banco vetorial dedicado.**

- **Estudo / poucos milhares de itens** → **não precisa**. Uma lista de vetores + `numpy` calculando a distância de todos (força bruta) responde em milissegundos. É exatamente o que faz o exemplo [`examples/rag-mini`](../examples/rag-mini) deste repositório: sem servidor, sem infra, sem índice. Comece por aí.
- **Muitos vetores, muitas buscas por segundo, ou você quer persistência e filtro por metadados** → **aí sim** um banco vetorial dedicado passa a valer a pena.

Traduzindo: a força bruta não é "o jeito errado". Ela é o jeito **certo** enquanto os números são pequenos. O banco vetorial entra quando a força bruta deixa de dar conta.

## Filtro por metadados

Um banco vetorial guarda, junto de cada vetor, **dados comuns** sobre o trecho: autor, data, categoria, idioma, ID do documento. Isso permite **filtrar** a busca por significado:

```text
"ache os trechos mais parecidos com esta pergunta,
 MAS só entre documentos de 2024 e da categoria 'financeiro'"
```

Fazer isso na mão, com uma lista + numpy, dá trabalho. É um dos motivos mais fortes pra migrar pra um banco de verdade: você combina "parecido no significado" com "bate com estes campos" numa consulta só.

## Ferramentas (exemplos, não ranking)

O ecossistema muda rápido e nomes vêm e vão — trate a lista abaixo como **exemplos de famílias**, não como um pódio definitivo:

- **pgvector** — extensão que adiciona busca vetorial ao **PostgreSQL**. Se você já usa Postgres, é o começo mais "boring" e sensato: um banco a menos pra manter.
- **FAISS** — biblioteca da Meta pra busca por similaridade, muito usada em pesquisa. É biblioteca, não servidor.
- **Chroma, Qdrant, Weaviate, Milvus** — bancos/serviços dedicados, open-source, cada um com seu foco.
- **Pinecone** — serviço gerenciado na nuvem (você não administra o servidor).

Recomendação prática: **comece simples.** Já tem Postgres? Use pgvector. Só estudando? Fique na lista + numpy do `rag-mini`. Só troque por algo mais parrudo quando um número real (volume, latência, buscas por segundo) pedir.

## Por dentro: precisão trocada por velocidade

A ideia-chave do banco vetorial cabe numa frase: **ANN abre mão da resposta perfeita pra ganhar muita velocidade.**

A força bruta te dá o vizinho **exato**, sempre — pagando o preço de olhar todo mundo. O índice ANN (HNSW e parentes) organiza os vetores numa malha navegável e **salta** por ela, olhando uma fração dos pontos. O resultado é *quase* sempre igual ao da força bruta, e chega em milissegundos mesmo com milhões de itens. Esse "quase" é o trade-off central, e na busca semântica ele costuma ser um ótimo negócio.

## Seja honesto: os limites

- **É aproximado.** Por definição, o ANN pode, de vez em quando, deixar passar o vizinho ideal. Se seu caso exige recuperação exata (raro em busca por significado), força bruta ou modos exatos são o caminho.
- **O índice tem parâmetros.** HNSW e afins têm botões de ajuste que equilibram velocidade × precisão × memória. O padrão costuma servir, mas afinar dá trabalho.
- **É mais infra pra manter.** Um serviço a mais pra subir, atualizar, fazer backup e monitorar. Não adote por hype.
- **O banco não conserta embedding ruim.** Ele acha o que está perto no mapa que você deu. Se o embedding representa mal o texto (modelo errado, trecho grande demais), a busca vem ruim — e o banco não tem como saber. Lixo entra, lixo sai.

## Exercício

1. Seu FAQ tem **3.000** perguntas. Vale montar um banco vetorial dedicado, ou força bruta com numpy resolve? E se fossem **8 milhões** de trechos com 200 buscas por segundo? Justifique cada caso em uma frase.
2. Você vai indexar os artigos de um blog. Liste **3 metadados** que valeria guardar junto de cada vetor e dê um exemplo de busca filtrada que cada um habilitaria (ex.: filtrar por `ano`).
3. Abra o exemplo [`examples/rag-mini`](../examples/rag-mini) e ache no código onde os vetores são **guardados** e onde são **buscados**. Ele usa força bruta ou um índice ANN? O que precisaria mudar se a base saltasse de 500 para 50 milhões de itens?

---

<div align="center">

[« 14 - O que é RAG](14-o-que-e-rag.md) — [Índice](../README.md#roadmap) — [16 - O que é um Agent »](16-o-que-e-um-agent.md)

</div>
