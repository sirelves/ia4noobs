# 08 - Como estruturar respostas

Até agora você aprendeu a fazer perguntas melhores. Mas tem outra parte que você pode controlar quase totalmente: **o formato da resposta**.

Você não precisa aceitar aquele "textão" corrido que a IA às vezes despeja. Você manda. Lista, tabela, passo a passo, resumo curtinho, até formatos que outros programas conseguem ler. Vamos ver como.

## Por que controlar o formato?

Pense numa receita. Não adianta a informação estar certa se vem tudo embolado num parágrafo gigante. A forma como a resposta é organizada muda **muito** o quanto ela é útil.

Além disso, pedir um formato específico:

- Facilita a leitura e a comparação de opções.
- Te poupa de reorganizar tudo na mão depois.
- É essencial quando **outra ferramenta** vai ler a resposta (mais sobre isso no fim).

## Peça listas

Ótimas pra tópicos, ideias e itens soltos.

```text
Liste 5 dicas para economizar energia em casa.
Use bullets curtos, no máximo uma linha cada.
```

## Peça tabelas

Perfeitas pra comparar coisas lado a lado.

```text
Compare 3 planos de celular pré-pago em uma tabela com as colunas:
Plano | Preço mensal | Internet | Minutos.
```

## Peça passo a passo

Quando a ordem importa, peça etapas numeradas.

```text
Explique como trocar um pneu de carro em passo a passo numerado,
do início ao fim, para quem nunca fez isso.
```

## Peça resumos com tamanho definido

Você pode amarrar o tamanho da resposta. Isso evita textos longos demais.

```text
Resuma este texto em no máximo 50 palavras.
[cole o texto aqui]
```

Ou ainda mais curto:

```text
Resuma a ideia principal deste artigo em uma única frase.
```

## Defina o tom e o tamanho

A IA se adapta ao estilo que você pedir. Diga se quer formal, informal, divertido, técnico.

```text
Reescreva este e-mail em tom formal e profissional,
mantendo no máximo 3 parágrafos:
[cole o e-mail aqui]
```

```text
Reescreva esta legenda em tom descontraído e divertido,
com no máximo 2 frases e um emoji no final.
```

## Use a ideia de "template"

Um truque ótimo: dê um molde com lacunas pra IA preencher. Assim toda resposta sai no mesmo padrão.

```text
Para cada filme que eu pedir, responda EXATAMENTE neste formato:

Título:
Gênero:
Em uma frase:
Nota (0 a 10):

Primeiro filme: De Volta para o Futuro.
```

Isso é especialmente útil quando você vai pedir várias vezes seguidas e quer respostas padronizadas.

## Peça formatos que máquinas leem (ex.: JSON)

Às vezes a resposta da IA não é pra você ler, e sim pra outro programa usar. Nesses casos, formatos estruturados como **JSON** são ideais, porque seguem um padrão rígido e previsível.

```text
Extraia as informações desta frase e responda APENAS em JSON,
sem texto extra, com as chaves "nome", "idade" e "cidade":

"Joana tem 27 anos e mora em Recife."
```

Resposta esperada:

```text
{
  "nome": "Joana",
  "idade": 27,
  "cidade": "Recife"
}
```

Não se preocupe se você não programa: o ponto é entender que, quando uma ferramenta vai consumir a resposta, pedir um formato estruturado evita bagunça e erros.

## System prompt x mensagem do usuário (em alto nível)

Você vai ouvir falar em **system prompt** (instrução de sistema). De forma simples:

- A **instrução de sistema** define o comportamento geral da IA: "Você é um assistente educado que sempre responde em português." É como o "regulamento da casa".
- A **mensagem do usuário** é o seu pedido do momento: "Me explique fotossíntese."

No chat comum, você quase sempre escreve só a mensagem do usuário. Mas alguns aplicativos e ferramentas (e configurações como "instruções personalizadas") deixam você definir a instrução de sistema, que vale pra conversa inteira. Saber que essa camada existe já ajuda muito a entender por que a IA às vezes "se comporta" de um jeito fixo.

## Resumindo

- Você controla o formato: lista, tabela, passo a passo, resumo, JSON.
- Defina tom e tamanho pra evitar respostas longas ou no estilo errado.
- Use templates pra padronizar respostas repetidas.
- Formatos estruturados (como JSON) são ideais quando outra ferramenta vai ler a resposta.
- A instrução de sistema define o comportamento geral; a mensagem do usuário é o pedido do momento.

## Exercício

1. Faça a mesma pergunta de 3 formas diferentes: pedindo **lista**, depois **tabela**, depois **resumo em uma frase**. Veja qual formato serve melhor pro seu caso.
2. Crie um **template** com lacunas (como o exemplo dos filmes) e peça pra IA preencher com 3 itens diferentes. Confira se ela manteve o padrão.
3. Peça uma resposta **apenas em JSON** extraindo dados de uma frase qualquer que você inventar. Observe se ela respeitou o formato sem texto extra.

---

<div align="center">

[« 07 - Como fazer perguntas melhores](07-como-fazer-perguntas-melhores.md) — [Índice](../README.md#roadmap) — [09 - Principais erros ao usar IA »](09-principais-erros-ao-usar-ia.md)

</div>
