# 24 - Custos e Escalabilidade

Seu app funciona, é seguro e você sabe avaliá-lo. Falta a pergunta que assombra todo projeto de IA em produção: **quanto isso vai custar quando muita gente usar?** IA não é grátis, e a conta cresce com o uso. Este último capítulo é sobre não tomar um susto na fatura e não derrubar o app quando ele bombar.

## Como a cobrança costuma funcionar: tokens

A maioria das APIs de LLM cobra por **token**. Token é um pedaço de texto — mais ou menos uma palavra curta ou parte de uma palavra. "Inteligência" pode virar 3 ou 4 tokens. Regra de bolso: ~1 token a cada 4 caracteres em inglês (um pouco mais em português).

Você paga por dois lados:

- **Tokens de entrada** (tudo que você manda: instruções + contexto + pergunta);
- **Tokens de saída** (o que o modelo gera).

A saída costuma ser **mais cara** por token que a entrada. E atenção: **todo o contexto conta toda vez**. Numa conversa longa, se você reenvia o histórico inteiro a cada mensagem, está pagando por ele repetidamente.

```text
custo ≈ (tokens_entrada × preço_entrada) + (tokens_saída × preço_saída)
```

## Por que prompts grandes custam caro

Dois vilões inflam a conta:

1. **Prompts e contextos enormes.** Mandar um documento inteiro de 50 páginas em toda requisição é caro — e nem sempre o modelo precisa de tudo.
2. **Respostas longas.** Pedir "explique em detalhes" gera muitos tokens de saída. Se você só precisa de um "sim/não", peça um "sim/não".

## Formas de reduzir custo

- **Escolha o modelo certo para a tarefa.** (Vimos no capítulo 21.) Tarefa simples e em volume? Modelo menor e mais barato. Não use o modelo topo de linha para classificar comentários.
- **Encurte os prompts.** Corte instruções repetidas, exemplos desnecessários e contexto que não ajuda. Menos tokens, menos custo.
- **Use RAG em vez de mandar tudo.** Em vez de despejar o documento inteiro, busque só os **trechos relevantes** e mande apenas eles. Economiza tokens e ainda melhora a resposta.
- **Cache.** Se a mesma pergunta se repete, guarde a resposta e reutilize. Muitos provedores também oferecem **cache de prompt** (o trecho fixo do prompt é cobrado mais barato nas chamadas seguintes).
- **Limite o tamanho da saída.** Defina um máximo de tokens de resposta para evitar respostas gigantes e caras.

## Latência e experiência do usuário

Custo é dinheiro; **latência** é paciência. Modelos demoram alguns segundos para responder, e respostas longas demoram mais. Ficar olhando uma tela travada é péssimo.

A solução clássica é **streaming**: em vez de esperar a resposta inteira, você mostra o texto **conforme ele é gerado**, palavra por palavra. A resposta total leva o mesmo tempo, mas o usuário **percebe** muito mais rápido — é a diferença entre "travou" e "está pensando".

```text
sem streaming:  [.................] (5s travado) → resposta
com streaming:  Olá... como... posso... ajudar...  (já aparecendo)
```

## Rate limits e filas

Os provedores impõem **limites de taxa** (rate limits): quantas requisições ou tokens você pode usar por minuto. Estoure o limite e a API retorna erro **429**. Em produção isso vai acontecer. Prepare-se:

- **Retry com espera** (backoff) para erros temporários.
- **Fila**: em vez de mandar tudo de uma vez, enfileire as requisições e processe num ritmo que respeite o limite.

## Escalar: lote e jobs assíncronos

Nem toda tarefa precisa de resposta na hora:

- **Processamento em lote (batch).** Tem 10 mil textos para classificar? Mande em lotes, fora do horário de pico. Vários provedores cobram **mais barato** em modo batch.
- **Jobs assíncronos.** Tarefas pesadas (resumir um relatório enorme, gerar muitos itens) não devem travar a requisição do usuário. Coloque numa **fila de jobs**, processe em segundo plano e avise quando terminar. (Se você usa Redis + Bull, ou Celery, é exatamente esse padrão.)

## Monitore em produção

Você não controla o que não mede. Acompanhe:

- **Custo por dia / por usuário / por funcionalidade** — descubra cedo o que está caro.
- **Tokens médios** por requisição — um pico pode indicar prompt inchado.
- **Taxa de erro e de rate limit** — sinal de que precisa de fila ou de outro plano.
- **Latência** — a experiência piorou?

Configure **alertas de custo**. A história clássica de IA em produção é a fatura surpresa no fim do mês. Um alerta simples evita isso.

## Checklist de produção

```text
[ ] Modelo escolhido por tarefa (nem sempre o mais caro)
[ ] Prompts enxutos; RAG manda só o relevante
[ ] Cache de respostas e/ou de prompt onde faz sentido
[ ] Limite de tokens de saída definido
[ ] Streaming para respostas longas
[ ] Retry com backoff para erro 429
[ ] Filas para volume e jobs assíncronos para tarefas pesadas
[ ] Monitoramento de custo, tokens, erros e latência
[ ] Alerta de custo configurado
```

## Próximos passos

Você chegou ao fim do IA4Noobs. Saiu do "o que é um modelo" e chegou em "como colocar IA no mundo real com segurança, qualidade e custo sob controle". Esse é o conhecimento que a maioria dos tutoriais pula.

E agora? **Construa.** Pegue uma ideia pequena, monte o backend, escreva um eval set, meça, ajuste e observe o custo. A prática é onde tudo se conecta. Leia a documentação do provedor que você escolher — preços e limites mudam, e ler a fonte oficial é um superpoder.

Por fim: o **IA4Noobs é open-source e feito pela comunidade**. Achou um erro? Tem um exemplo melhor? Quer escrever um capítulo novo? **Contribua.** Abra uma issue, mande um pull request, compartilhe com quem está começando. Ensinar é a melhor forma de aprender — e é assim que o 4noobs cresce. Bons builds! 🚀

## Exercício

Estime o custo do seu app de IA:

1. Escolha uma tarefa real e conte (ou estime) os **tokens de entrada e saída** de uma requisição típica.
2. Pegue a tabela de preços de um provedor e calcule o **custo de uma requisição**.
3. Multiplique por um volume realista (ex.: 1.000 requisições/dia). Assustou?
4. Liste **duas mudanças** (modelo menor, prompt menor, cache, RAG) que reduziriam esse custo e estime o novo valor.

---

<div align="center">

[« 23 - Como avaliar respostas de IA](23-como-avaliar-respostas-de-ia.md) — [Índice](../README.md#roadmap) — [Glossário »](glossario.md)

</div>
