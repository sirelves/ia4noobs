# 03 - IA Multimodal

Até agora falamos de IA que lê e escreve **texto**. Mas você provavelmente já viu uma IA descrever uma foto, gerar uma imagem a partir de uma frase ou transcrever um áudio. Isso é **IA multimodal**: modelos que lidam com mais de um tipo de dado. A pergunta interessante é: como a mesma máquina que prevê a próxima palavra consegue "ver" uma foto? A resposta é mais simples e mais elegante do que parece — e é o coração deste capítulo.

## O que é uma "modalidade"

Modalidade é só um nome chique para **um tipo de informação**. Os principais são:

- **Texto** — o que a gente já viu.
- **Imagem** — fotos, prints, desenhos, gráficos.
- **Áudio** — fala, música, sons.
- **Vídeo** — imagem em movimento (com ou sem áudio).

Um modelo **multimodal** entende e/ou gera mais de uma dessas coisas. O ChatGPT, o Claude e o Gemini de hoje, por exemplo, aceitam texto **e** imagem na mesma conversa.

## Entender vs. gerar

Tem uma diferença importante que confunde muita gente. Multimodal pode significar duas direções:

- **Entender (entrada)**: você **manda** uma imagem/áudio e a IA interpreta. Ex: "o que tem nesta foto?", "resuma este áudio".
- **Gerar (saída)**: você pede em texto e a IA **cria** a mídia. Ex: "desenhe um gato astronauta", "leia este texto em voz alta".

Nem todo modelo faz as duas coisas, nem para todas as modalidades. Um modelo pode **ler** imagem mas só **responder** em texto. Outro só **gera** imagem. Vale sempre checar o que a ferramenta específica faz.

| Tarefa | Direção | Exemplo de ferramenta |
|---|---|---|
| Descrever uma foto | Imagem → texto | ChatGPT, Claude, Gemini |
| Criar uma imagem | Texto → imagem | DALL·E, Midjourney, Stable Diffusion |
| Transcrever um áudio | Áudio → texto | Whisper |
| Ler um texto em voz | Texto → áudio | ElevenLabs, TTS dos assistentes |
| Descrever um vídeo | Vídeo → texto | Gemini |

## Como uma imagem entra no modelo

Aqui está a ideia central, e ela vale ouro. Como você vai ver no [capítulo 05 - Tokens](05-o-que-sao-tokens.md), o texto é picado em **tokens** e cada token vira um **vetor** de números (os *embeddings* do [capítulo 13](13-o-que-sao-embeddings.md)). Uma imagem passa por um caminho parecido:

1. A imagem é cortada numa **grade de quadradinhos** chamados **patches** — pense em pedaços de, digamos, 16×16 pixels cada.
2. Cada patch é **achatado** (os pixels viram uma fileira de números) e transformado num **vetor**. Esse vetor é um **token visual**: o equivalente, para a imagem, de um token de texto.
3. Todos esses tokens visuais entram **na mesma sequência** que os tokens de texto do seu prompt.

Ou seja: depois desse passo, o modelo não vê mais "texto" e "imagem" como coisas diferentes. Ele vê **uma fila de vetores**. A mesma máquina que processa texto processa a imagem, porque **tudo virou vetor**.

```text
IMAGEM (uma foto)
   │  corta em grade
   ▼
┌──┬──┬──┬──┐
│  │  │  │  │   cada quadradinho = 1 PATCH (ex: 16x16 pixels)
├──┼──┼──┼──┤
│  │  │  │  │
└──┴──┴──┴──┘
   │  cada patch é achatado e vira um VETOR (um "token visual")
   ▼
[v1] [v2] [v3] ... [v16]
   │
   ▼  entram na MESMA sequência que o texto:
[ O ] [ que ] [ tem ] [ nesta ] [ foto ] [v1] [v2] [v3] ... [v16]
   │
   ▼
       MODELO  ->  RESPOSTA
```

*(Números e tamanhos acima são ilustrativos — cada modelo usa seu próprio tamanho de patch e sua própria contagem.)*

## Buscar por texto e descrever imagem: o mesmo espaço

Falta um pedaço para a mágica funcionar: por que o modelo associa a **palavra** "gato" à **foto** de um gato?

Porque em muitos sistemas texto e imagem são treinados para caírem no **mesmo espaço vetorial** — a ideia por trás de modelos do tipo **CLIP**. A intuição, sem fórmula:

> Você mostra ao modelo milhões de pares (imagem, legenda) e o treina para **aproximar** o vetor da foto do vetor da sua descrição, e **afastar** de descrições erradas. Com o tempo, o vetor da foto de um gato e o vetor da palavra "gato" ficam **pertinho** um do outro.

Quando texto e imagem moram no mesmo mapa, duas coisas ficam fáceis:

- **Buscar imagem por texto**: você escreve "cachorro na praia", vira um vetor, e o sistema procura as fotos cujos vetores estão perto. É assim que busca semântica de imagem funciona.
- **Descrever imagem**: o vetor da foto já está "perto" das palavras que a descrevem, então o modelo tem por onde começar a escrever a legenda.

## E para gerar imagem?

Gerar imagem é um mecanismo **diferente** de gerar texto. O texto sai **um token por vez** (capítulo 05). A imagem, nos geradores atuais, costuma usar **difusão**: o modelo **parte de puro ruído** (uma tela de chuviscos) e vai **limpando** esse ruído passo a passo, sempre guiado pelo seu texto, até sobrar a imagem pedida. É como revelar uma foto no escuro: começa borrão e vai ganhando forma. Não é "desenhar do zero pincelada por pincelada" — é "tirar o ruído até aparecer o que o texto descreve".

## Por dentro: de patch a token visual

Juntando tudo, o pulo do gato (trocadilho intencional) é este:

```text
[1] IMAGEM  → cortada em PATCHES (grade de quadradinhos)
[2] cada PATCH → achatado → VETOR = TOKEN VISUAL
[3] TOKENS VISUAIS + TOKENS DE TEXTO → mesma sequência de vetores
[4] o MESMO transformer processa a fila inteira, misturando os dois
[5] sai a resposta (texto que "olhou" a imagem, ou uma nota de busca)
```

O motivo de a IA conseguir "misturar" uma foto e uma pergunta no mesmo raciocínio é justamente o passo [3]: **não existe mais fronteira** entre as modalidades lá dentro. Vetor é vetor. Por isso o mesmo maquinário serve para os dois.

## Pra que serve no dia a dia

- Tirar foto de um erro no código e perguntar "por que isso quebra?".
- Mandar o print de um gráfico e pedir um resumo dos números.
- Fotografar a geladeira e pedir receitas com o que tem nela.
- Transcrever uma reunião e gerar a ata.
- Gerar imagens para um post, um mockup ou um ícone.
- Descrever imagens para pessoas com deficiência visual (acessibilidade).

## Seja honesto: os limites (e o porquê)

- **Ela "vê" contando tokens visuais, não olhando como você.** Como a imagem virou um punhado de patches, o modelo **erra contagem** ("quantas pessoas tem na foto?") e **lê mal texto dentro de imagens** (OCR falho): as letras estão espalhadas por vários patches e ele precisa "adivinhar" juntando os pedaços. Não é que ele seja desatento — é que ele nunca viu a imagem inteira de uma vez.
- **Imagens geradas erram dedos e texto.** Mãos com seis dedos, placas com letras embaralhadas, reflexos impossíveis. A difusão aprende **padrões visuais**, não um modelo explícito de "como o mundo funciona" — ela não sabe que mão tem cinco dedos, só que costuma parecer assim. Melhora rápido, mas confira sempre.
- **Custa mais.** Uma imagem vira **muitos** tokens visuais, então processá-la consome bem mais que uma frase de texto — o que pesa no bolso quando você constrói uma aplicação (veja [capítulo 28](28-custos-e-escalabilidade.md)).
- **Direitos e privacidade.** Cuidado com imagens de pessoas, obras protegidas e dados sensíveis. Não mande o que você não pode compartilhar.

## Exercício

1. **Faça a IA errar contagem.** Tire (ou pegue) uma foto com **vários objetos parecidos** — um punhado de moedas, uma bandeja de brigadeiros, um estacionamento cheio. Pergunte "quantos você conta?". Confira na mão. Repita com outra foto mais cheia. A partir de quantos objetos ela começa a chutar?
2. Na mesma ferramenta, mande um print com **texto pequeno** (um recibo, um slide) e peça para transcrever. Onde o OCR escorregou? Compare com um texto grande e nítido.
3. Peça para uma IA **gerar** uma imagem de algo bem específico (ex: "uma mão segurando cinco lápis coloridos, close"). Repare nos dedos e em qualquer texto que aparecer. Depois mude **uma** palavra do pedido e gere de novo — o que mudou?
4. Classifique cada tarefa como *entrada* ou *saída* multimodal: (a) transcrever um podcast, (b) criar um logo, (c) resumir um print de conversa.

---

<div align="center">

[« 02 - O que é IA Generativa](02-o-que-e-ia-generativa.md) — [Índice](../README.md#roadmap) — [04 - Como o ChatGPT funciona »](04-como-o-chatgpt-funciona.md)

</div>
