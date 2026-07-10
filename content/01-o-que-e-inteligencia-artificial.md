# 01 - O que é Inteligência Artificial

Você provavelmente já usou Inteligência Artificial hoje, mesmo sem perceber. Quando o celular sugere a próxima palavra, quando o app de música acerta uma recomendação ou quando o e-mail joga uma propaganda direto no spam: tem IA por trás.

Mas afinal, o que é isso? E por que, se IA existe desde os anos 1950, todo mundo só começou a falar dela no fim de 2022? Este capítulo responde as duas coisas.

## Uma definição simples

Inteligência Artificial é a área da computação que faz máquinas executarem tarefas que, antes, só pessoas conseguiam fazer bem. Reconhecer um rosto numa foto, entender uma frase, traduzir um texto, jogar xadrez.

Mas "IA" não é uma técnica única. É um guarda-chuva. Debaixo dele cabem dois mundos bem diferentes de fazer a máquina parecer inteligente: **escrever regras à mão** e **deixar a máquina aprender com exemplos**. A diferença entre esses dois mundos é o coração deste capítulo.

## Dois jeitos de fazer IA: regras vs aprendizado

Imagine que sua tarefa é construir um **filtro de spam**. Existem dois caminhos.

**Caminho 1 — IA simbólica (regras escritas à mão).** Você, humano, senta e escreve a lógica. É o famoso `if/else`, só que gigante:

```python
def eh_spam(email):
    texto = email.lower()
    if "grátis" in texto and "clique aqui" in texto:
        return True
    if "você ganhou" in texto or "prêmio" in texto:
        return True
    if texto.count("!!!") > 2:
        return True
    return False
```

Isso é IA de verdade — chama-se **IA simbólica** ou **sistema baseado em regras**. Foi a abordagem dominante por décadas (os "sistemas especialistas" dos anos 1980 eram exatamente isso: milhares de regras escritas por especialistas humanos). E funciona... até certo ponto.

O problema aparece no mundo real. O spammer troca "grátis" por "gr4tis". Ou por "ganhe sem pagar nada". Aí você adiciona mais uma regra. Ele muda de novo. Você adiciona outra. Você está numa corrida de escrever `if` que nunca acaba — e cada regra nova pode quebrar as antigas. Você não escala.

**Caminho 2 — Machine Learning (aprender com exemplos).** Aqui você inverte a lógica. Em vez de escrever as regras, você mostra **exemplos** e deixa o computador descobrir os padrões:

```python
# pseudo-código do treino
emails    = [ ...milhares de e-mails... ]
rotulos   = [ "spam", "não spam", "spam", ... ]  # marcados por humanos

modelo = TreinarModelo(emails, rotulos)   # o modelo acha os padrões sozinho

modelo.prever("Ganhe um iPhone grátis!")  # → "spam"
```

Ninguém escreveu a regra "e-mail com 'grátis' é suspeito". O modelo **deduziu** isso ao ver que a palavra aparecia muito nos exemplos marcados como spam — junto com centenas de outros sinais sutis que nenhum humano listaria à mão (a frequência de certas palavras, links estranhos, horário de envio, e por aí vai).

Por que o de aprendizado ganha no mundo real? Porque quando o spammer inventa um truque novo, você não reescreve código: você só **mostra exemplos novos e retreina**. O sistema se adapta com dados, não com programador digitando `if`. É essa capacidade de melhorar com mais exemplos que fez o Machine Learning engolir quase toda a IA moderna.

## IA, Machine Learning e Deep Learning (as bonecas russas)

Esses três termos aparecem juntos o tempo todo e confundem muita gente. A melhor imagem é a das **bonecas russas** (matrioscas): uma dentro da outra, da maior para a menor.

```text
┌───────────────────────────────────────────────────────────┐
│ INTELIGÊNCIA ARTIFICIAL                                    │
│ máquinas fazendo tarefas "inteligentes"                    │
│ (inclui a IA simbólica / de regras — o if/else gigante)    │
│                                                            │
│   ┌───────────────────────────────────────────────────┐   │
│   │ MACHINE LEARNING                                   │   │
│   │ aprende padrões a partir de dados, sem regra à mão │   │
│   │                                                    │   │
│   │   ┌────────────────────────────────────────────┐  │   │
│   │   │ DEEP LEARNING                              │  │   │
│   │   │ redes neurais com muitas camadas           │  │   │
│   │   │                                            │  │   │
│   │   │   ┌────────────────────────────────────┐   │  │   │
│   │   │   │ IA GENERATIVA / LLMs               │   │  │   │
│   │   │   │ ChatGPT, geradores de imagem       │   │  │   │
│   │   │   └────────────────────────────────────┘   │  │   │
│   │   └────────────────────────────────────────────┘  │   │
│   └───────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────┘
```

- **Inteligência Artificial (boneca maior)** — o conceito amplo. Inclui a IA simbólica de regras que vimos acima.
- **Machine Learning (boneca do meio)** — a IA que **aprende com dados**. Nosso filtro de spam do Caminho 2 mora aqui.
- **Deep Learning (boneca menor)** — um tipo de Machine Learning que usa **redes neurais** com muitas camadas empilhadas ("deep" = profundo, muitas camadas). É o que destravou reconhecimento de voz, visão e linguagem.
- **IA Generativa e LLMs (a boneca de dentro)** — Deep Learning treinado para **gerar** conteúdo novo (texto, imagem, áudio). O ChatGPT é um **LLM** (Large Language Model), lá no núcleo de todas as caixas. Você aprofunda isso no [capítulo 02](02-o-que-e-ia-generativa.md).

Resumindo: todo LLM é Deep Learning, todo Deep Learning é Machine Learning, e todo Machine Learning é IA. Mas nem toda IA aprende — a boneca de fora ainda guarda os `if/else`.

## Por dentro: por que aprender escala melhor que escrever regras

A diferença entre os dois caminhos não é só de estilo. É a razão de a IA ter explodido.

**Escrever regras** tem um custo que cresce com a complexidade do problema. Cada caso novo = mais uma regra escrita por um humano. Para um problema simples (é fim de semana? cobre tarifa maior), dez regras resolvem. Para "essa foto tem um gato?", quantas regras você escreveria? Como se escreve `if` para "orelha pontuda"? É impossível na prática — o mundo tem gatos pretos, gatos de costas, gatos na sombra. Ninguém enumera isso.

**Treinar com exemplos** vira o jogo. Você não descreve o gato: você mostra 100 mil fotos rotuladas "gato / não gato" e deixa o modelo achar sozinho os padrões — bordas, texturas, formas — em camadas. As primeiras camadas de uma rede neural aprendem coisas simples (linhas, cantos); as seguintes combinam isso em partes (olho, pata); as últimas juntam tudo em "gato". Ninguém programou "olho" — emergiu dos dados.

A consequência prática é esta: com regras, para o sistema ficar melhor, **um humano trabalha mais**. Com aprendizado, para o sistema ficar melhor, você dá **mais dados e mais computação** — e isso a gente sabe fabricar em escala. Foi por isso que, quando a internet gerou dados demais e as placas de vídeo (GPUs) ficaram baratas, o aprendizado disparou e as regras ficaram para trás.

## Uma história bem resumida (IA não é nova)

A IA generativa parece ter surgido do nada em 2022, mas a área tem mais de 70 anos:

- **1950** — Alan Turing pergunta "máquinas podem pensar?" e propõe o **Teste de Turing**.
- **1956** — o termo "Inteligência Artificial" é cunhado na **conferência de Dartmouth**, nos EUA. Nasce o campo.
- **1997** — o **Deep Blue** (IBM) vence Garry Kasparov no xadrez. Marco da IA... mas ainda era muito baseado em regras e força bruta.
- **2012** — a rede **AlexNet** arrasa a competição de imagens **ImageNet**. É o estouro do **Deep Learning**: a prova de que aprender com dados + GPUs vencia as regras.
- **2016** — o **AlphaGo** (DeepMind) vence Lee Sedol no Go, jogo complexo demais para força bruta. Deep Learning de novo.
- **novembro de 2022** — lançamento do **ChatGPT**. A IA generativa vira acessível a qualquer pessoa com um navegador.

Repare no padrão: IA existe há décadas. O que "explodiu" recentemente não foi a IA em si — foi a **IA generativa acessível**, colocada na mão de todo mundo por uma caixa de texto.

## Os limites honestos

- **IA estreita (narrow) vs IA geral (AGI).** Toda IA que existe hoje é **estreita**: faz bem uma coisa. O modelo que recomenda filmes não dirige carro; o que joga Go não escreve e-mail. Mesmo o ChatGPT, que parece versátil, é estreito — foi treinado para uma tarefa (prever texto). A **IA geral (AGI)**, que raciocinaria sobre qualquer assunto como um humano, **ainda não existe**. É pesquisa e especulação.
- **IA não "entende" nem tem consciência.** Ela não tem sentimentos nem vontades. Calcula padrões e probabilidades — não compreende o mundo como você.
- **É boa em padrões, ruim em garantir verdade.** A IA acerta o que é *provável*, não o que é *verdadeiro*. Por isso ela às vezes inventa fatos com total confiança (você vai ver isso nas "alucinações", mais adiante). Ótima ferramenta, péssima testemunha jurada.

Guarde essa ideia: a IA de hoje é **poderosa e limitada** ao mesmo tempo. Entender as duas coisas é o que vai te fazer usá-la bem.

## Exercício

Para cada situação abaixo, decida: dá para resolver bem com **regras escritas à mão** (`if/else`) ou o problema **precisa de aprendizado com exemplos**? Justifique em uma frase, pensando em "eu conseguiria listar todas as regras?".

1. Calcular o troco de uma compra.
2. Identificar se há um cachorro numa foto.
3. Decidir se um aluno passou de ano (média ≥ 6 e presença ≥ 75%).
4. Transcrever um áudio de voz em texto.
5. Bloquear cartão quando a compra é "suspeita" (padrão de fraude).
6. Verificar se uma senha tem pelo menos 8 caracteres e um número.

Depois, responda: o ChatGPT é uma IA estreita ou uma IA geral (AGI)? E em qual boneca russa ele mora?

---

<div align="center">

[« 00 - Introdução](00-introducao.md) — [Índice](../README.md#roadmap) — [02 - O que é IA Generativa »](02-o-que-e-ia-generativa.md)

</div>
