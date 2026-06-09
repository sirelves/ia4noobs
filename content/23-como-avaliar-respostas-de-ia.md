# 23 - Como avaliar respostas de IA

Você ajustou o prompt e *parece* melhor. Mas será que melhorou mesmo? Ou só ficou melhor naquele um exemplo que você testou — e piorou em dez outros que você não viu? Sem **medir**, você está no escuro. E em IA o chão se move: o provedor atualiza o modelo, você troca o prompt, muda a temperatura — e o comportamento muda junto. Avaliar é o que separa "achismo" de "engenharia".

## Por que avaliar

Três motivos práticos:

1. **Saber se a mudança ajudou.** Trocou o prompt? Mediu antes e depois? Se não, você só *acha* que melhorou.
2. **Evitar regressões.** Uma mudança que conserta um caso pode quebrar outro. Sem testes, você não percebe.
3. **Modelos mudam sem avisar.** O mesmo prompt pode responder diferente depois de uma atualização do provedor. Avaliação te avisa quando isso acontece.

## O conjunto de avaliação (eval set)

A base de tudo é um conjunto de exemplos de teste. Cada exemplo tem:

- uma **entrada** (o que o usuário manda);
- a **resposta esperada** ou critérios do que seria uma boa resposta — o famoso **ground truth** ("verdade de referência").

Pense numa tabela:

| Entrada | Resposta esperada / critério |
| --- | --- |
| "Qual a capital da França?" | "Paris" |
| "Resuma este texto: ..." | Resumo com no máximo 3 frases, sem inventar fatos |
| "Traduza 'good morning'" | "bom dia" |
| (input que deve ser recusado) | Deve recusar educadamente |

Inclua **casos normais**, **casos difíceis** e **casos que devem falhar/ser recusados**. São esses últimos que mais pegam problemas.

## Métodos de avaliação

Existem três grandes formas, e você costuma combinar.

### 1. Checagem automática (quando há resposta certa)

Se a tarefa tem resposta objetiva — classificação, extração, tradução exata, formato JSON — dá para checar por código:

```text
para cada caso no eval_set:
    resposta = chamar_modelo(caso.entrada)
    se resposta == caso.esperada:
        acertos += 1
print(acertos / total)   # sua "nota"
```

Rápido, barato e repetível. É o ideal sempre que possível.

### 2. LLM como juiz (com cuidado)

Quando não há resposta única certa (um resumo, um texto livre), você pode usar **outro LLM para avaliar** a resposta, segundo critérios que você define:

```text
"Avalie a resposta abaixo de 0 a 5 quanto a:
 - factualmente correta?
 - responde a pergunta?
 - tom adequado?
Responda em JSON."
```

É escalável, mas tem armadilhas: o juiz também erra, tem vieses (tende a gostar de respostas longas, por exemplo) e custa dinheiro. Use como **sinal**, não como verdade absoluta — e calibre o juiz contra alguns exemplos avaliados por humanos.

### 3. Feedback humano

O padrão-ouro. Pessoas leem as respostas e avaliam. Caro e lento, então use de forma focada: amostras dos casos mais importantes, ou um botão de "👍/👎" no produto para coletar sinal real dos usuários.

## O que medir

Não meça só "acertou ou não". Olhe várias dimensões:

- **Precisão factual** — a informação está correta?
- **Ausência de alucinação** — o modelo inventou algo que não estava nos dados?
- **Formato** — seguiu a estrutura pedida (JSON válido, tamanho, idioma)?
- **Tom** — adequado ao seu produto?
- **Segurança** — recusou o que deveria recusar? Vazou algo?

## Evitar regressões: rode os evals sempre

Trate seu eval set como **testes automatizados**. Toda vez que você:

- muda o prompt,
- troca o modelo ou a versão,
- mexe na temperatura ou em outros parâmetros,

**rode os evals de novo e compare a nota.** Se caiu, você acabou de pegar uma regressão antes do usuário. Isso transforma ajustes de prompt de "tentativa e oração" em algo controlado.

## Comece simples

Você não precisa de uma plataforma de avaliação cara para começar. Uma **planilha** com 20 a 30 casos de teste já muda o jogo:

```text
| entrada | esperado | resposta_v1 | ok? | resposta_v2 | ok? |
```

Rode seus prompts, cole as respostas, marque o que passou. Com 30 casos você já enxerga padrões que um teste solto jamais mostraria. Depois, conforme o projeto cresce, você automatiza.

## Resumo

Avaliar não é luxo de projeto grande — é o que te dá confiança para mexer. Sem eval, cada mudança é um chute. Com eval, você tem números para decidir. Comece pequeno, com casos reais, incluindo os difíceis, e rode toda vez que algo mudar.

## Exercício

Crie uma mini-planilha de avaliação para uma tarefa de IA simples (ex.: classificar se um comentário é positivo, negativo ou neutro):

1. Escreva **10 casos de entrada**, incluindo pelo menos 2 ambíguos/difíceis.
2. Anote a **resposta esperada** de cada um.
3. Rode seu prompt e preencha a coluna "resposta do modelo".
4. Calcule a **taxa de acerto**. Depois mude algo no prompt, rode de novo e veja se a nota subiu ou caiu.

---

<div align="center">

[« 22 - Segurança em IA](22-seguranca-em-ia.md) — [Índice](../README.md#roadmap) — [24 - Custos e Escalabilidade »](24-custos-e-escalabilidade.md)

</div>
