# 04 - Como o ChatGPT funciona

Este é o capítulo que abre a caixa-preta. Existe uma verdade sobre o ChatGPT que soa decepcionante no primeiro segundo e libertadora no segundo seguinte: **no fundo, ele é um autocompletar gigante.** Ele não "pensa", não "entende" e não "consulta a verdade". Ele faz uma coisa só, muito bem, muitas vezes seguidas: prevê o próximo pedaço de texto.

Quando você enxerga isso, para de ter medo dele e começa a usá-lo bem — sabendo onde confiar e onde desconfiar.

## A ideia central: prever o próximo token

O ChatGPT recebe o texto até aqui e responde uma pergunta só: **qual o próximo pedaço de texto mais provável?** Ele escolhe esse pedaço, cola no fim, olha tudo de novo e prevê o próximo. E de novo. E de novo, até a resposta terminar.

Esse "pedaço" tem nome: **token** — pode ser uma palavra, um pedaço de palavra ou um sinal de pontuação. É o assunto do [capítulo 05 - Tokens](05-o-que-sao-tokens.md). Por enquanto, pense em "palavra" que já serve.

```text
Você escreve:  "O céu está"
                     │
                     ▼
O modelo calcula uma probabilidade para CADA palavra possível (números ilustrativos):
        "azul"      → 41%
        "nublado"   → 28%
        "escuro"    → 12%
        "abacaxi"   → 0,0001%
                     │
                     ▼
Escolhe uma  →  "azul"
                     │
                     ▼
Agora o texto é "O céu está azul" e ele repete tudo para a PRÓXIMA palavra
```

É o **teclado preditivo** do celular levado ao extremo. A diferença é escala: em vez de sugerir a próxima palavra de um jeito tosco, ele foi treinado com uma quantidade absurda de texto e consegue manter sentido por parágrafos inteiros — inclusive parecendo que raciocina.

Segure esta frase, porque tudo depende dela: **ele não busca a resposta certa, ele monta a continuação mais plausível.** Na maior parte do tempo, plausível e certo coincidem. Quando não coincidem, começam os problemas — voltamos a isso no fim.

## As três fases do treino

Se ele é só um autocompletar, por que responde como um assistente educado em vez de completar sua pergunta com... outra pergunta? Porque passou por três fases. Cada uma transforma um pouco mais o "completador de texto cru" num assistente.

```text
  [1] PRÉ-TREINAMENTO          [2] AJUSTE FINO (SFT)         [3] RLHF
  ───────────────────         ────────────────────         ──────────────────
  Ler ~a internet inteira     Humanos escrevem              Humanos comparam
  e prever a próxima          exemplos de                   respostas do modelo
  palavra, bilhões de         "pergunta boa →               ("esta é melhor
  vezes                       resposta boa"                  que aquela")
        │                           │                             │
        ▼                           ▼                             ▼
  Sabe LÍNGUA, fatos,         Aprende o FORMATO de          Aprende o TOM: ser
  estilos. Mas é cru:         seguir instruções e           útil, seguro e
  só sabe continuar texto     conversar                     agradável
```

### 1. Pré-treinamento (ler "a internet inteira")

Mostraram ao modelo uma quantidade gigantesca de texto — grande parte da internet pública, livros, artigos, código. A tarefa era sempre a mesma e sem nenhum humano corrigindo à mão: **tampar a próxima palavra e tentar adivinhá-la.** Errando e se ajustando bilhões de vezes, ele foi absorvendo gramática, fatos sobre o mundo, raciocínios comuns e vários estilos de escrita.

O resultado dessa fase é um **autocompletar cru e poderoso** — que sabe muito, mas não sabe conversar. Se você escrevesse "Qual a capital da França?", um modelo só pré-treinado poderia responder... com mais perguntas parecidas, porque na internet perguntas costumam vir em listas. Ele completa o padrão, não atende ao pedido.

### 2. Ajuste fino supervisionado (SFT / instruction tuning)

Aqui humanos entram em cena. Eles escrevem milhares de exemplos caprichados de **como um bom assistente responde**: uma instrução ou pergunta, seguida da resposta ideal. O modelo treina em cima desses exemplos e aprende o **formato** de seguir instruções e dialogar.

É como pegar alguém que já domina o idioma e ensinar a etiqueta da conversa: "quando te perguntam algo, você responde aquilo — de forma direta e organizada". Depois dessa fase ele já parece um assistente. Mas ainda não sabe, entre duas respostas aceitáveis, qual as pessoas realmente preferem.

### 3. RLHF (aprendizado por reforço com feedback humano)

Na última fase, o modelo gera várias respostas para o mesmo pedido e **humanos comparam**: "a resposta A é melhor que a B". Esse monte de comparações treina o modelo a **preferir** o tipo de resposta que as pessoas aprovam — mais útil, mais segura, no tom certo, sem enrolação. O nome técnico disso é **RLHF** (*Reinforcement Learning from Human Feedback*); guarde a sigla, ela aparece muito.

É o polimento final: pré-treino dá o conhecimento, SFT dá o formato, RLHF dá o **julgamento de qual resposta é boa**. Os três juntos transformam um autocompletar num assistente.

## Por dentro: atenção (attention)

Falta explicar o "motor" que faz o modelo manter o fio da meada. A arquitetura por trás do ChatGPT se chama **Transformer**, e a peça central dela é a **atenção** (*attention*).

A intuição, sem uma fórmula sequer: ao decidir o próximo token, o modelo **olha para todos os tokens anteriores ao mesmo tempo** e **pesa quais são os mais relevantes** para aquela decisão. Nem toda palavra importa igual — a atenção é o mecanismo que decide "para prever o que vem agora, preciso prestar atenção NAQUELAS palavras ali".

Um exemplo clássico. Considere a frase pela metade:

```text
"O médico falou com a paciente porque ela ..."
                                        │
                                        ▼
    Para continuar, a quem "ela" se refere? médico ou paciente?
    A ATENÇÃO liga "ela" ──────────────────────► "paciente"
    (pesa forte esse vínculo e fraco o resto)
```

O modelo conecta "ela" a "paciente" e segue coerente. Troque para "porque **ele**..." e a atenção religa o vínculo para "médico". **É isso que dá o famoso "contexto"**: a cada token gerado, o Transformer recalcula em quem prestar atenção. Não há memória mágica nem compreensão — há um mecanismo que pondera relevância entre pedaços de texto, repetido em muitas camadas empilhadas. Dessa ponderação, feita em escala gigantesca, emerge algo que se parece muito com entender.

## Os limites (a parte honesta)

Agora que você viu o mecanismo, os limites deixam de ser defeitos misteriosos e viram consequências óbvias de como a coisa funciona:

- **Ele não entende nem tem intenção.** Não há um "eu" ali querendo te ajudar ou te enganar. Há um preditor de texto plausível. Ele parece intencional porque foi treinado com texto humano, que é cheio de intenção.
- **Ele alucina com confiança.** Como ele gera o texto que **soa** mais provável — e não consulta um banco de fatos —, quando não sabe algo, muitas vezes preenche o vazio com algo plausível: um nome, uma data, uma referência que parece real e não existe. Isso se chama **alucinação**. E como o tom seguro também foi premiado no treino, ele erra com a mesma cara de quem acerta.
- **O conhecimento tem data de corte.** Ele só viu o texto do pré-treino, que parou num certo ponto no tempo. Fora isso, ele não sabe o que não estava no treino — eventos recentes, o conteúdo de um site que você não colou, seus dados privados. Se não está na pergunta nem no treino, ele **chuta plausível**.

> Lição prática: **confie no estilo, desconfie dos fatos.** Sempre verifique datas, números, nomes e citações — ainda mais quando ele soa mais convicto.

## Recapitulando

- No fundo, o ChatGPT **prevê o próximo token**, repetidamente. É um autocompletar gigante — não pensa nem entende.
- Ele vira assistente por três fases: **pré-treinamento** (aprende língua e fatos), **SFT** (aprende o formato de seguir instruções) e **RLHF** (aprende o tom que as pessoas preferem).
- O motor é o **Transformer**, e sua peça-chave é a **atenção**: a cada token, o modelo pesa quais palavras anteriores importam. É daí que vem o "contexto".
- Como gera texto **plausível** (não verificado), ele **alucina** com confiança e tem **data de corte** de conhecimento.

## Exercício

1. **Veja o autocompletar em ação.** Escreva uma frase pela metade e mande o modelo continuar, tipo: "Complete esta história: *Era uma tarde de sexta quando o telefone tocou e...*". Repare que ele não "sabe" o final — ele monta a continuação mais plausível, token a token.
2. **Explique com suas palavras** as três fases de treino (pré-treinamento, SFT e RLHF) e o que cada uma acrescenta. Se travar em alguma, releia a seção — e note que explicar com as próprias palavras é justamente o que um autocompletar não conseguiria fingir bem.
3. Peça ao modelo uma informação bem específica e recente (uma estatística de ontem, o preço de algo hoje). Ele respondeu com números? Agora relacione a resposta com "alucinação" e "data de corte". Você confiaria sem verificar?

---

<div align="center">

[« 03 - IA Multimodal](03-ia-multimodal.md) — [Índice](../README.md#roadmap) — [05 - O que são Tokens »](05-o-que-sao-tokens.md)

</div>
