# RAG mínimo (busca por similaridade)

Este exemplo mostra, com o **mínimo de dependências possível**, a ideia central
de um **RAG** (Retrieval-Augmented Generation): a etapa de **busca por
similaridade** (o "retrieval").

A pergunta do usuário e cada documento viram **vetores de números**. Comparamos
esses vetores com **similaridade do cosseno** e devolvemos os documentos mais
parecidos. É exatamente isso que acontece "por baixo" de um RAG quando ele
procura quais trechos da sua base usar para responder.

## O que este exemplo SIMPLIFICA

Para rodar offline e sem custo, ele corta vários cantos de propósito:

- **Embedding falso/didático**: em vez de um modelo de embeddings real, usamos
  um simples **vetor de frequência de palavras** (bag-of-words) sobre um
  vocabulário montado a partir dos documentos. Funciona quando a pergunta
  **repete palavras** dos documentos, mas não entende sinônimos nem significado.
- **Sem LLM**: nada de geração de texto. O script faz a busca e **monta o
  prompt** (trechos marcados com a fonte + pergunta + regra anti-alucinação),
  mas não o envia. Pra fechar o ciclo, cole esse prompt no
  [`chamar-api`](../chamar-api) ou no [`modelo-local`](../modelo-local).
- **Só palavra-chave**: como o "embedding" é contagem de palavras, a busca se
  comporta como uma busca **por palavra-chave**. Teste "como começo a codar?":
  nenhuma palavra bate com "programar", e o resultado vem ruim. Um embedding
  real acertaria. Veja a seção de busca híbrida no [cap. 16](../../content/16-rag-na-pratica.md).
- **Sem banco vetorial**: uma simples **lista em memória** faz esse papel. Não
  há índice otimizado nem persistência.

## Como rodar

Não precisa instalar nada (apenas Python 3 e a biblioteca padrão):

```bash
python busca.py
```

O script pede uma pergunta. Aperte **Enter** para usar o exemplo embutido
(`"Quero aprender a programar"`).

## O que isto vira num RAG de verdade

| Aqui (didático) | Num RAG de verdade |
| --- | --- |
| `texto_para_vetor` (contagem de palavras) | **Modelo de embeddings real** (entende significado; sinônimos ficam próximos) |
| Lista `DOCUMENTOS` em memória | **Banco vetorial** (ex.: Pinecone, Chroma, pgvector) com índice rápido e persistente |
| `similaridade_cosseno` no Python | A mesma ideia, mas executada **dentro do banco vetorial** sobre milhões de vetores |
| `montar_prompt` + `print` | O prompt é **enviado a um LLM**, que gera a resposta final citando a fonte |
| Fonte `doc-N` (posição na lista) | **Metadados** guardados com cada chunk (arquivo, seção, data) |

O fluxo de um RAG completo, então, é:

1. **Indexar** (uma vez): quebrar documentos em pedaços, gerar embeddings e
   salvar no banco vetorial.
2. **Recuperar** (a cada pergunta): transformar a pergunta em embedding e buscar
   os pedaços mais parecidos — **é o que este exemplo faz**.
3. **Gerar**: montar um prompt com a pergunta + os pedaços recuperados e pedir
   ao LLM a resposta.

---

Veja [14 - O que é RAG](../../content/14-o-que-e-rag.md),
[15 - O que é Banco Vetorial](../../content/15-o-que-e-banco-vetorial.md) e
[16 - RAG na prática](../../content/16-rag-na-pratica.md).
