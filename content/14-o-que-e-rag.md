# 14 - O que é RAG

No capítulo anterior você viu os embeddings. Agora vamos usá-los pra resolver um problema bem real da IA: ela **não conhece os seus documentos**.

A solução pra isso tem nome: **RAG**.

## O problema

Um LLM (o modelo que conversa com você) tem duas limitações importantes:

- **Data de corte**: ele foi treinado até certa data. O que aconteceu depois, ele não sabe.
- **Não conhece os SEUS dados**: o manual interno da sua empresa, suas notas, seus PDFs... nada disso estava no treino.

E o pior: quando o modelo não sabe, muitas vezes ele **não fica calado**. Ele **inventa** uma resposta com cara de verdade. Isso é a famosa **alucinação** (vimos ela no [capítulo 12](12-principais-erros-ao-usar-ia.md)).

Então como fazer a IA responder sobre **os seus documentos**, com informação **atualizada** e **confiável**?

## O que significa RAG

**RAG** = **R**etrieval-**A**ugmented **G**eneration. Em português: **Geração Aumentada por Recuperação**.

Quebrando o nome:

- **Recuperação (Retrieval)**: buscar os trechos certos dos seus documentos.
- **Aumentada (Augmented)**: enriquecer a pergunta com esses trechos.
- **Geração (Generation)**: o LLM gera a resposta usando esse material.

A ideia em uma frase:

> Em vez de pedir pro modelo responder "de cabeça", a gente **entrega o material certo junto da pergunta** e pede pra ele responder com base naquilo.

É como fazer uma prova com **consulta**: você não precisa decorar tudo, só precisa achar a página certa na hora.

## O fluxo passo a passo

O RAG tem duas fases. A primeira é a **preparação** (feita uma vez, antes das perguntas):

```
DOCUMENTOS (PDFs, textos, páginas)
        |
        v
[1] Quebrar em pedaços menores (chunks)
        |
        v
[2] Gerar embedding de cada pedaço
        |
        v
   Guardar os vetores  ->  [ Banco Vetorial ]
```

A segunda é o que acontece **a cada pergunta**:

```
PERGUNTA DO USUÁRIO
        |
        v
[3] Buscar no banco os pedaços mais parecidos (semânticos)
        |
        v
[4] Montar um prompt:  trechos encontrados + pergunta
        |
        v
[5] LLM lê os trechos e RESPONDE baseado neles
        |
        v
RESPOSTA (de preferência citando a fonte)
```

Resumindo os 5 passos:

1. **Quebrar** os documentos em pedaços (chunks).
2. **Gerar embeddings** de cada pedaço e **guardar**.
3. Na pergunta, **buscar** os pedaços mais relevantes.
4. **Montar um prompt** com esses trechos + a pergunta.
5. O LLM **responde** com base neles.

Agora vamos abrir cada peça e ver **por que** ela existe.

## Peça 1: Chunking (quebrar em pedaços)

Por que não jogar o documento inteiro no prompt? Dois motivos: **contexto** e **custo**. Um manual de 200 páginas não cabe na janela de contexto do modelo, e mesmo que coubesse, você pagaria por todos aqueles tokens em **toda** pergunta (lembra do [capítulo 05](05-o-que-sao-tokens.md)?). A graça do RAG é recuperar só os **trechos relevantes**.

Então a gente pica o documento em pedaços chamados **chunks** (um parágrafo, algumas frases, uma seção). E qual o tamanho ideal? Aqui tem um **trade-off** que você vai sentir na prática:

- **Chunk grande** (ex: uma página inteira): carrega bastante contexto ao redor, mas a busca fica **menos precisa** — o pedaço tem muito assunto misturado, e o vetor dele vira uma "média" de tudo.
- **Chunk pequeno** (ex: uma frase): a busca fica **mais precisa** e certeira, mas o pedaço pode **perder o contexto** ao redor (a frase "o prazo é de 7 dias" não diz prazo de quê).

Um truque comum é usar **overlap** (sobreposição): fazer os chunks se cruzarem um pouco — o fim de um chunk repete no começo do próximo — pra não cortar uma ideia exatamente no meio.

## Peça 2: Embeddings + busca

Aqui entra tudo do [capítulo 13](13-o-que-sao-embeddings.md). Cada chunk vira um **vetor** (embedding) que captura o **significado** daquele texto. Na hora da pergunta, a **pergunta também vira um vetor**, com o mesmo modelo.

Aí a busca é geométrica: procuramos os vetores de chunk **mais parecidos** com o da pergunta, usando **similaridade de cosseno** (o ângulo entre os vetores). Não pegamos só o melhor — pegamos os **top-k** (os `k` mais parecidos, ex: os 3 ou 5 melhores). Assim, se a resposta estiver espalhada em dois trechos, os dois entram.

Repare: a busca é por **significado**, não por palavra igual. A pergunta "posso devolver?" casa com um chunk que fala em "política de troca" mesmo sem a palavra "devolver" aparecer.

## Peça 3: Montagem do prompt (exemplo trabalhado)

Essa é a parte que junta tudo. Vamos ver **concretamente**, com um mini-documento de exemplo.

> ⚠️ **Exemplo ilustrativo** — chunks e pergunta inventados pra mostrar o mecanismo.

Suponha que o FAQ da loja, depois do chunking, virou 3 chunks:

```text
chunk A: "Trocas e devoluções: o cliente tem até 7 dias corridos após
          o recebimento para solicitar devolução por arrependimento."
chunk B: "Entrega: o prazo padrão é de 5 a 10 dias úteis, variando
          conforme a região."
chunk C: "Formas de pagamento: aceitamos cartão, Pix e boleto."
```

A pergunta do usuário:

```text
"Comprei uma blusa ontem, ainda dá pra devolver?"
```

A busca por similaridade de cosseno compara o vetor da pergunta com os 3 chunks. O **chunk A** vence com folga (fala de devolução e prazo), mesmo sem repetir a palavra "blusa" nem "ontem". Com `k=1`, recuperamos só o A. O prompt final montado fica assim:

```text
Use APENAS os trechos abaixo para responder. Se a resposta não estiver
neles, diga que não sabe.

Trechos:
- "Trocas e devoluções: o cliente tem até 7 dias corridos após o
   recebimento para solicitar devolução por arrependimento."

Pergunta: Comprei uma blusa ontem, ainda dá pra devolver?
```

Esse texto inteiro é o que vai pro LLM. Ele não precisa "saber" a política da sua loja — a política está ali, na cara dele. A instrução **"responda só com base nos trechos"** é o que segura o modelo pra não inventar.

### Passo opcional: re-ranking

Às vezes a busca vetorial traz, digamos, os 20 candidatos mais parecidos, mas nem todos são bons. O **re-ranking** é um passo extra: um modelo mais caro e preciso **reordena** esses candidatos por relevância real antes de mandar os melhores pro LLM. Custa um pouco mais, mas melhora bastante a qualidade quando a busca simples erra a ordem.

## Por dentro: por que RAG reduz alucinação

Lembra do [capítulo 04](04-como-o-chatgpt-funciona.md): o modelo funciona **prevendo o próximo token** a partir do que aprendeu no treino. Quando você pergunta algo que ele não viu direito, ele **não tem de onde puxar** — então prevê tokens plausíveis, que soam certos mas podem ser pura invenção. É a alucinação do [capítulo 12](12-principais-erros-ao-usar-ia.md).

O RAG muda o jogo: coloca **a informação certa dentro do prompt**. Agora o modelo responde **com consulta** — em vez de chutar de memória, ele lê o trecho na hora. Isso se chama **grounding** (aterrar a resposta em uma fonte). Não é que o modelo ficou mais inteligente; é que a resposta certa parou de depender da memória dele e passou a depender do texto que você entregou.

## Por que isso ajuda tanto?

- **Menos alucinação**: o modelo responde olhando o material, não chutando.
- **Dados atualizados**: é só atualizar os documentos no banco. Não precisa retreinar nada.
- **Respostas com fonte**: dá pra mostrar de qual trecho/documento veio a resposta.
- **Controle**: você decide quais documentos a IA pode consultar.

## RAG vs Fine-tuning (em alto nível)

Você vai ouvir falar de **fine-tuning** (ajuste fino). É outra forma de adaptar um modelo. Em alto nível:

| | RAG | Fine-tuning |
|---|---|---|
| O que faz | Consulta documentos na hora | Reajusta o modelo com novos dados |
| Atualizar dados | Fácil (troca os documentos) | Difícil (treina de novo) |
| Mostra a fonte | Sim, dá pra citar | Não diretamente |
| Bom pra | Conhecimento que muda, FAQs, manuais | Mudar **estilo**, formato, tom de voz |
| Custo de mudar | Baixo | Alto |

Regra prática pra começar: se o problema é **"o modelo não conhece minha informação"**, comece por **RAG**. Fine-tuning resolve mais o "**como**" o modelo responde do que "**o que**" ele sabe.

## Seja honesto: os limites

- RAG **reduz** a alucinação, mas não zera. Se o trecho recuperado estiver errado, a resposta sai errada.
- A qualidade depende muito da **busca**: se os pedaços recuperados forem ruins, a resposta será ruim. ("Lixo entra, lixo sai.")
- Como quebrar os documentos (tamanho dos chunks, overlap) faz diferença e **dá trabalho de ajustar** — não existe número mágico, você testa.

## Onde ver isso na prática

- O exemplo [`examples/rag-mini`](../examples/rag-mini) implementa a **busca** (peças 1 e 2): quebra um texto em chunks, gera embeddings e recupera os mais parecidos com a pergunta.
- No [capítulo 15 - Banco Vetorial](15-o-que-e-banco-vetorial.md) você vê onde os vetores ficam guardados e como a busca escala.
- No [capítulo 29 - Projeto final](29-projeto-final-faq-rag.md) a gente monta um FAQ com RAG de ponta a ponta.

## Exercício

1. Imagine que você vai montar um RAG pro FAQ de uma loja virtual. Liste 3 documentos que você colocaria no banco (ex: política de troca, prazos de entrega...).
2. Escreva os **5 passos** do fluxo RAG com suas palavras, sem olhar as seções acima.
3. Para a pergunta "Posso devolver um produto depois de 10 dias?", de qual documento o sistema deveria recuperar o trecho? Por quê?
4. Pense no **tamanho do chunk**: se você quebrasse a política de troca em pedaços de uma frase só, que problema poderia aparecer numa pergunta como "qual o prazo?"? E se o chunk fosse a página inteira, o que pioraria na busca?

---

<div align="center">

[« 13 - O que são Embeddings](13-o-que-sao-embeddings.md) — [Índice](../README.md#roadmap) — [15 - O que é Banco Vetorial »](15-o-que-e-banco-vetorial.md)

</div>
