# 03 - Como o ChatGPT funciona

O ChatGPT parece mágica: você escreve uma pergunta e ele responde com texto bem construído, como se entendesse tudo. Mas por baixo do capô, a ideia central é surpreendentemente simples.

## A ideia central: prever a próxima palavra

No fundo, o ChatGPT faz **uma coisa só, repetida muitas vezes**: dado um texto até aqui, ele prevê qual é a **próxima palavra mais provável**. Aí ele anexa essa palavra, olha tudo de novo e prevê a próxima. E de novo. E de novo. Até formar a resposta inteira.

Pense no **teclado preditivo** do seu celular. Quando você digita "Bom", ele sugere "dia". O ChatGPT é isso **turbinado ao extremo**: em vez de adivinhar a próxima palavra de um jeito tosco, ele aprendeu com uma quantidade gigantesca de texto e consegue manter sentido por parágrafos inteiros.

```text
Entrada:  "O céu está"
Previsão: "azul" (muito provável)
          "nublado" (provável)
          "abacaxi" (quase impossível)
```

Ele escolhe entre as opções prováveis e segue em frente. Só isso, milhões de vezes por segundo.

## Como ele é treinado (sem matemática)

O ChatGPT não nasceu sabendo. Ele passou por etapas:

### 1. Pré-treino (ler "a internet inteira")

Mostraram a ele uma quantidade absurda de texto: livros, sites, artigos, fóruns. A tarefa era sempre a mesma: **tampar uma palavra e tentar adivinhar qual era.** Errando e ajustando bilhões de vezes, ele foi capturando padrões da linguagem, fatos sobre o mundo e estilos de escrita.

### 2. Ajuste fino (fine-tuning)

Depois, ele recebeu exemplos mais cuidadosos de **como ser um bom assistente**: perguntas e respostas bem escritas, mostrando o comportamento desejado. É como pegar alguém que sabe falar e ensinar a ser educado e prestativo.

### 3. Feedback humano (RLHF)

Por fim, pessoas avaliaram respostas do modelo, dizendo qual era melhor. Com esse "joinha / não-joinha" repetido muitas vezes, o modelo aprendeu a preferir respostas mais úteis, seguras e agradáveis. Essa etapa tem o nome técnico de **RLHF** (aprendizado por reforço com feedback humano).

## Por que ele inventa coisas (alucinação)

Aqui está o ponto crucial: o ChatGPT **não consulta um banco de dados de verdades**. Ele não tem uma "tabela de fatos" para verificar antes de responder.

Ele simplesmente gera o texto que **soa mais provável** dado o seu pedido.

Por isso, quando ele não sabe algo, em vez de dizer "não sei", muitas vezes ele **preenche o vazio com algo plausível** — um nome, uma data, uma fonte que parece real mas não existe. A isso damos o nome de **alucinação**.

Não é mentira no sentido humano (ele não tem intenção). É só consequência de como ele funciona: gerar texto provável, não texto verificado.

> Lição prática: confie no estilo, desconfie dos fatos. Sempre verifique datas, números, citações e nomes.

## Aleatoriedade e criatividade (temperatura)

Você já reparou que, fazendo a **mesma** pergunta duas vezes, o ChatGPT responde diferente? Isso é proposital.

Ele não escolhe **sempre** a palavra mais provável. Às vezes ele sorteia entre as opções boas, para soar mais natural e criativo. Existe um controle para isso, chamado **temperatura**:

- **Temperatura baixa** → mais previsível, "certinho", repetitivo. Bom para tarefas exatas.
- **Temperatura alta** → mais variado, criativo, surpreendente (e mais arriscado). Bom para brainstorm e textos criativos.

É como temperar comida: um pouco dá graça, demais estraga o prato.

## Recapitulando

- O ChatGPT prevê a próxima palavra, repetidamente.
- Ele aprendeu isso lendo muito texto, depois foi ajustado e refinado com ajuda humana.
- Ele **gera texto provável**, não consulta uma verdade — por isso pode alucinar.
- A "temperatura" controla o quanto ele varia entre o seguro e o criativo.

## Exercício

1. Com suas palavras, explique a frase: "o ChatGPT prevê a próxima palavra". Use a analogia do teclado preditivo.
2. Por que o ChatGPT às vezes inventa fatos? Relacione com a ideia de que ele "não consulta um banco de verdades".
3. Você vai pedir uma resposta técnica precisa (ex: converter unidades). Faz mais sentido temperatura **alta** ou **baixa**? Por quê?

---

<div align="center">

[« 02 - O que é IA Generativa](02-o-que-e-ia-generativa.md) — [Índice](../README.md#roadmap) — [04 - O que são Tokens »](04-o-que-sao-tokens.md)

</div>
