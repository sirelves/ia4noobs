# 09 - Como fazer perguntas melhores

No [capítulo 08](08-o-que-e-prompt-engineering.md) você viu a **teoria**: o que é um prompt, quais são as peças de um bom pedido (papel, contexto, tarefa, formato, exemplos) e por que iterar faz parte do jogo. Aqui é a **oficina**. Vamos pegar perguntas ruins de verdade e transformá-las em perguntas boas, uma decisão de cada vez, para você ver *o que* foi adicionado e *por quê* aquilo muda a resposta.

A regra que costura tudo: **a IA não adivinha o que está na sua cabeça.** Toda informação que você não dá, ela preenche com o "chute mais comum". Perguntar melhor é substituir os chutes dela pelas suas escolhas.

## Três reformas ANTES → DEPOIS

Não vou explicar no abstrato. Veja o mesmo pedido antes e depois, com o que entrou marcado.

**1. Pedir ajuda com código**

```text
ANTES:  meu código não funciona, me ajuda?
```

Aqui a IA não sabe a linguagem, não vê o código, não sabe o erro nem o que "funcionar" significa. Ela vai chutar tudo isso.

```text
DEPOIS:  Estou em Python 3.11. [contexto técnico]
         Esta função deveria somar só os números pares de uma lista,
         mas retorna 0 quando testo com uma lista de números pares. [comportamento esperado vs. real]

         def soma_pares(lista):
             total = 0
             for n in lista:
                 if n % 2 == 1:
                     total += n
             return total          [o código de verdade]

         Aponte o bug e explique a correção em 1 frase. [tarefa + formato]
```

O que entrou: **linguagem/versão, o código real, o que deveria acontecer, o que acontece de fato, e o formato da resposta.** Com isso a IA para de adivinhar e vai direto ao ponto (aqui, o `== 1` deveria ser `== 0`).

**2. Pedir um texto**

```text
ANTES:  escreve um email pro meu chefe sobre férias
```

```text
DEPOIS:  Escreva um e-mail curto (máx. 6 linhas) para meu gestor
         pedindo férias de 12 a 26 de janeiro. [tarefa + restrição de tamanho]
         Tom cordial e profissional, sem ser bajulador. [tom]
         Já combinei a cobertura com a Ana; mencione isso. [contexto que só eu sei]
         Não invente motivos pessoais nem prometa nada além do combinado. [restrição]
```

O que entrou: **tamanho, tom, um fato do mundo real (a Ana cobre), e uma trava contra a IA inventar** — que é o erro mais comum em textos.

**3. Pedir uma explicação**

```text
ANTES:  o que é uma API?
```

```text
DEPOIS:  Explique o que é uma API para alguém que sabe usar planilhas
         mas nunca programou. [público-alvo]
         Use uma analogia do dia a dia e no máximo 2 parágrafos. [formato]
         Uma boa resposta me deixa capaz de explicar para outra pessoa
         com as minhas palavras. [critério de sucesso]
```

O que entrou: **público-alvo (define o vocabulário), tamanho, e um critério de sucesso** — o famoso "uma boa resposta seria...", que diz à IA qual é o alvo real.

## O kit anti-ambiguidade

Repare que os três exemplos puxam do mesmo baralho. Antes de mandar um pedido importante, passe os olhos nesta lista e adicione o que fizer sentido (não precisa usar todos):

- **Situação/contexto** — quem é você, onde isso se encaixa. *"Sou recém-formado buscando estágio."*
- **Público-alvo** — para quem é a resposta. *"Explique para uma criança de 8 anos."*
- **Formato** — lista, tabela, parágrafo, passo a passo, JSON.
- **Nível de detalhe** — *"resposta em 3 linhas"* vs. *"guia completo com exemplos"*.
- **Restrições** — o que evitar. *"Sem jargão", "não use bibliotecas externas", "máx. 200 palavras".*
- **Critério de sucesso** — *"uma boa resposta me permite fazer X sem ajuda."*
- **Exemplos do que você quer** — um modelo do estilo/formato (isso é *few-shot*, aprofundado no [capítulo 10](10-few-shot-e-chain-of-thought.md)).

Cada item que você adiciona é uma dúvida a menos para a IA preencher com chute.

## Papel e restrições: mire o comportamento

Duas alavancas fáceis e de alto impacto. **Papel** diz de que ângulo responder; **restrições** dizem o que *não* fazer. Juntas, elas afunilam a resposta:

```text
Aja como um revisor de segurança de código. [papel]
Analise a função abaixo e aponte SOMENTE problemas de segurança. [restrição de escopo]
Ignore estilo e performance. [o que ignorar]
Responda em bullets, um por problema, do mais grave ao menos grave. [formato]
```

Sem o papel e as restrições, a IA provavelmente comentaria indentação, nomes de variáveis e mil coisas irrelevantes. Com eles, ela mira só onde você quer.

## Iterar: a segunda pergunta vale ouro

Quase nunca o primeiro prompt sai perfeito — e tudo bem. A técnica é: **peça → veja o que faltou → refine.** Veja três rodadas reais de uma mesma conversa (as respostas estão *resumidas e rotuladas como ilustração*, não são saídas literais):

```text
RODADA 1 — você:
  Me dê ideias de post para o Instagram da minha cafeteria.

  [ilustração da resposta: 10 ideias genéricas — "poste uma foto do café",
   "faça uma enquete"... nada com a cara do seu negócio]

RODADA 2 — você (dando o contexto que faltou):
  Minha cafeteria é vegana, fica perto de uma faculdade e o público
  é estudante. Foco em preço acessível. Refaça as ideias com isso.

  [ilustração: agora vêm ideias sobre combo-estudante, café da tarde
   barato, opções veganas... mais alinhado, mas os textos estão longos]

RODADA 3 — você (apontando o problema e pedindo ajuste):
  Bom. Agora reescreva as 5 melhores como legendas curtas,
  no máximo 2 linhas cada, com um emoji no começo.

  [ilustração: 5 legendas curtas, prontas para colar]
```

Repare no movimento: rodada 1 revela o que faltou, rodada 2 injeta **contexto**, rodada 3 **corrige o formato**. Você não recomeça do zero a cada vez — vai lapidando. Frases que destravam quase tudo: *"ficou genérico, considere que..."*, *"errou aqui, o certo é..."*, *"mantenha o conteúdo, mas em forma de tabela"*.

## Por dentro: por que especificidade funciona

Lembra do [capítulo 04](04-como-o-chatgpt-funciona.md)? O modelo gera texto escolhendo, palavra por palavra, a **continuação mais provável** do que já está escrito. Um prompt vago tem *milhares* de continuações plausíveis, e a IA vai puxar para a mais comum — que raramente é a sua.

Pense no seu pedido como um funil. Cada detalhe que você acrescenta **corta fora** um monte de continuações que não te servem:

```text
"me fala sobre investimentos"
   → leque enorme: história, tipos, gírias de bolsa, cripto, tudo...

+ "para quem nunca investiu"      → corta as respostas técnicas
+ "poupança vs. Tesouro Direto"   → corta os outros produtos
+ "em linguagem simples"          → corta o economês
+ "quem guarda R$ 500/mês"        → corta os exemplos milionários
   = sobra praticamente só a resposta que você queria
```

É exatamente essa a intuição por trás das "peças" do [capítulo 08](08-o-que-e-prompt-engineering.md): papel, contexto, formato e restrições não são enfeite — cada um **estreita o leque de continuações** e empurra o modelo para o canto onde mora a boa resposta. Especificar é mirar.

## Onde isso NÃO ajuda (limites honestos)

Perguntar melhor turbina muito o resultado, mas não é mágica:

- **Não elimina alucinação.** Um prompt impecável ainda pode receber um fato inventado com toda confiança. A IA prevê texto plausível, não verdade — confira dados importantes por fora (mais no [capítulo 12](12-principais-erros-ao-usar-ia.md)).
- **Excesso de instrução atrapalha.** Vinte regras, algumas se contradizendo ("seja detalhado" + "responda em 1 linha"), confundem o modelo. Priorize o que importa.
- **Contexto tem custo.** Colar cinco páginas "por garantia" gasta tokens e pode até diluir o que importa. Dê o necessário, não o máximo (relembre [tokens](05-o-que-sao-tokens.md) e [janela de contexto](06-o-que-e-janela-de-contexto.md)).

A régua é simples: adicione detalhe enquanto ele **remove ambiguidade**; pare quando começar a virar ruído.

## Exercício

1. Pegue **2 perguntas ruins** que você mesmo fez a uma IA esta semana. Reescreva cada uma aplicando pelo menos **3 itens** do kit anti-ambiguidade (contexto, público-alvo, formato, restrição ou critério de sucesso).
2. Rode as **duas versões** (a ruim e a boa) na mesma IA e compare lado a lado: o que a versão boa trouxe que a ruim não trouxe?
3. Escolha uma das boas e faça **uma rodada de iteração**: aponte o que ainda faltou e peça um ajuste de contexto *ou* de formato. Veja se a segunda resposta chega mais perto do que você queria.

---

<div align="center">

[« 08 - O que é Prompt Engineering](08-o-que-e-prompt-engineering.md) — [Índice](../README.md#roadmap) — [10 - Few-shot e Chain-of-Thought »](10-few-shot-e-chain-of-thought.md)

</div>
