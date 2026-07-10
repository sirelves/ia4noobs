# 10 - Few-shot e Chain-of-Thought

Você já sabe fazer boas perguntas. Agora vamos a duas técnicas de prompt que parecem avançadas mas são simples — e que mudam MUITO o resultado: **few-shot** (dar exemplos) e **chain-of-thought** (pedir para pensar passo a passo). Mais do que "como usar", este capítulo explica **por que elas funcionam** — o que dá nome ao fenômeno e mostra o que está acontecendo por dentro.

## Zero-shot: o padrão

Quando você só descreve a tarefa, sem dar exemplo, isso se chama **zero-shot** ("zero tentativas de exemplo"):

```text
Classifique o sentimento da frase como POSITIVO, NEGATIVO ou NEUTRO.

Frase: "A entrega atrasou, mas o produto é ótimo."
```

Funciona bem em muitos casos. Mas às vezes a IA responde num formato que você não quer, ou erra o critério que você tinha em mente.

## Few-shot: mostre exemplos

**Few-shot** é dar **alguns exemplos** de entrada e saída antes do caso real. Em vez de *explicar* o que você quer, você *mostra*:

```text
Classifique o sentimento como POSITIVO, NEGATIVO ou NEUTRO.

Frase: "Amei, chegou antes do prazo!" -> POSITIVO
Frase: "Veio quebrado e ninguém respondeu." -> NEGATIVO
Frase: "Chegou no dia combinado." -> NEUTRO

Frase: "A entrega atrasou, mas o produto é ótimo." ->
```

Por que isso ajuda tanto:

- **Define o formato.** A IA vê que a resposta é uma palavra só e copia o padrão.
- **Ensina o seu critério.** Os exemplos mostram como VOCÊ decide os casos de fronteira.
- **Reduz variação.** Menos chance de a IA inventar um formato diferente a cada vez.

Regra prática: 2 a 5 exemplos costumam ser suficientes. E capriche neles — **exemplo ruim ensina a coisa errada.**

### O nome do fenômeno: in-context learning

Repare numa coisa estranha. Você "ensinou" o modelo a classificar do seu jeito — e ele aprendeu na hora, só de ler o prompt. **Nenhum peso do modelo mudou.** Ele é exatamente o mesmo depois da sua conversa; se você abrir uma aba nova, ele não lembra de nada. Esse aprendizado que acontece **dentro do prompt, sem re-treinar**, tem nome: **in-context learning** (aprendizado em contexto).

A intuição liga direto no [capítulo 04](04-como-o-chatgpt-funciona.md): o modelo só faz uma coisa, prever a continuação mais provável do texto. Quando ele lê três linhas no formato `Frase: ... -> ROTULO`, a continuação estatisticamente mais provável para uma quarta linha `Frase: ... ->` é... **outro rótulo, no mesmo formato.** Os exemplos não "programam" o modelo; eles **condicionam** qual continuação parece natural. Você não está mudando a máquina — está montando um começo de texto que só tem um jeito óbvio de terminar.

Isso é bem diferente de **fine-tuning** (ajuste fino), que é o outro jeito de "ensinar" um modelo. No fine-tuning você mostra milhares de exemplos e **os pesos do modelo realmente mudam** — o aprendizado fica gravado, permanente, e não custa tokens no prompt depois. Few-shot é o contrário: nada fica gravado, o "ensino" vive só naquele prompt e some quando a conversa acaba. Para a maioria das tarefas do dia a dia, few-shot resolve sem você precisar treinar nada.

## Chain-of-Thought: peça para pensar passo a passo

**Chain-of-Thought** (CoT), ou "cadeia de raciocínio", é pedir para a IA **mostrar o passo a passo** antes de dar a resposta final. Serve para problemas que exigem raciocínio: contas, lógica, decisões com várias etapas.

Compare. Sem CoT:

```text
Tenho 3 caixas com 12 maçãs cada. Dei 8 maçãs. Quantas sobraram?
```

Com CoT, é só acrescentar uma frase:

```text
Tenho 3 caixas com 12 maçãs cada. Dei 8 maçãs. Quantas sobraram?
Pense passo a passo antes de responder.
```

Ao "pensar em voz alta" (3 × 12 = 36; 36 − 8 = 28), a IA erra menos do que quando tenta cravar a resposta de primeira. É a diferença entre resolver uma conta de cabeça correndo e fazer no papel.

### Por que gastar tokens "pensando" ajuda

Lembra do [capítulo 05](05-o-que-sao-tokens.md)? O modelo gera **um token por vez**, sempre chutando o próximo mais provável, e é por isso que ele erra contas quando tenta cravar o resultado de uma vez — ele não "calcula", ele adivinha os tokens de um número plausível.

O CoT ataca exatamente esse ponto. Quando você deixa o modelo escrever os passos, cada passo vira uma **previsão mais fácil**. Prever o próximo token de "3 × 12 = " é muito mais fácil do que prever, do nada, o token da resposta final de um problema inteiro. O modelo quebra um problema difícil em vários pedaços fáceis, e ainda usa os pedaços que ele mesmo já escreveu como apoio para o próximo. Cada `36` e cada `28` que ele escreve fica no contexto e serve de trampolim para o passo seguinte. É como fazer a conta no papel em vez de na cabeça: os rascunhos intermediários seguram o raciocínio.

> Muitos modelos mais novos já raciocinam passo a passo por conta própria (os chamados modelos de "reasoning"). Mesmo assim, pedir explicitamente ajuda — e ainda te deixa **ver** o raciocínio para conferir se faz sentido.

### Self-consistency: pergunte várias vezes e vote

Tem uma técnica que turbina o CoT em problemas difíceis: **self-consistency** (autoconsistência). A ideia é simples — em vez de gerar **um** raciocínio, você gera **vários** para a mesma pergunta e fica com a resposta que **mais se repete**.

A intuição é a de uma votação. Como o modelo escolhe tokens com um pouco de aleatoriedade (aquela **temperatura** do [capítulo 05](05-o-que-sao-tokens.md)), cada tentativa pode seguir um caminho de raciocínio diferente. Alguns caminhos escorregam num passo e chegam a respostas erradas — mas erram cada um pro seu lado. Os caminhos **certos** tendem a convergir para a **mesma** resposta. Então, se você roda o problema 5 vezes e 4 delas dão `28`, `28` é uma aposta mais segura do que confiar numa tentativa só. Custa mais (você paga por várias respostas), então guarde para os problemas que realmente valem.

## Dá para juntar os dois

Few-shot e CoT se combinam: você pode dar exemplos que **já mostram o raciocínio**, não só a resposta final. Aí a IA aprende *como* pensar, não só *o que* responder.

```text
P: Um lápis custa R$2. Comprei 5. Quanto gastei?
R: 5 lápis × R$2 = R$10. Resposta: R$10.

P: Um caderno custa R$8. Comprei 3. Quanto gastei?
R:
```

## Por dentro: por que dá pra "ensinar" no prompt sem treinar

Vamos juntar as peças. A pergunta de fundo é: como um modelo com os pesos **congelados** consegue aprender uma tarefa nova no meio de uma conversa?

A resposta está em como ele lê o prompt. O modelo processa **tudo de uma vez**, o prompt inteiro junto, e para prever o próximo token ele "presta atenção" (é o mecanismo de atenção que vimos nos bastidores do [cap. 04](04-como-o-chatgpt-funciona.md)) em tudo o que já está escrito — inclusive nos seus exemplos. Ilustrando o raciocínio interno, sem afirmar que é a saída literal:

```text
[seu prompt, lido inteiro de uma vez]
  Frase: "Amei..."      -> POSITIVO
  Frase: "Veio quebrado" -> NEGATIVO
  Frase: "Chegou no dia" -> NEUTRO
  Frase: "A entrega atrasou, mas o produto é ótimo." ->  ← previsão aqui
                                                    │
   o modelo "olha para trás" e detecta o PADRÃO ────┘
   → formato: UMA palavra em CAIXA ALTA
   → tarefa:  rótulo de sentimento
   → continuação mais provável: POSITIVO
```

Nada foi gravado. O "aprendizado" é o modelo **detectar o padrão dos seus exemplos e continuá-lo** — e ele consegue detectar padrões assim porque foi treinado (aí sim, com pesos mudando) em bilhões de textos cheios de listas, tabelas e sequências que seguem um formato. Few-shot ativa essa habilidade já existente; ele não cria uma nova. Por isso o efeito **some** quando a conversa acaba: sem os exemplos no contexto, não há padrão para continuar.

## Seja honesto: os limites

- **Exemplos gastam contexto.** Cada exemplo ocupa tokens e entra na janela de contexto ([cap. 06](06-o-que-e-janela-de-contexto.md)). Muitos exemplos = prompt caro e, às vezes, mais lento.
- **CoT não garante acerto.** Um raciocínio bonito pode chegar a uma conclusão errada — o passo a passo *parece* convincente e mesmo assim escorrega numa conta. Confira o **resultado**, não só a "cara" do raciocínio.
- **Exemplo enviesa.** Se todos os seus exemplos forem de um tipo, o modelo aprende o viés junto: ele continua o padrão que você deu, torto e tudo. Varie os casos.
- **Nem toda tarefa precisa.** Para pedidos simples, zero-shot resolve. Não encha o prompt de exemplos nem peça raciocínio à toa.

## Na prática

Quer ver a diferença entre zero-shot e few-shot rodando de verdade? Tem um exemplo comentado em [`examples/few-shot`](../examples/few-shot).

## Exercício

1. **Few-shot vs zero-shot.** Pegue uma tarefa de classificação sua (ex: marcar mensagens como "urgente" ou "pode esperar"). Escreva um prompt **zero-shot** e um **few-shot** com 3 exemplos. Rode os dois. A resposta ficou mais consistente com exemplos?
2. **Chain-of-thought.** Dê para a IA um probleminha de lógica ou conta e peça a resposta direta. Depois refaça acrescentando "pense passo a passo". Mudou o acerto? Confira: o passo a passo estava certo, ou só *parecia* certo?
3. **Few-shot de formato.** Escreva 3 exemplos few-shot que ensinem um **formato de saída** específico (ex: sempre responder em JSON com os campos `nome` e `preco`). Sem explicar o formato em palavras — só mostrando os exemplos. O modelo pegou o padrão sozinho?
4. **Self-consistency na unha.** Pegue um problema de raciocínio meio difícil e mande o mesmo prompt com CoT **3 vezes**. As respostas bateram? Se divergiram, qual apareceu mais — e ela era a correta?

---

<div align="center">

[« 09 - Como fazer perguntas melhores](09-como-fazer-perguntas-melhores.md) — [Índice](../README.md#roadmap) — [11 - Como estruturar respostas »](11-como-estruturar-respostas.md)

</div>
