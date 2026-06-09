# 11 - O que é RAG

No capítulo anterior você viu os embeddings. Agora vamos usá-los pra resolver um problema bem real da IA: ela **não conhece os seus documentos**.

A solução pra isso tem nome: **RAG**.

## O problema

Um LLM (o modelo que conversa com você) tem duas limitações importantes:

- **Data de corte**: ele foi treinado até certa data. O que aconteceu depois, ele não sabe.
- **Não conhece os SEUS dados**: o manual interno da sua empresa, suas notas, seus PDFs... nada disso estava no treino.

E o pior: quando o modelo não sabe, muitas vezes ele **não fica calado**. Ele **inventa** uma resposta com cara de verdade. Isso é a famosa **alucinação**.

Então como fazer a IA responder sobre **os seus documentos**, com informação **atualizada** e **confiável**?

## O que significa RAG

**RAG** = **R**etrieval-**A**ugmented **G**eneration.

Em português: **Geração Aumentada por Recuperação**.

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
- Como quebrar os documentos (tamanho dos chunks) faz diferença e dá trabalho de ajustar.

## Exercício

Imagine que você vai montar um RAG pro FAQ de uma loja virtual.

1. Liste 3 documentos que você colocaria no banco (ex: política de troca, prazos de entrega...).
2. Escreva os **5 passos** do fluxo RAG com suas palavras, sem olhar a seção acima.
3. Para a pergunta "Posso devolver um produto depois de 10 dias?", de qual documento o sistema deveria recuperar o trecho? Por quê?

---

<div align="center">

[« 10 - O que são Embeddings](10-o-que-sao-embeddings.md) — [Índice](../README.md#roadmap) — [12 - O que é Banco Vetorial »](12-o-que-e-banco-vetorial.md)

</div>
