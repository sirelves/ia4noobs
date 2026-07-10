# 28 - Custos e Escalabilidade

Seu app funciona, é seguro e você sabe avaliá-lo. Falta a pergunta que assombra todo projeto de IA em produção: **quanto isso vai custar quando muita gente usar?** IA não é grátis, e a conta cresce com o uso. Este último capítulo é sobre não tomar um susto na fatura e não derrubar o app quando ele bombar.

> **Aviso de honestidade:** todos os preços aqui são **aproximados e mudam com o tempo**. Use-os para pegar a **ordem de grandeza**, não como valor exato. Antes de decidir qualquer coisa, confira a página de preços do seu provedor. E a regra de ouro deste capítulo: **meça antes de otimizar** — não gaste tempo cortando tokens no escuro sem saber onde o dinheiro está indo.

## A base: você paga por token

Como vimos no [capítulo 05](05-o-que-sao-tokens.md), a maioria das APIs de LLM cobra por **token** — os pedacinhos de texto que o modelo enxerga. E você paga por dois lados:

- **Tokens de entrada** (tudo que você manda: instruções + contexto + histórico + pergunta);
- **Tokens de saída** (o que o modelo gera).

A saída costuma ser **mais cara** por token que a entrada — muitas vezes 3 a 5× mais. E atenção ao ponto que mais pega gente de surpresa: **todo o contexto conta toda vez**. Numa conversa longa, se você reenvia o histórico inteiro a cada mensagem, paga por ele repetidamente.

```text
custo_por_chamada ≈ (tokens_entrada × preço_entrada) + (tokens_saída × preço_saída)
```

### A conta de uma chamada

Vamos repetir a conta do [capítulo 05](05-o-que-sao-tokens.md), que é a fundação de tudo aqui. Usando um modelo barato com preço na **ordem de** US$ 0,15 por 1 milhão de tokens de entrada e US$ 0,60 por 1 milhão de saída:

```text
Entrada:  2.000 tokens  →  2.000 / 1.000.000 × US$ 0,15  = US$ 0,0003
Saída:      500 tokens  →    500 / 1.000.000 × US$ 0,60  = US$ 0,0003
                                                   Total ≈ US$ 0,0006  por chamada
```

### A conta de escala

US$ 0,0006 parece nada — e é, para **uma** chamada. O susto vem da multiplicação:

```text
US$ 0,0006 × 100.000 chamadas/mês  ≈  US$ 60/mês
```

Sessenta dólares por uma feature que faz 100 mil chamadas mensais. Tranquilo. Agora veja como isso escala nos dois eixos que importam — **contexto** e **volume**:

```text
                    10 mil/mês     100 mil/mês     1 milhão/mês
contexto enxuto     ~US$ 6         ~US$ 60         ~US$ 600
(2.500 tk/chamada)

contexto inchado    ~US$ 60        ~US$ 600        ~US$ 6.000
(25.000 tk/chamada)
```

Repare: **enfiar um "manual" de contexto que você não precisava multiplicou a fatura quase 10 vezes** — de US$ 600 para US$ 6.000/mês no mesmo volume. (A tabela usa um preço médio por token para simplificar; como o inchaço é quase todo de **entrada**, a mais barata, na prática o salto fica um pouco menor — mas continua brutal.) Não foi o modelo, não foi o volume: foi o contexto desperdiçado, cobrado em **toda** chamada. Guarde essa imagem, porque é ela que explica as alavancas a seguir.

## As 3 grandes alavancas de custo

Quase todo custo de LLM sai de três lugares. Se a conta está alta, o problema está em pelo menos um deles — e é aí que você mexe.

**1. Tamanho do modelo.** Modelo maior = mais caro por token, às vezes 20 a 50× mais que um modelo pequeno. A alavanca: **use o menor modelo que resolve a tarefa**. Classificar um comentário como spam não precisa do topo de linha. Uma técnica poderosa é o **roteamento por dificuldade**: um modelo pequeno e barato tenta primeiro; só o que ele não dá conta sobe para o modelo caro. Escolher modelo é assunto do [capítulo 07](07-escolhendo-o-modelo-certo.md).

**2. Tamanho do contexto.** Cada token de entrada é pago, e o contexto ([capítulo 06](06-o-que-e-janela-de-contexto.md)) é onde o desperdício se esconde. Mandar um PDF de 50 páginas em toda requisição quando o modelo só precisa de dois parágrafos é queimar dinheiro. A alavanca: **mande só o necessário**. Em vez de despejar o documento inteiro, use **RAG** ([capítulo 14](14-o-que-e-rag.md)) para buscar e enviar **apenas os trechos relevantes**. Economiza tokens e ainda **melhora** a resposta, porque o modelo não se perde no meio de ruído.

**3. Número de chamadas.** Custo total = custo por chamada × **número de chamadas**. Esse último fator é fácil de esquecer, mas é onde os **agents** ([capítulo 16](16-o-que-e-um-agent.md)) mordem o bolso: um agent não faz uma chamada por tarefa — ele **pensa, chama uma tool, lê o resultado, pensa de novo, chama outra**. Uma única tarefa pode virar 5, 10, 20 chamadas ao modelo. A alavanca: **reduza os passos**. Menos idas e voltas, prompts que resolvem em uma passada, e cuidado com loops que reprocessam o mesmo contexto crescente a cada volta.

> Ordem prática de ataque: a maior economia quase sempre está em **(1) modelo menor** e **(2) menos contexto**. Só depois pense em microtruques.

## Técnicas de economia (nome + intuição)

- **Caching (cache de prompt).** Muitos provedores permitem marcar o **prefixo fixo** do seu prompt (aquele system prompt gigante com regras e exemplos que se repete em toda chamada) para ser cobrado **muito mais barato** nas chamadas seguintes. Intuição: se o começo não muda, o provedor não precisa reprocessá-lo do zero — e repassa o desconto. Só ajuda **quando há repetição**.
- **Caching (cache de resposta).** Se a **mesma** pergunta chega de novo, não chame o modelo: guarde a resposta e devolva a guardada. Perguntas idênticas → resposta idêntica → custo zero na segunda vez.
- **Batching (processamento em lote).** Tem 10 mil textos para classificar? Em vez de 10 mil chamadas ao vivo, mande em **lote**, fora do horário de pico. Vários provedores cobram **mais barato** no modo batch em troca de você aceitar esperar. Intuição: trabalho previsível e sem pressa é mais fácil (e barato) de agendar.
- **Escolher o modelo por tarefa.** Já é a alavanca 1, mas vale como técnica do dia a dia: mantenha um modelo pequeno como padrão e só suba quando a tarefa exigir.
- **Streaming.** Mostrar a resposta **conforme é gerada**, palavra por palavra. Importante ser honesto: **streaming NÃO reduz custo** — você paga os mesmos tokens. O que ele melhora é a **latência percebida**: o usuário vê algo em 0,5s em vez de encarar tela travada por 5s. É a diferença entre "quebrou" e "está pensando".

```text
sem streaming:  [.................] (5s travado) → resposta
com streaming:  Olá... como... posso... ajudar...  (já aparecendo)
```

## Escala e produção

Custo resolvido, falta aguentar o tranco quando o volume sobe.

- **Rate limits (limite de taxa).** Provedores limitam quantas requisições/tokens você usa por minuto. Estourou, a API responde erro **429**. Em produção isso **vai** acontecer.
- **Retry com backoff exponencial.** Ao tomar um 429 ou uma falha temporária, não martele a API — espere e tente de novo, dobrando a espera a cada tentativa (1s, 2s, 4s, 8s...). Intuição: recuar dá tempo do provedor respirar, em vez de piorar o congestionamento.
- **Filas.** Em vez de disparar tudo de uma vez, **enfileire** as requisições e processe num ritmo que respeite o rate limit. Serve também para **jobs assíncronos**: tarefas pesadas (resumir um relatório enorme, gerar centenas de itens) não devem travar a tela do usuário — vão para a fila, rodam em segundo plano e avisam quando terminam. (Se você usa Redis + Bull, ou Celery, é exatamente esse padrão.)
- **Monitorar custo e uso.** Você não controla o que não mede. A resposta da API traz o campo **`usage`** ([capítulo 05](05-o-que-sao-tokens.md) e o exemplo [`examples/chamar-api`](../examples/chamar-api)), que diz exatamente quantos tokens de entrada e saída aquela chamada gastou — o número pelo qual você é cobrado. Acompanhe **custo por dia / por usuário / por feature**, **tokens médios por requisição** (um pico denuncia prompt inchado) e **taxa de 429**. E configure **alerta de custo**: a história clássica de IA em produção é a fatura-surpresa no fim do mês.

## Por dentro: para onde o dinheiro vai

Toda a fatura de um LLM cabe numa fórmula. Não tem mágica, tem multiplicação:

```text
custo_total ≈ (tokens_entrada + tokens_saída) × preço × número_de_chamadas
                        │                         │            │
                  alavanca 2 e 3            alavanca 1     alavanca 3
                  (contexto/saída)       (modelo escolhido)  (volume/agents)
```

Otimizar custo é, literalmente, **empurrar um desses fatores para baixo**:

- Diminuir `tokens_entrada` → prompt enxuto + RAG em vez de despejar tudo.
- Diminuir `tokens_saída` → limitar o máximo de tokens de resposta; pedir "sim/não" quando é só isso que você precisa.
- Diminuir `preço` → modelo menor / roteamento por dificuldade.
- Diminuir `número_de_chamadas` → menos passos de agent, cache de respostas repetidas.

E é por isso que **medir vem antes de otimizar**: sem olhar o `usage` e o custo por feature, você não sabe **qual** fator está grande — e pode passar horas cortando 50 tokens de um prompt enquanto o verdadeiro rombo é um agent dando 15 voltas por tarefa. Corte o fator que domina, não o que é fácil.

## Checklist de produção

```text
[ ] Modelo escolhido por tarefa (o menor que resolve) — alavanca 1
[ ] Prompts enxutos; RAG manda só o relevante        — alavanca 2
[ ] Nº de chamadas sob controle (agents com poucos passos) — alavanca 3
[ ] Cache de respostas e/ou de prompt onde há repetição
[ ] Limite de tokens de saída definido
[ ] Streaming para melhorar a latência percebida
[ ] Retry com backoff exponencial para erro 429
[ ] Filas para volume; jobs assíncronos para tarefas pesadas
[ ] Monitoramento de custo, tokens (usage), erros e latência
[ ] Alerta de custo configurado
```

## Próximos passos

Você chegou ao fim do IA4Noobs. Saiu do "o que é um modelo" e chegou em "como colocar IA no mundo real com segurança, qualidade e custo sob controle". Esse é o conhecimento que a maioria dos tutoriais pula.

E agora? **Construa.** Pegue uma ideia pequena, monte o backend, escreva um eval set, meça, ajuste e observe o custo. A prática é onde tudo se conecta. Leia a documentação do provedor que você escolher — preços e limites mudam, e ler a fonte oficial é um superpoder.

Por fim: o **IA4Noobs é open-source e feito pela comunidade**. Achou um erro? Tem um exemplo melhor? Quer escrever um capítulo novo? **Contribua.** Abra uma issue, mande um pull request, compartilhe com quem está começando. Ensinar é a melhor forma de aprender — e é assim que o 4noobs cresce. Bons builds! 🚀

## Exercício

1. **Custo mensal de uma feature.** Uma requisição típica usa 3.000 tokens de entrada e 800 de saída. Com preço na ordem de US$ 0,15/milhão (entrada) e US$ 0,60/milhão (saída), calcule o custo de **uma** chamada. Depois multiplique por 50.000 chamadas/mês. Quanto dá?
2. **Ache a maior alavanca.** Neste cenário, você paga US$ 900/mês. A feature usa o modelo topo de linha para uma tarefa simples, manda um documento de 20 mil tokens em toda chamada e faz 1 chamada por requisição. Qual das **3 alavancas** cortaria mais custo aqui, e por quê?
3. **Custo de um agent.** Um agent faz **5 chamadas** ao modelo para completar 1 tarefa, cada chamada com ~1.500 tokens de entrada e ~300 de saída. Calcule o custo de **uma tarefa** e depois de **10.000 tarefas/mês**. Compare com o mesmo volume se você reduzisse o agent para 3 chamadas.

---

<div align="center">

[« 27 - Como avaliar respostas de IA](27-como-avaliar-respostas-de-ia.md) — [Índice](../README.md#roadmap) — [29 - Projeto final: um assistente de FAQ com RAG »](29-projeto-final-faq-rag.md)

</div>
