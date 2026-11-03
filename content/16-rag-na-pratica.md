# 16 - RAG na prática

No [capítulo 14](14-o-que-e-rag.md) você montou o RAG básico: quebrar em chunks, buscar os top-k, montar o prompt. No [capítulo 15](15-o-que-e-banco-vetorial.md) viu onde os vetores moram. Esse básico já resolve muita coisa, mas na vida real você logo esbarra em respostas erradas e não sabe por quê.

Este capítulo é a **caixa de ferramentas** pra fazer o RAG funcionar bem. A regra de ouro dele: **meça antes de mexer**. Cada técnica aqui adiciona custo e complexidade, então só vale ligar a que resolve o problema que a sua medição apontou.

## Primeiro: meça (o RAG tem duas metades)

Um RAG tem **duas metades**, e cada uma erra de um jeito. Avalie as duas separado ([capítulo 28](28-como-avaliar-respostas-de-ia.md)):

1. **A busca trouxe o trecho certo?** Pra cada pergunta do seu teste, anote qual chunk tem a resposta e confira se ele apareceu entre os `k` recuperados. A porcentagem de acertos se chama **recall@k** ("o certo estava entre os k?").
2. **A resposta é fiel aos trechos?** Dado que o trecho certo veio, o modelo respondeu **com base nele**, sem inventar nada além? Isso se chama **fidelidade** (*faithfulness*).

Por que separar? Porque o conserto é diferente:

```text
Resposta errada
   |
   |-- o trecho certo NÃO veio na busca?
   |        -> problema de RECUPERAÇÃO: mexa no chunk, no k,
   |           tente busca híbrida, re-ranking...      (seções 1 a 4)
   |
   '-- o trecho certo VEIO, mas a resposta saiu errada?
            -> problema de GERAÇÃO: mexa no prompt, no modelo...
                                                       (seção 5)
```

Sem essa separação, você fica trocando o modelo quando o problema era o chunk (ou o contrário). Existem ferramentas prontas que medem essas métricas, como o **Ragas**, mas uma planilha com 10 a 20 perguntas já te leva longe.

> ⚠️ **Exemplo ilustrativo** — uma planilha de avaliação mínima:
>
> ```text
> Pergunta                    | Chunk esperado        | Veio no top-3? | Resposta certa?
> ----------------------------|-----------------------|----------------|----------------
> Qual o prazo de devolução?  | politica-de-trocas #1 | sim            | sim
> Aceita Pix?                 | pagamentos #1         | sim            | não  <- geração
> O que é o erro ERR-4021?    | erros #12             | não            | não  <- recuperação
> ```

## 1. Melhorando o chunking

O tamanho do chunk é um trade-off ([capítulo 14](14-o-que-e-rag.md)). Mas o **jeito de cortar** importa tanto quanto o tamanho. Do mais simples ao mais esperto:

- **Tamanho fixo**: a cada N tokens (ou caracteres), corta. Fácil de fazer, mas pode partir uma frase ou tabela no meio, por isso o overlap.
- **Pela estrutura do texto**: corta onde o próprio documento já se divide: títulos, seções, parágrafos. Um FAQ, por exemplo, pede **um chunk por pergunta+resposta**. Costuma ser a melhor escolha quando o documento é bem organizado.
- **Recursivo**: tenta cortar primeiro por parágrafo; se o pedaço ainda ficar grande, por linha; depois por frase. É o que muitas bibliotecas (como o LangChain) fazem por padrão.

E o tamanho? Pra ter uma referência de partida (não uma verdade): a busca em arquivos da OpenAI usa por padrão chunks de **800 tokens com 400 de overlap**. Pra textos curtos como um FAQ, chunks bem menores (um parágrafo) funcionam melhor. Comece com algo razoável e deixe a sua planilha de avaliação decidir.

> 💡 **Guarde metadados junto de cada chunk**: de qual arquivo veio, título da seção, data. Sem isso você não consegue **citar a fonte** depois, e nem **filtrar** a busca ([capítulo 15](15-o-que-e-banco-vetorial.md)).

## 2. Busca híbrida: significado + palavra exata

A busca por significado tem um ponto cego: **termos exatos**. Pergunte "o que significa o erro `ERR-4021`?" e o embedding pode trazer trechos sobre "erros em geral", porque pra ele `ERR-4021` e `ERR-4022` "significam" quase a mesma coisa. Códigos, nomes de produto, siglas e números de lei sofrem disso.

A busca **por palavra-chave** (a clássica, de buscador; o algoritmo mais usado se chama **BM25**) é o oposto: não entende sinônimo, mas acerta em cheio termo exato.

| | Busca por embedding | Busca por palavra-chave (BM25) |
|---|---|---|
| "posso devolver?" achar "política de troca" | ✅ entende o sentido | ❌ nenhuma palavra em comum |
| "erro ERR-4021" achar o trecho exato | ⚠️ pode trazer o erro vizinho | ✅ acha o termo exato |

A **busca híbrida** roda as duas e junta os rankings (um jeito comum de juntar é o *Reciprocal Rank Fusion*, que soma pontos pela posição em cada lista). Não precisa de infra exótica: o próprio **pgvector** no Postgres ([capítulo 15](15-o-que-e-banco-vetorial.md)) e a API de busca da OpenAI já suportam.

Curiosidade: o exemplo [`examples/rag-mini`](../examples/rag-mini) usa contagem de palavras, então ele se comporta como a busca **por palavra-chave**. Teste nele uma pergunta com sinônimo e veja ele errar (é o exercício 1 lá embaixo).

## 3. Re-ranking

Às vezes a busca traz, digamos, os 20 candidatos mais parecidos, mas nem todos são bons, e os melhores não estão no topo. O **re-ranking** é um passo extra: um modelo mais caro e preciso **reordena** esses candidatos por relevância real antes de mandar os melhores pro LLM.

```text
pergunta -> busca rápida (top-20) -> re-ranker reordena -> top-5 vão pro prompt
```

Por que não usar só o re-ranker? Porque ele é lento demais pra comparar a pergunta com a base inteira. A busca rápida faz a peneira grossa; o re-ranker, a fina. Custa um pouco mais de latência e dinheiro, mas melhora bastante a qualidade quando a busca acerta os trechos e erra a ordem.

## 4. Dar contexto ao chunk (*Contextual Retrieval*)

Lembra do problema do chunk pequeno? "A receita cresceu 3% em relação ao trimestre anterior": receita **de quem**? **Qual** trimestre? Sozinho, o chunk perdeu o contexto, e a busca sofre.

A ideia do *Contextual Retrieval* (publicada pela Anthropic em 2024) é simples: **antes** de gerar o embedding, um LLM escreve uma frase curta situando o chunk dentro do documento, e essa frase é grudada no começo dele:

```text
ANTES:  "A receita cresceu 3% em relação ao trimestre anterior."

DEPOIS: "Trecho do relatório da ACME sobre o 2º trimestre de 2023;
         a receita do trimestre anterior foi de US$ 314 milhões.
         A receita cresceu 3% em relação ao trimestre anterior."
```

Nos testes deles, buscando os 20 melhores trechos:

| Técnica | Redução nas buscas que falharam |
|---|---|
| Contexto no chunk (só embeddings) | 35% |
| + busca por palavra-chave (híbrida) | 49% |
| + re-ranking | 67% |

A lição por trás dos números: as técnicas **se somam**. Mas repare no custo: gerar o contexto exige uma chamada de LLM **por chunk** na hora de indexar. Com milhares de chunks, isso pesa (o **prompt caching** ajuda bastante, porque o documento inteiro se repete em cada chamada).

## 5. Montando um prompt melhor

Se a sua planilha diz que o trecho certo **veio** mas a resposta saiu errada, o problema está na geração. Compare o prompt básico do capítulo 14 com este, que segue o que a documentação dos provedores recomenda:

```text
<documentos>
  <documento fonte="politica-de-trocas.md">
    Trocas e devoluções: o cliente tem até 7 dias corridos após o
    recebimento para solicitar devolução por arrependimento.
  </documento>
  <documento fonte="entregas.md">
    Entrega: o prazo padrão é de 5 a 10 dias úteis, variando conforme a região.
  </documento>
</documentos>

Responda a pergunta usando APENAS os documentos acima.
Se a resposta não estiver neles, diga "não encontrei isso nos documentos".
No fim, cite a fonte (o nome do arquivo) que você usou.

Pergunta: Comprei uma blusa ontem, ainda dá pra devolver?
```

O que mudou e por quê:

- **Cada trecho marcado com tags e a fonte** (`<documento fonte="...">`): o modelo enxerga onde começa e termina cada trecho, e consegue **dizer de onde tirou** a resposta.
- **Documentos em cima, pergunta embaixo**: a Anthropic relata que, com documentos longos, colocar a pergunta **no fim** melhora a qualidade da resposta em até **30%** nos testes dela.
- **Saída "não encontrei" explícita**: dá ao modelo uma resposta honesta pra quando o trecho certo não veio. Sem isso, ele tende a chutar.

É exatamente o formato que a função `montar_prompt` do [`examples/rag-mini`](../examples/rag-mini) gera.

> 💡 Alguns provedores já fazem a citação por você: a API da Anthropic tem um recurso de **Citations** que devolve o trecho exato do documento que sustenta cada frase da resposta.

### Cuidado com a ordem: "perdido no meio"

Mandar mais trechos nem sempre ajuda. Um estudo de 2023 (*Lost in the Middle*, Liu et al.) mostrou que os modelos usam melhor a informação que está no **começo ou no fim** do contexto, e pioram quando o trecho importante fica **no meio** de muitos outros. Na prática: não encha o prompt com 50 trechos "por garantia", e coloque os **mais relevantes nas pontas**.

## Outro caminho: uma wiki que a própria IA mantém

Repare num detalhe do RAG: a cada pergunta, o modelo **redescobre** o conhecimento do zero. Ele busca pedaços soltos, junta, responde... e esquece. Na pergunta seguinte, começa tudo de novo. Nada se acumula.

Em 2026, Andrej Karpathy popularizou uma alternativa chamada **LLM-wiki**: em vez de buscar trechos crus na hora da pergunta, você pede pra IA **compilar o conhecimento antes**, numa pasta de arquivos markdown que ela mesma escreve e mantém atualizada.

```text
fontes/            <- documentos originais (a IA só lê, nunca edita)
wiki/
├── index.md       <- catálogo: cada página com link + resumo de uma linha
├── log.md         <- histórico do que foi adicionado e quando
├── clientes.md    <- páginas de conceito, ligadas entre si por links
└── politica-de-trocas.md
CLAUDE.md          <- as regras de como a wiki é organizada
```

O ciclo tem três operações: **ingerir** (chegou um documento novo, a IA resume e atualiza as páginas relacionadas), **consultar** (a IA lê o `index.md`, abre só as páginas certas e responde citando-as) e **revisar** (de tempos em tempos, a IA procura contradições, páginas desatualizadas e links quebrados).

Você vai reencontrar essa ideia nas [skills do capítulo 19](19-o-que-sao-skills.md): é a mesma **divulgação progressiva**, em que o agent lê um índice curto e abre só o que precisa.

O Google deu um passo além e propôs o **OKF** (*Open Knowledge Format*): uma especificação aberta pra esse tipo de wiki, pra que ela funcione entre ferramentas diferentes. A regra é simples: cada conceito é um arquivo markdown com um cabeçalho YAML (`type`, `title`, `description`, `tags`...), e os conceitos se ligam por links comuns. É **só arquivo**: sem servidor, sem SDK.

Quando usar cada um?

| | RAG | Wiki curada (LLM-wiki / OKF) |
|---|---|---|
| A cada pergunta | Busca trechos crus e monta a resposta | Lê páginas já resumidas e ligadas |
| Conhecimento se acumula? | Não | Sim, a wiki melhora com o tempo |
| Escala | Milhões de trechos | Pequena/média (o próprio Karpathy fala em ~100 fontes, centenas de páginas) |
| Custo de manter | Reindexar quando muda | A IA reescreve páginas a cada fonte nova |
| Risco | Trecho errado recuperado | Um resumo errado da IA vira "verdade" na wiki |

Não é "um ou outro": quando a wiki cresce demais, o próprio Karpathy sugere colocar uma **busca** (híbrida!) por cima dela. E seja honesto com o momento: o OKF ainda está nas primeiras versões (v0.2), sem adoção ampla confirmada. O que vale aprender aqui é o **padrão** (conhecimento curado em markdown, com índice e links), não apostar numa especificação específica.

## Por dentro: uma escada, não um cardápio

Junte tudo e o RAG "de produção" vira uma esteira com vários estágios opcionais:

```text
INDEXAR:   documento -> chunk (pela estrutura) -> [contexto no chunk]
                     -> embedding + índice de palavra-chave

PERGUNTAR: pergunta -> busca híbrida (top-20) -> [re-ranking] -> top-5
                    -> prompt com fontes (docs em cima, pergunta embaixo)
                    -> LLM -> resposta citando a fonte
```

Os itens entre colchetes são degraus, não obrigação. A ordem sensata é: **básico + planilha de avaliação** primeiro; depois, olhando onde a planilha aponta erro, sobe um degrau por vez e mede de novo. Ligar tudo de uma vez, sem medir, é o jeito mais rápido de ter um sistema caro, lento e que você não sabe explicar.

## Seja honesto: os limites

- **Cada degrau custa.** Re-ranking adiciona latência; contexto no chunk adiciona uma chamada de LLM por chunk na indexação; busca híbrida adiciona um segundo índice pra manter.
- **Os números são do teste de alguém.** Os 35%/49%/67% vêm dos dados da Anthropic. Na sua base, o ganho pode ser maior, menor ou nenhum, e só a sua avaliação diz.
- **Nenhuma técnica conserta documento ruim.** Se a informação está desatualizada, contraditória ou nem existe na base, não há chunking ou re-ranking que salve.
- **A planilha também mente se for pequena.** 10 perguntas pegam erros grosseiros; não provam que o sistema está bom em tudo. Cresça o conjunto com os erros que aparecerem em uso real.

## Exercício

1. **Busca híbrida na prática:** rode o [`examples/rag-mini`](../examples/rag-mini) com a pergunta "quero aprender a programar" e depois com "como começo a codar?". Por que a segunda vai pior? Que tipo de busca (embedding ou palavra-chave) resolveria cada uma?
2. **Diagnóstico:** seu RAG respondeu errado "qual o prazo de entrega?". Você abre o log e vê que o chunk de entregas **veio** na busca. O problema está na recuperação ou na geração? O que você mudaria primeiro?
3. **Monte sua planilha:** escolha 5 documentos curtos e escreva 8 perguntas, cada uma com o chunk que deveria ser recuperado (inclua 2 perguntas cuja resposta **não** está nos documentos). Esse é o seu ponto de partida pra medir qualquer melhoria deste capítulo.
4. Pense em 3 situações: (a) o FAQ de uma loja com 40 perguntas; (b) as anotações de estudo de um curso inteiro, que crescem toda semana; (c) 2 milhões de tickets de suporte. Pra cada uma, você usaria "tudo no prompt", RAG ou uma wiki curada? Por quê?

## Referências e para ir mais fundo

Fontes usadas neste capítulo, boas pra quem quer aprofundar (a maioria em inglês):

- **[Introducing Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)** (Anthropic, 2024) — contexto no chunk, busca híbrida e re-ranking, com os números citados aqui.
- **[Long context prompting tips](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)** (documentação da Anthropic) — documentos no topo, pergunta no fim, tags com a fonte.
- **[Citations](https://platform.claude.com/docs/en/build-with-claude/citations)** (documentação da Anthropic) — respostas com o trecho exato que as sustenta.
- **[Retrieval / File search](https://developers.openai.com/api/docs/guides/retrieval)** (documentação da OpenAI) — vector stores, chunking padrão e busca híbrida numa API pronta.
- **[Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172)** (Liu et al., 2023) — por que a posição do trecho no prompt importa.
- **[Ragas: Automated Evaluation of RAG](https://arxiv.org/abs/2309.15217)** (Es et al., 2023) — métricas pra avaliar recuperação e fidelidade.
- **[pgvector](https://github.com/pgvector/pgvector)** — busca vetorial (e híbrida) dentro do PostgreSQL.
- **[Advanced RAG](https://huggingface.co/learn/cookbook/en/advanced_rag)** (Hugging Face Cookbook) — notebook prático, com código, das técnicas de chunking e re-ranking.
- **[LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)** (Andrej Karpathy, 2026) — o texto original do padrão de wiki mantida pela IA.
- **[How the Open Knowledge Format can improve data sharing](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing)** (Google Cloud, 2026) — o anúncio do OKF; a especificação fica em [GoogleCloudPlatform/open-knowledge-format](https://github.com/GoogleCloudPlatform/open-knowledge-format).

---

<div align="center">

[« 15 - O que é Banco Vetorial](15-o-que-e-banco-vetorial.md) — [Índice](../README.md#roadmap) — [17 - O que é um Agent »](17-o-que-e-um-agent.md)

</div>
