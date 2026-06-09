# 06 - O que é Prompt Engineering

Você já parou pra pensar que a mesma IA pode te dar uma resposta péssima ou uma resposta excelente, dependendo só de **como** você pede? Pois é. A diferença não está na IA. Está no seu pedido.

Neste capítulo você vai entender o que é um prompt e por que aprender a pedir bem é talvez a habilidade mais útil pra quem usa IA no dia a dia.

## O que é um prompt?

Um **prompt** é simplesmente a mensagem que você envia pra IA. É o seu pedido, sua pergunta, sua instrução. Tudo o que você digita no ChatGPT, Claude ou Gemini é um prompt.

Quando você escreve "me dê uma receita de bolo", isso é um prompt. Curto e simples. Mas prompts podem ser bem mais elaborados, e é aí que a mágica acontece.

## O que é "prompt engineering"?

O nome assusta, mas a ideia é tranquila. **Prompt engineering é a arte de pedir bem.** É aprender a escrever pedidos que fazem a IA entregar exatamente o que você precisa.

Não tem nada de engenharia pesada nem matemática. É mais parecido com aprender a explicar uma tarefa pra um estagiário muito esforçado, mas que precisa de instruções claras pra acertar.

## Por que isso importa?

Veja a mesma intenção pedida de dois jeitos diferentes.

Prompt fraco:

```text
fala sobre cachorro
```

A IA vai responder algo genérico, talvez uma enciclopédia chata sobre cachorros, e provavelmente não é o que você queria.

Prompt bem estruturado:

```text
Você é um veterinário experiente.
Escreva um texto curto (máximo 5 frases) explicando para um dono
de primeira viagem os 3 cuidados mais importantes com um filhote
de cachorro nas primeiras semanas em casa.
Use linguagem simples e acolhedora.
```

Sentiu a diferença? Mesma IA, resultado muito melhor. Você guiou a resposta.

## Os componentes de um bom prompt

Não precisa usar todos sempre, mas conhecer essas "peças" ajuda a montar pedidos melhores:

- **Papel / Persona**: diga quem a IA deve "ser". Ex.: "Você é um professor de história paciente."
- **Contexto**: dê informações de fundo. Ex.: "Estou estudando para uma prova do ensino médio."
- **Tarefa clara**: o que exatamente você quer. Ex.: "Resuma a Revolução Francesa."
- **Formato de saída**: como a resposta deve aparecer. Ex.: "Em forma de lista com 5 tópicos."
- **Exemplos**: mostre um modelo do que espera (veremos abaixo).

Juntando tudo:

```text
Você é um professor de história paciente. [papel]
Estou estudando para uma prova do ensino médio. [contexto]
Resuma as causas da Revolução Francesa. [tarefa]
Responda em uma lista de 5 tópicos curtos. [formato]
```

## Zero-shot vs few-shot

Esses dois termos aparecem bastante. São mais simples do que parecem.

**Zero-shot** significa pedir sem dar nenhum exemplo. Você só descreve a tarefa:

```text
Classifique este comentário como POSITIVO ou NEGATIVO:
"O atendimento foi rápido e simpático."
```

**Few-shot** significa dar alguns exemplos antes de fazer o pedido real. Isso ensina a IA o padrão que você quer:

```text
Classifique os comentários como POSITIVO ou NEGATIVO.

Comentário: "Adorei, voltarei sempre!" -> POSITIVO
Comentário: "Demorou demais e veio frio." -> NEGATIVO
Comentário: "O atendimento foi rápido e simpático." ->
```

Quando a tarefa é mais difícil ou você quer um formato bem específico, few-shot costuma dar resultados mais consistentes. Os exemplos funcionam como uma "demonstração".

## Iterar é parte do jogo

Aqui vai um segredo: quase ninguém acerta o prompt perfeito de primeira. E tudo bem.

Prompt engineering é **conversa**. Você pede, vê a resposta, ajusta e pede de novo. Coisas como:

- "Ficou longo demais, resuma pela metade."
- "Mude o tom para mais formal."
- "Reescreva como se eu tivesse 10 anos de idade."

Cada ajuste te aproxima do resultado ideal. Trate a IA como uma parceira de iteração, não como uma máquina de respostas únicas.

## Resumindo

- Prompt é a mensagem que você envia pra IA.
- Prompt engineering é a habilidade de pedir bem.
- Um bom prompt costuma ter papel, contexto, tarefa clara, formato e (às vezes) exemplos.
- Zero-shot = sem exemplos. Few-shot = com alguns exemplos.
- Iterar é normal e esperado. Ajuste até ficar bom.

## Exercício

1. Pegue um pedido simples que você faria normalmente (ex.: "me ajuda a escrever um e-mail") e reescreva como um prompt completo, usando pelo menos **papel**, **contexto** e **formato de saída**. Teste os dois na IA e compare.
2. Crie um prompt **few-shot** para classificar mensagens como "URGENTE" ou "PODE ESPERAR", dando 2 exemplos antes do caso real.
3. Faça um pedido qualquer e, depois da resposta, **itere pelo menos 2 vezes** pedindo ajustes (tom, tamanho ou estilo). Observe como a resposta muda.

---

<div align="center">

[« 05 - O que é Janela de Contexto](05-o-que-e-janela-de-contexto.md) — [Índice](../README.md#roadmap) — [07 - Como fazer perguntas melhores »](07-como-fazer-perguntas-melhores.md)

</div>
