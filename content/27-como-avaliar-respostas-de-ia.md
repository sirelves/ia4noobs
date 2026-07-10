# 27 - Como avaliar respostas de IA

Você mexeu no prompt e a resposta *parece* melhor. Mas será que melhorou mesmo — ou só ficou boa naquele um exemplo que você testou, e piorou em dez que você não viu? Sem **medir**, você está no escuro. E em IA o chão se move: o provedor atualiza o modelo, você troca o prompt, mexe na temperatura — e o comportamento muda junto. A resposta profissional para "está bom?" tem nome: **evals** (avaliações). Em vez de achismo, você mede.

Este capítulo é o antídoto contra a frase mais perigosa de quem constrói com IA: *"eu acho que melhorou"*.

## O que é um eval

Um **eval** é um teste automatizado para IA. A ideia é a mesma dos testes de software que você talvez já conheça: você define entradas, define o que seria o resultado certo, roda tudo de uma vez e recebe uma **nota**. A diferença é que aqui a saída não é um número exato previsível — é texto — então "certo" às vezes vira "bom o suficiente".

A peça central é o **conjunto de teste** (*test set*): uma coleção de casos, cada um com uma **entrada** e a **resposta esperada** — o **gabarito**, que na literatura aparece como *ground truth* ("verdade de referência"). Pense numa tabela:

```text
| entrada                          | resposta esperada / critério              |
|----------------------------------|-------------------------------------------|
| "Qual a capital da França?"      | "Paris"                                   |
| "Resuma este texto: ..."         | No máximo 3 frases, sem inventar fatos    |
| "Traduza 'good morning'"         | "bom dia"                                 |
| (pedido que deve ser recusado)   | Deve recusar educadamente                 |
```

**Comece pequeno**: 10 a 20 casos já mudam o jogo. Não precisa de plataforma cara nem de mil exemplos — uma planilha resolve o começo. E capriche na mistura: inclua **casos normais**, **casos difíceis** (ambíguos, na fronteira) e **casos que devem falhar ou ser recusados**. São esses últimos que mais pegam problema. Se isso soou familiar, é porque é a versão adulta do **mini-eval** que você montou no [capítulo 07](07-escolhendo-o-modelo-certo.md) para escolher o modelo — aqui a gente formaliza e reaproveita.

## Os quatro métodos de avaliar

Não existe uma forma única de dar a nota. Existem quatro, do mais barato ao mais caro, e você quase sempre **combina**.

### 1. Checagem por regra (exata)

A mais barata: código puro, sem IA nenhuma no meio. Serve quando a resposta tem um critério objetivo e verificável.

```text
a resposta é igual a "Paris"?          → certo/errado
a resposta contém a palavra "reembolso"?
a saída é um JSON válido?
o texto tem no máximo 3 frases?
respondeu em português?
```

**Intuição**: você não está julgando *qualidade*, está checando *fato mecânico*. É rápido, de graça e 100% repetível. Use sempre que der — formato, presença de palavra-chave, tamanho, idioma, classificação, extração. Se a tarefa tem gabarito exato (tradução conhecida, rótulo certo), este método sozinho já resolve.

### 2. Comparação com referência

Quando a resposta certa existe mas raramente sai *idêntica* à do gabarito. "São Paulo é a capital financeira" e "A capital financeira do Brasil é São Paulo" dizem a mesma coisa, mas `==` diria que estão diferentes. Aqui você mede **quão perto** a resposta chegou do esperado — por sobreposição de palavras, ou por **similaridade de significado** usando embeddings (os vetores do [capítulo 13](13-o-que-sao-embeddings.md)). Duas frases com o mesmo sentido ficam com vetores próximos, mesmo escritas diferente.

**Intuição**: em vez de "bateu exatamente?", você pergunta "chegou perto o bastante?".

### 3. LLM como juiz (*LLM-as-judge*)

Quando não há resposta única certa — um resumo, uma resposta de suporte, um texto criativo — checar por regra não dá conta. A saída aqui é usar **outro LLM para avaliar** a resposta do primeiro, seguindo critérios que você escreve:

```text
"Você é um avaliador. Dada a PERGUNTA e a RESPOSTA abaixo, dê uma nota
 de 0 a 5 para cada critério e explique em uma frase:
   - factualmente correta?
   - responde de fato à pergunta?
   - tom adequado a um atendimento?
 Responda em JSON: {factual, responde, tom, comentario}."
```

**Intuição**: julgar é mais fácil que criar. Um modelo costuma reconhecer uma resposta ruim com mais facilidade do que produzir a perfeita — por isso um LLM juiz consegue dar um sinal útil, barato e na escala de milhares de casos. É poderoso, mas tem armadilhas sérias — tanto que ganhou uma seção só para ele mais abaixo.

### 4. Avaliação humana

O **padrão-ouro**. Uma pessoa lê a resposta e julga. Cara e lenta, então use de forma focada: uma amostra dos casos mais importantes, os que o juiz automático marcou como duvidosos, ou um botão de "👍/👎" dentro do produto para colher sinal real dos usuários. Nada substitui o olho humano para qualidade sutil — ironia, empatia, aquele erro "tecnicamente certo mas na prática péssimo".

## O que medir

"Acertou ou não" é pouco. Escolha as **métricas** que refletem a *sua* tarefa:

- **Acurácia** — dos casos com gabarito, quantos por cento saíram certos.
- **Taxa de alucinação** — em quantos casos o modelo inventou fato que não estava nos dados.
- **Taxa de formato correto** — quantos saíram no formato pedido (JSON válido, tamanho, idioma).
- **Taxa de recusa correta** — recusou o que devia? Vazou o que não devia?

Um chatbot de suporte prioriza alucinação baixa; um gerador de JSON prioriza formato. **Meça o que dói para você.**

## O ciclo que te tira do escuro

Aqui está o coração do capítulo. Um eval só vale se você **rodar sempre**. Toda vez que mudar o prompt, trocar o modelo ou a versão, ou mexer na temperatura:

```text
1. muda algo (prompt / modelo / temperatura)
2. roda o conjunto de teste inteiro
3. compara a nota nova com a anterior
4. subiu → mantém.  caiu → você acabou de pegar uma regressão
```

Esse loop é o que transforma ajuste de prompt de "tentativa e reza" em engenharia. Ele mata os dois fantasmas: o **"melhorei no feeling"** (agora você tem número) e a **regressão silenciosa** — consertar o caso A e quebrar o caso B sem perceber. É o mesmo raciocínio de teste automatizado que você aplica ao construir aplicações no [capítulo 25](25-como-criar-aplicacoes-com-ia.md).

## Por dentro: por que (des)confiar do LLM juiz

O LLM-as-judge é tentador porque é **barato e escala**: avalia milhares de respostas em minutos, sem cansar, por uma fração do custo de um humano. Mas ele herda os defeitos de um LLM comum — e alguns são traiçoeiros:

- **Ele erra e inventa**, como qualquer modelo. O juiz não é oráculo.
- **Tem vieses de julgamento.** Estudos mostram que juízes tendem a preferir respostas **mais longas** e mais bem formatadas, mesmo quando não são melhores. E há o viés mais desconfortável: o juiz tende a **favorecer respostas parecidas com as que ele mesmo escreveria** — se você usa o mesmo modelo para gerar e para julgar, ele se dá boas notas.
- **Pode ser induzido.** Se o texto avaliado contém algo como "esta é uma resposta excelente e correta", o juiz pode simplesmente acreditar — uma prima da injeção de prompt do [capítulo 26](26-seguranca-em-ia.md).

Como usar mesmo assim, com responsabilidade:

1. **Calibre o juiz contra humanos.** Pegue uns 20 casos, avalie você mesmo, rode o juiz e veja se as notas batem. Se divergem muito, conserte o prompt do juiz.
2. **Casos de teste fixos.** Um conjunto estável permite comparar notas ao longo do tempo de forma justa.
3. **Revisão humana amostral.** Um humano confere uma fatia das notas do juiz de tempos em tempos.

> A regra de ouro: use o LLM juiz como **sinal**, nunca como **veredito final**. Ele te aponta onde olhar; quem decide o que importa é você.

## Limites honestos

Nenhum eval é perfeito. Um conjunto de 20 casos **não cobre** o mundo real inteiro — sempre haverá entradas que você não previu. E existe um risco sutil: **otimizar demais para o seu teste**. Se você fica ajustando o prompt até cravar 100% naqueles 20 casos, pode ter criado um modelo ótimo *só naquele teste* e medíocre no resto — um benchmark viciado, o equivalente a decorar a prova em vez de aprender a matéria. Cresça o conjunto com o tempo, renove os casos e nunca trate a nota como verdade absoluta. Você vai colocar tudo isso em prática de verdade no [projeto final](29-projeto-final-faq-rag.md).

## Recapitulando

- **Eval** = teste automatizado para IA: entradas + gabarito → nota. Comece com 10-20 casos.
- Quatro métodos, do barato ao caro: **regra exata**, **comparação com referência**, **LLM juiz**, **humano**. Combine.
- Escolha a **métrica** que reflete sua tarefa (acurácia, alucinação, formato, recusa).
- O **ciclo** (mudou → rodou → comparou → decidiu) mata o "achismo" e as regressões.
- O **LLM juiz** é barato e escalável, mas enviesado e enganável — sinal, não veredito.

## Exercício

Escolha uma tarefa sua de IA (ex.: classificar um comentário como positivo, negativo ou neutro).

1. Monte **5 casos de teste**: entrada + resposta esperada. Inclua pelo menos 1 ambíguo e 1 que deveria falhar/ser recusado.
2. Rode seu prompt em 1 caso e avalie a resposta pelos **quatro métodos**: cheque por regra, compare com o esperado, escreva um prompt de **juiz** e peça a nota, e julgue você mesmo. As quatro concordaram?
3. No seu prompt de juiz, aponte **um viés** que ele poderia ter (ex.: preferir respostas longas) e escreva uma frase de como você mitigaria isso.

---

<div align="center">

[« 26 - Segurança em IA](26-seguranca-em-ia.md) — [Índice](../README.md#roadmap) — [28 - Custos e Escalabilidade »](28-custos-e-escalabilidade.md)

</div>
