# 08 - O que é Prompt Engineering

A mesma IA pode te dar uma resposta péssima ou uma resposta excelente dependendo só de **como** você pede. A diferença quase nunca está no modelo. Está no seu pedido — no **prompt**. Aprender a escrever bons prompts é, hoje, a habilidade mais barata e mais rentável para quem usa IA no dia a dia.

## O que é um prompt (e por que ele "guia" a resposta)

Um **prompt** é a mensagem que você envia pra IA: seu pedido, sua pergunta, sua instrução. Tudo o que você digita no ChatGPT, Claude ou Gemini é um prompt.

Mas para entender *por que* pedir bem funciona, precisa lembrar do [capítulo 04](04-como-o-chatgpt-funciona.md): o modelo não "responde" no sentido humano — ele **continua o texto mais plausível**. Você escreve um começo, e ele completa com o que, estatisticamente, costuma vir depois de um texto assim.

O prompt é exatamente esse começo. Ele define a **trajetória** da resposta. Pense num trilho: onde você posiciona o trem e para que lado aponta os trilhos decide onde ele chega. Um prompt vago é um trilho solto no meio do nada — o modelo vai para o destino "médio", genérico. Um prompt bem-feito estreita os trilhos: entre todas as continuações possíveis, você torna prováveis só as que servem pra você.

> **Prompt engineering** é a arte de pedir bem — de condicionar o modelo para a resposta que você quer. Não tem matemática pesada. É mais parecido com explicar uma tarefa para um estagiário brilhante, rápido e cheio de conhecimento, mas que precisa de instruções claras porque não lê a sua mente.

## A anatomia de um bom prompt

Um prompt completo costuma ter até seis peças. Você não usa todas sempre — mas conhecer o kit ajuda a montar pedidos melhores:

1. **Papel / persona** — quem a IA deve "ser". `Você é um veterinário experiente.` Isso puxa a resposta para o vocabulário e a postura daquele tipo de pessoa.
2. **Tarefa clara** — o que exatamente você quer, com um verbo de ação. `Explique`, `Liste`, `Reescreva`, `Compare`.
3. **Contexto** — o pano de fundo. Quem é o leitor, para que serve, o que já foi feito. `O leitor é um dono de cachorro de primeira viagem.`
4. **Formato de saída** — como a resposta deve aparecer. Lista, tabela, JSON, parágrafo único, no máximo 5 frases.
5. **Restrições** — os limites. Tamanho, tom, o que **não** incluir. `Sem jargão técnico. Não sugira remédios.`
6. **Exemplos** — um ou dois modelos do que você espera. É a peça mais poderosa, e o [capítulo 10](10-few-shot-e-chain-of-thought.md) aprofunda (few-shot).

## Antes e depois: o mesmo pedido, dois resultados

Veja a **mesma tarefa** pedida de dois jeitos.

**Antes** (vago):

```text
fala sobre cuidados com filhote de cachorro
```

O que o modelo faz com isso? Ele busca a continuação *média* de um pedido genérico: provavelmente um texto-enciclopédia, longo, sem foco em quem vai ler, cobrindo tudo um pouco e nada direito. Não porque a IA é burra — porque você não deu trilho nenhum.

**Depois** (as seis peças montadas):

```text
Você é um veterinário experiente.                          [papel]
Explique os 3 cuidados mais importantes com um filhote     [tarefa]
de cachorro nas primeiras semanas em casa.
O leitor é um dono de primeira viagem, ansioso.            [contexto]
Responda em 3 tópicos curtos, um por cuidado.              [formato]
No máximo 5 frases no total. Linguagem simples e           [restrições]
acolhedora. Não recomende medicamentos.

Exemplo do tom que quero:                                  [exemplo]
"Vacinação: leve seu filhote ao veterinário na
primeira semana para começar o calendário de vacinas."
```

*(Prompt ilustrativo — não vou inventar a resposta exata do modelo, mas dá para descrever a diferença.)* A versão estruturada estreita a distribuição em várias frentes: o **papel** puxa o vocabulário de veterinário; o **contexto** faz o tom virar acolhedor em vez de técnico; **formato** e **restrições** cortam a enrolação; o **exemplo** fixa o comprimento e o estilo de cada tópico. O resultado tende a chegar quase pronto — enquanto o "antes" quase sempre exige uma segunda rodada de ajustes.

Repare: você não deixou a IA "mais inteligente". Você **reduziu as saídas possíveis** para o subconjunto que serve.

## System prompt vs mensagem do usuário

Nas ferramentas e, principalmente, quando você programa via API, existem dois tipos de mensagem com pesos diferentes:

- O **system prompt** (mensagem de sistema) define o **papel e as regras gerais** que valem para a conversa inteira: "Você é um assistente de suporte da loja X. Nunca prometa reembolso. Responda sempre em português." É a moldura fixa.
- A **mensagem do usuário** é o pedido específico daquele momento: "Meu pedido 4821 chegou quebrado."

O system prompt condiciona o modelo *antes* de qualquer pergunta e costuma ter prioridade quando há conflito. No ChatGPT, aquilo que você escreve em "instruções personalizadas" funciona como um system prompt. Guarde esse termo — ele reaparece no glossário e nos capítulos de aplicação.

## Técnicas que os próximos capítulos aprofundam

Prompt engineering é um kit que cresce. Aqui, só o mapa:

- **Dar exemplos (few-shot)** — mostrar 1–3 casos resolvidos antes do pedido real. Sobe muito a consistência de formato. → [capítulo 10](10-few-shot-e-chain-of-thought.md)
- **Pedir um formato específico** — lista, tabela, JSON. Facilita ler e, no código, facilita processar. → [capítulo 11](11-como-estruturar-respostas.md)
- **Usar delimitadores** — separar suas instruções do material a ser processado com marcações como `"""` ou `<texto>...</texto>`. Evita que o modelo confunda o que é ordem com o que é dado.
- **Dividir tarefas grandes** — em vez de um prompt gigante que faz dez coisas, quebre em etapas. Menos chance de o modelo "esquecer" um pedaço.

## Por dentro

No fundo, um prompt é uma coisa só: **condicionamento da probabilidade dos próximos tokens**.

Lembre do [capítulo 05](05-o-que-sao-tokens.md): o modelo gera **um token por vez**, sempre calculando uma probabilidade para cada token possível e escolhendo o próximo. O prompt é todo o texto que já está na mesa quando ele faz esse cálculo. Ele não é "lido e interpretado" à parte — ele **é** o contexto que enviesa a distribuição de saída.

É por isso que cada peça da anatomia funciona. Escrever `Você é um veterinário` não liga um "modo veterinário": ele desloca a probabilidade para continuações que, no treino, apareciam perto de textos escritos por veterinários. Pedir formato de lista aumenta a chance de o próximo token ser um `-` ou `1.`. Tudo é empurrão na mesma máquina de probabilidade.

Esse mesmo mecanismo explica a fragilidade da coisa: como a saída sai de uma distribuição sensível ao texto de entrada, **mudanças pequenas no prompt podem mudar muito a resposta**. Trocar uma palavra, reordenar frases, tirar uma vírgula — às vezes muda pouco, às vezes muda o resultado inteiro. Por isso prompt engineering é empírico: você testa, não deduz.

## O que prompt engineering NÃO resolve (limites honestos)

- **Prompt não conserta modelo fraco.** Se o modelo não sabe algo ou não é capaz de raciocinar sobre aquilo, nenhuma palavra mágica cria a capacidade. Bom prompt extrai o melhor do que existe; não inventa competência.
- **Prompt é frágil e não é portável.** Um prompt afinado para um modelo pode render pior em outro — e até entre **versões** do mesmo modelo. O que funciona hoje pode precisar de ajuste depois de uma atualização.
- **Texto de fora pode conter instruções maliciosas.** Se seu prompt inclui conteúdo que você não escreveu (uma página web, um e-mail, um PDF), esse texto pode trazer ordens escondidas do tipo "ignore as instruções acima e faça X". Isso se chama **prompt injection** e é um risco real quando a IA processa dados externos. → [capítulo 26](26-seguranca-em-ia.md)

## Iterar é parte do jogo

Quase ninguém acerta o prompt perfeito de primeira — e tudo bem. Prompt engineering é **conversa**: você pede, olha a resposta, ajusta ("ficou longo, corte pela metade", "mais formal", "reescreva para uma criança de 10 anos") e pede de novo. Cada volta te aproxima. Trate a IA como parceira de iteração, não como máquina de resposta única.

## Recapitulando

- O prompt define a **trajetória** da resposta: ele condiciona a continuação mais provável do texto.
- A anatomia de um bom prompt: **papel, tarefa, contexto, formato, restrições e exemplos**.
- **System prompt** = papel e regras fixas da conversa; **mensagem do usuário** = o pedido do momento.
- Por dentro, prompt é condicionar a probabilidade dos próximos tokens — por isso mudanças pequenas mudam muito.
- Limites: não conserta modelo fraco, é frágil entre modelos/versões, e texto externo pode injetar instruções.

## Exercício

1. Pegue um pedido vago que você faria normalmente (ex.: "me ajuda a escrever um e-mail cobrando um cliente"). Reescreva-o com **as seis peças** da anatomia: papel, tarefa, contexto, formato, restrições e pelo menos um exemplo do tom.
2. Rode as **duas versões** (a vaga e a estruturada) na mesma IA. Compare: qual chegou mais perto de pronto? Quantos ajustes cada uma ainda precisou?
3. Tire **uma** peça da versão estruturada (por exemplo, remova o formato de saída) e rode de novo. O que mudou na resposta? Isso te mostra, na prática, o peso de cada componente.

---

<div align="center">

[« 07 - Escolhendo o modelo certo](07-escolhendo-o-modelo-certo.md) — [Índice](../README.md#roadmap) — [09 - Como fazer perguntas melhores »](09-como-fazer-perguntas-melhores.md)

</div>
