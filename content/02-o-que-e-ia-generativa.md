# 02 - O que é IA Generativa

No capítulo anterior vimos o filtro de spam: ele olha um e-mail e responde "spam" ou "não spam". Esse tipo de IA **classifica** ou **prevê** coisas. Ela escolhe entre opções que já existem.

A IA Generativa faz algo diferente: ela **cria conteúdo novo** — um texto, uma imagem, um áudio ou um trecho de código que não existia antes. São duas famílias de modelos com objetivos opostos, e entender a diferença explica quase tudo o que vem depois neste guia.

## Discriminativo vs generativo

Na literatura, o modelo que classifica/prevê é chamado de **discriminativo**, e o que cria é **generativo**. A intuição por trás dos nomes:

- Um modelo **discriminativo** aprende a **traçar a fronteira** entre categorias. Ele responde "de que lado dessa linha isto está?". Não sabe desenhar um gato — só sabe dizer se há um gato na foto.
- Um modelo **generativo** aprende **como os dados são feitos por dentro** e, por isso, consegue produzir exemplos novos que parecem ter vindo do mesmo lugar.

Lado a lado:

| | Discriminativo (classifica/prevê) | Generativo (cria) |
|---|---|---|
| **O que faz** | Decide, rotula, dá uma nota | Produz conteúdo inédito |
| **Saída** | Um rótulo ou número | Texto, imagem, áudio, código |
| **Exemplo de pergunta** | "Isto é spam?" | "Escreva um e-mail educado recusando isto" |
| | "Gato ou cachorro?" | "Crie uma imagem de um gato astronauta" |
| | "Qual o preço deste imóvel?" | "Escreva o anúncio deste imóvel" |
| **Analogia** | O crítico que julga o prato | O cozinheiro que inventa o prato |

Os dois podem viver no mesmo produto: um app usa um modelo discriminativo para **detectar** que sua foto tem um cachorro e um generativo para **escrever** a legenda "Golden Retriever curtindo o sol".

## A ideia central: aprender a distribuição e amostrar dela

Aqui está o coração da IA generativa, em uma frase:

> O modelo aprende como os dados costumam ser (a **distribuição**) e depois **sorteia** um exemplo novo que combina com esse padrão.

"Distribuição" é só o nome técnico para "o jeito como as coisas normalmente aparecem". Depois de ver milhões de fotos de gatos, o modelo tem uma noção do que faz um gato parecer um gato: orelhas, bigodes, proporções. Ele não guardou as fotos — guardou o **padrão**. Gerar é **amostrar** desse padrão: puxar um exemplo plausível que ninguém tinha visto antes.

O mecanismo de amostragem muda conforme o tipo de conteúdo. Vamos ver os dois mais importantes — **texto** e **imagem** —, que funcionam de maneiras bem diferentes.

## Texto: prever o próximo token, de novo e de novo

Para texto, o mecanismo é simples de enunciar: **prever qual é o próximo pedaço de texto, repetir, repetir.** Esses pedaços são chamados de **tokens** (dedicamos o [capítulo 05](05-o-que-sao-tokens.md) inteiro a eles — por ora, pense em "pedaço de palavra"). O modelo olha tudo o que já existe na frase, produz uma **probabilidade** para cada token que poderia vir a seguir, **escolhe um**, cola no fim do texto e recomeça — agora com o token novo fazendo parte da entrada.

Um exemplo passo a passo, começando pela frase "O céu está":

```text
Passo 1 — entrada: "O céu está"
   candidatos e probabilidades (ILUSTRATIVO, não são números reais):
      " azul"     → 60%
      " nublado"  → 25%
      " limpo"    →  8%
   escolhe → " azul"

Passo 2 — entrada: "O céu está azul"
      " e"        → 40%
      " hoje"     → 30%
   escolhe → " e"

Passo 3 — entrada: "O céu está azul e"  →  escolhe " o"  →  ... e repete até parar.
```

É só isso, repetido centenas de vezes. Nenhuma frase é planejada de uma vez — ela é **construída um token por vez**. É por isso que a resposta aparece "digitando" na tela: cada palavrinha é uma escolha recém-feita. E é a mesma razão pela qual o modelo às vezes começa uma frase bonita e se perde no meio: ele não sabia o fim quando escolheu o começo.

## Imagem: partir do ruído e ir limpando (difusão)

Para imagem, o truque é **completamente diferente**. Não existe "próximo pixel" da esquerda para a direita. O mecanismo mais comum hoje se chama **difusão** (*diffusion*), e a intuição é linda:

> O modelo aprende a **remover ruído**. Ele começa com uma tela de puro chiado aleatório — como a "chuvinha" de uma TV velha — e vai limpando esse chiado passo a passo, até sobrar uma imagem nítida.

Como ele aprendeu isso? No treino, pegaram imagens reais e foram **borrando** cada uma com ruído até virar chiado total. O modelo treinou para desfazer esse processo: dado um borrão, prever como ele era um passo antes, menos borrado. Repetindo essa "des-borração" muitas vezes, ele parte do chiado puro e chega a uma imagem.

O seu texto (o *prompt*) entra como um **guia**: a cada passo de limpeza, ele empurra o resultado na direção de "gato astronauta". O chiado que vira gato é diferente do que vira paisagem — o texto é quem decide.

```text
Puro ruído  →  [remove um pouco]  →  [remove mais]  →  ...  →  imagem nítida
  ▓▒░▓▒░         formas vagas          silhueta            "gato astronauta"
   (guiado o tempo todo pelo seu prompt de texto)
```

Guarde a diferença: **texto se constrói acrescentando** (um token de cada vez); **imagem se constrói removendo** (ruído, passo a passo). Quando um mesmo modelo junta vários tipos — texto **e** imagem **e** áudio — chamamos de **multimodal**, tema do [capítulo 03](03-ia-multimodal.md).

## Por dentro: por que o mesmo prompt dá respostas diferentes

Você já deve ter notado: mande o mesmo pedido duas vezes e recebe respostas distintas. Isso não é bug — é o efeito direto da palavra **amostrar**.

Volte ao passo 1 do texto: `" azul"` tinha 60% e `" nublado"` 25%. Se o modelo **sempre** pegasse o mais provável, a resposta seria idêntica toda vez — robótica e repetitiva. Em vez disso, ele faz um **sorteio ponderado**: quase sempre sai `" azul"`, mas às vezes sai `" nublado"`. Uma escolha diferente no começo leva a uma frase inteira diferente no fim.

O parâmetro que controla o quanto ele "arrisca" se chama **temperatura**:

- **Temperatura baixa** (perto de 0): quase sempre pega o token de maior probabilidade. Saída mais **previsível e conservadora**. Boa para tarefas objetivas (extrair um dado, seguir um formato).
- **Temperatura alta**: dá mais chance aos tokens menos prováveis. Saída mais **variada e criativa** — e mais propensa a viajar.

Na difusão de imagens acontece algo equivalente: o ruído inicial é aleatório (controlado por um número chamado *seed*), então cada geração parte de um chiado diferente e chega a uma imagem diferente. Mesmo *seed* + mesmo prompt tende a repetir a imagem.

Ou seja: a variação **é o funcionamento normal**, não uma falha. Um modelo generativo é uma máquina de sortear coisas plausíveis.

## Os limites: plausível não é o mesmo que verdadeiro

Aqui mora o aviso mais importante do capítulo:

> A IA generativa é otimizada para produzir o que é **provável** — não o que é **verdadeiro**.

Na maioria das vezes o provável coincide com o correto, mas nem sempre — e, quando não coincide, o modelo continua gerando com toda a confiança do mundo. Consequências concretas:

- **Alucinação.** É exatamente o "gerar o mais provável" que faz o modelo **inventar** fatos, datas, citações e links que soam perfeitos e não existem. Para ele, uma fonte falsa com formato convincente é tão "provável" quanto uma real. Trataremos disso a fundo mais à frente no guia.
- **Erros de conta.** Como ele prevê o texto plausível de uma resposta em vez de calcular, erra contas simples com cara de certeza absoluta.
- **Vieses.** Ele aprende os padrões do treino — inclusive os preconceitos que estavam lá — e pode reproduzir estereótipos sem "querer".
- **Direitos autorais.** Normalmente ele **não copia trechos literais** (não é um banco de dados que cola do original), mas, por ter aprendido com obras existentes, pode gerar algo perto demais de um estilo ou conteúdo protegido. Área jurídica ainda em aberto.

A síntese prática: **criativo não é o mesmo que correto.** Use a IA generativa como um assistente rápido e incansável — e confira o que for importante. Ela acelera o seu trabalho; não substitui o seu senso crítico.

## Exercício

1. **Classifique as tarefas.** Para cada item, diga se pede um modelo **discriminativo** ou **generativo**: (a) marcar um comentário como ofensivo; (b) escrever uma resposta educada a esse comentário; (c) prever se um cliente vai cancelar a assinatura; (d) criar o texto do e-mail que tenta reter esse cliente.
2. **Veja a variação na prática.** Abra um chat de IA (ChatGPT, Claude ou Gemini) e mande **três vezes** o mesmo prompt, começando um chat novo a cada vez — por exemplo: "Escreva uma frase de abertura para um post sobre café." Compare as três saídas. Onde elas mudaram? Conecte isso com a ideia de amostragem e temperatura.
3. **Provoque uma alucinação com cuidado.** Peça: "Cite três artigos científicos sobre um tema bem específico e nichado, com autores e ano." Depois tente confirmar se existem. O que isso te ensina sobre "plausível ≠ verdadeiro"?

---

<div align="center">

[« 01 - O que é Inteligência Artificial](01-o-que-e-inteligencia-artificial.md) — [Índice](../README.md#roadmap) — [03 - IA Multimodal »](03-ia-multimodal.md)

</div>
