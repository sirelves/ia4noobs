# 07 - Escolhendo o modelo certo

Você já entendeu como um LLM funciona, o que são tokens e o que é a janela de contexto. Agora bate a pergunta prática: **qual IA eu uso?** ChatGPT? Claude? Gemini? Um modelo aberto rodando na minha máquina?

Não existe "o melhor modelo". Essa frase parece papo furado até você perceber uma coisa: **"melhor" não é um número, é uma soma de eixos que você pondera conforme a tarefa.** Um modelo pode ser o melhor em qualidade e o pior em custo. Outro é mediano em tudo, mas roda offline. Este capítulo te ensina a decompor "melhor" nesses eixos e a **medir** — em vez de acreditar em ranking de internet.

## "Melhor" se decompõe em eixos

Antes de escolher, saiba o que você está comparando. Cada eixo abaixo é mensurável, e a sua tarefa dá o peso de cada um:

| Eixo | O que é | Quando pesa muito |
|---|---|---|
| **Qualidade** | Acerta a resposta, segue instrução, raciocina | Código difícil, análise, texto que vai pra fora |
| **Latência** | Quão rápido responde (o "time to first token" e a velocidade de geração) | Chat ao vivo, autocomplete, algo que o usuário espera na tela |
| **Custo por token** | Preço de entrada + saída (revê o [capítulo 05](05-o-que-sao-tokens.md)) | Grande volume: milhares de chamadas/dia |
| **Janela de contexto** | Quanto texto cabe de uma vez | Livros, muitos documentos, históricos longos |
| **Multimodal** | Entende/gera imagem, áudio, vídeo | Ler uma foto, transcrever, analisar gráfico ([cap. 03](03-ia-multimodal.md)) |
| **Aberto vs. fechado** | Você baixa e roda, ou chama uma API | Controle, custo fixo, rodar offline |
| **Privacidade** | Os dados saem da sua infra ou não | Dado sensível, saúde, jurídico, LGPD |

O erro do iniciante é olhar só um eixo (qualidade) e ignorar os outros quatro que vão doer depois (custo e latência em produção, privacidade num dado sensível).

## Os grandes nomes (retrato do momento)

A IA muda muito rápido. Trate isto como uma foto de hoje, não como verdade eterna — em poucos meses os nomes de versão já mudaram.

| Família | Empresa | Costuma se destacar em |
|---|---|---|
| **GPT** (ChatGPT) | OpenAI | Uso geral, ecossistema grande, muitas integrações |
| **Claude** | Anthropic | Textos longos, código, seguir instruções com cuidado |
| **Gemini** | Google | Multimodal, integração com produtos Google, contexto enorme |
| **Llama** | Meta | Modelo **aberto**, roda na sua máquina/servidor |
| **Mistral / DeepSeek / Qwen** | Vários | Modelos abertos, boa relação qualidade/custo |

> Não decore essa tabela. O ponto é: há **modelos fechados** (você acessa por API/site de uma empresa) e **modelos abertos** (você pode baixar e rodar). Cada grupo tem seus trade-offs — os dois próximos quadros aprofundam isso.

## Benchmarks: úteis, mas não confie cegamente

**Benchmark** é um teste padronizado para medir modelos. Você vai esbarrar nestes:

- **MMLU**: milhares de questões de múltipla escolha (de história a medicina) medindo **conhecimento**. Vira um número tipo "88%".
- **Arena de preferência humana** (estilo **LMArena / Chatbot Arena**): a mesma pergunta vai pra dois modelos anônimos, uma pessoa vota qual respondeu melhor, e milhares de votos viram um **ranking** (um "Elo", como no xadrez). Mede o que a gente *sente* como melhor, não só acerto de prova.

Números redondos convencem. Mas há três armadilhas que quase ninguém comenta:

1. **Contaminação de dados.** O modelo treina em bilhões de páginas da internet — incluindo, às vezes, **o próprio gabarito do teste**. Aí ele não "raciocina", ele **lembra**. É como um aluno que decorou a prova vazada: nota alta, aprendizado zero.
2. **O benchmark não é a SUA tarefa.** MMLU mede questão de múltipla escolha. Se o seu trabalho é *resumir chamados de suporte em pt-BR*, o campeão do MMLU pode perder feio pra um modelo "pior" no ranking.
3. **Vira alvo.** Quando um teste fica famoso, as empresas passam a **otimizar pra ele**. O número sobe; a utilidade real, nem sempre. (É a Lei de Goodhart: "quando a métrica vira meta, ela deixa de ser boa métrica".)

Ranking serve pra montar a **lista curta** de 2 ou 3 candidatos. A decisão final é sua — e vem do teste a seguir.

## O método que importa: seu próprio mini-eval

Esta é a parte mais valiosa do capítulo. Em vez de perguntar "qual o melhor modelo?", você monta um **mini-eval**: um mini-teste com a *sua* tarefa. É reproduzível e leva uma tarde.

1. **Junte 10 a 20 casos reais** da sua tarefa. Reais mesmo — e-mails que você já classificou, bugs que já resolveu, textos que já resumiu.
2. **Escreva a resposta esperada** de cada um (o "gabarito"). Sem gabarito não há como comparar.
3. **Rode o mesmo prompt** nos 2-3 candidatos da lista curta.
4. **Anote três colunas**: qualidade (acertou?), custo (tokens gastos) e velocidade.

O resultado vira uma tabelinha assim (**números ilustrativos** — os seus vão ser outros):

| Modelo | Acertos (20 casos) | Custo (20 chamadas) | Tempo médio |
|---|---|---|---|
| Pequeno/barato | 17/20 (85%) | US$ 0,004 | 0,8 s |
| Médio | 19/20 (95%) | US$ 0,03 | 1,5 s |
| Topo de linha | 20/20 (100%) | US$ 0,20 | 4 s |

Olhando *esta* tabela (e não o ranking global), a decisão fica óbvia pro seu caso. Como julgar "acertou ou não" de forma justa é assunto do [capítulo 27 - Como avaliar respostas de IA](27-como-avaliar-respostas-de-ia.md).

## A conta de custo × qualidade (e o roteamento)

Repare nos múltiplos da tabela acima (**ilustrativos**): o modelo topo custou ~**50x** mais que o pequeno. Na prática, um modelo de ponta costuma custar **10x a 20x** mais por token que um pequeno da mesma família. Vale sempre pagar isso? Faça a conta.

O pequeno acertou **85%**. Ou seja, ele já resolve a maioria — só tropeça nos casos difíceis. A jogada esperta é o **roteamento por dificuldade**:

```text
Caso chega
   │
   ▼
Roda no modelo PEQUENO (barato, rápido)
   │
   ├── resolveu bem? → entrega (foi ~85% dos casos, custo baixo)
   │
   └── caso difícil / baixa confiança? → manda pro modelo TOPO
                                          (só nos ~15% que precisam)
```

Se o pequeno faz 85% a US$ 0,0002/caso e o topo faz o resto a US$ 0,01, o custo médio despenca perto do modelo pequeno — mas a qualidade final beira a do topo. **Você paga o carro caro só na viagem longa, não pra ir na padaria.** É assim que produtos sérios seguram a conta sem perder qualidade.

## Aberto vs. fechado

A primeira grande bifurcação de infraestrutura:

| | Modelo fechado (API) | Modelo aberto (você roda) |
|---|---|---|
| Como usa | Chamada a uma API paga | Baixa e roda (sua máquina/servidor) |
| Qualidade de ponta | Geralmente os mais fortes | Bons, atrás dos top fechados |
| Custo | Paga por uso (tokens) | Sem custo por token, mas paga a máquina/GPU |
| Privacidade | Dados saem para o fornecedor | Dados **não saem** da sua infra |
| Facilidade | Muito fácil de começar | Exige setup e hardware |

Vamos rodar um modelo aberto na prática no [capítulo 24 - Rodando modelos localmente](24-rodando-modelos-localmente.md).

## Tamanho: nem tudo precisa do topo de linha

Cada família tem versões de tamanhos diferentes — em geral uma **rápida e barata** e uma **poderosa e cara**. O erro clássico do iniciante é usar sempre a mais cara.

Pense como quem escolhe transporte:

- Ir à padaria da esquina? A pé (modelo pequeno, rápido, barato).
- Atravessar a cidade? De carro (modelo médio).
- Mudar de estado? Avião (modelo topo, para o que é realmente difícil).

Tarefas simples e em **grande volume** (classificar comentários, extrair um campo de um texto) pedem modelo pequeno. Raciocínio complexo, código difícil, análise longa pedem os grandes.

## Seja honesto: os limites

- **Rankings envelhecem em semanas.** Todo mês tem modelo novo. Não se apegue a "o modelo X é o melhor" — reavalie de vez em quando.
- **"Melhor no teste" ≠ melhor pra você.** Um modelo pode liderar o benchmark e responder pior no seu caso específico. Por isso o mini-eval existe.
- **Trocar de modelo dá trabalho.** Um prompt afinado num modelo quase sempre precisa de ajuste em outro. Não é 100% "plug and play".
- **Mais caro nem sempre é melhor.** Muita gente paga pelo topo em tarefas que um modelo barato faria igual — só nunca mediu.

## Exercício

1. **Monte o esqueleto do seu mini-eval.** Escolha uma tarefa que você faria com IA (resumir e-mails, gerar testes, classificar feedback) e escreva **5 casos de teste**: a entrada e a resposta esperada de cada um.
2. **Rode um mesmo prompt em duas ferramentas** diferentes (ex.: ChatGPT e Gemini, versões gratuitas) com esses casos. Preencha as três colunas: qual acertou mais? Qual foi mais rápido?
3. **Classifique por dificuldade.** Para qual destas você usaria um modelo **pequeno e barato**, e por quê: (a) escrever um contrato, (b) marcar 10 mil avaliações como positivas ou negativas, (c) explicar um bug complexo? Qual dessas você rotearia pro modelo topo?

---

<div align="center">

[« 06 - O que é Janela de Contexto](06-o-que-e-janela-de-contexto.md) — [Índice](../README.md#roadmap) — [08 - O que é Prompt Engineering »](08-o-que-e-prompt-engineering.md)

</div>
