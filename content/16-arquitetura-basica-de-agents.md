# 16 - Arquitetura básica de Agents

Já vimos as peças soltas: o loop, as tools, as skills. Agora vamos **juntar tudo** e entender como um agent é montado por dentro.

## Os componentes de um agent

Um agent é feito de cinco partes principais. Uma boa analogia é pensar nele como uma pessoa trabalhando:

### 1. O modelo / LLM — o cérebro

É o LLM que **decide** o que fazer a cada passo. Ele é quem raciocina, interpreta os resultados e escolhe a próxima ação. Sem o modelo, não há decisão — só código burro.

### 2. Instruções / prompt de sistema — a personalidade e as regras

É o texto que define **quem o agent é e como deve se comportar**: o tom, as regras, o que pode e o que não pode fazer, o objetivo geral. É como o "contrato de trabalho" do agent.

```
Exemplo de prompt de sistema:
"Você é um assistente de pesquisa. Sempre cite suas fontes.
 Se não tiver certeza, diga que não sabe. Nunca invente dados."
```

### 3. Tools — as mãos

São as capacidades de **agir** no mundo (buscar na web, ler arquivos, chamar APIs). O cérebro decide, as mãos executam. Já vimos isso em detalhe no capítulo 14.

### 4. Memória — o que ele lembra

A memória vem em dois tipos:

- **Curto prazo (contexto)**: o que está acontecendo *agora* — o objetivo, os passos já dados, os resultados recentes. É a "memória de trabalho" da tarefa atual. Some quando a conversa acaba.
- **Longo prazo (banco / arquivos)**: informação que **persiste** entre conversas — guardada num banco de dados, em arquivos, ou num banco vetorial (lembra do capítulo 12?). É de onde o agent puxa coisas que aprendeu ou guardou antes.

### 5. O loop de execução — o ciclo de trabalho

É o motor que faz tudo girar: **decidir → chamar tool → observar → repetir**, com uma **condição de parada**. É o que vimos no capítulo 13, só que agora é ele que costura todos os componentes acima.

## O padrão ReAct (em alto nível)

Um padrão muito comum para montar esse loop se chama **ReAct** — de **Re**asoning + **Act**ing (raciocinar + agir).

A ideia é simples: a cada passo, o agent **alterna** entre **pensar** ("o que eu faço agora?") e **agir** (chamar uma tool). O raciocínio fica explícito antes de cada ação, o que ajuda o agent a tomar decisões melhores e fica mais fácil de depurar.

```
Pensamento: Preciso saber a cotação do dólar hoje.
Ação:       buscar_web("cotação dólar hoje")
Observação: "R$ 5,40"
Pensamento: Agora consigo calcular o valor em reais.
Ação:       calcular(100 * 5.40)
Observação: "540"
Pensamento: Tenho a resposta.
Resposta:   "100 dólares são R$ 540,00 hoje."
```

Não precisa decorar o nome — o importante é entender o ritmo: **pensa, age, observa; pensa, age, observa...** até concluir.

## Tratando erros e limites

Aqui entra a parte honesta. Um agent **não é perfeito** e precisa de freios:

- **Máximo de passos**: sem um limite, um agent pode **rodar para sempre** — entrar em loop repetindo a mesma ação. Por isso se define um teto (ex: "no máximo 15 passos"). Bateu o limite, ele para e relata o que conseguiu.
- **Erros de tool**: uma tool pode falhar (a API caiu, o arquivo não existe). O agent precisa saber lidar com o erro — tentar de novo, tentar outra abordagem, ou desistir com elegância.
- **Custo**: cada passo do loop é uma chamada ao modelo. Mais passos = **mais dinheiro** e mais tempo. Um agent que dá 30 voltas custa muito mais que um que resolve em 3. Limitar passos também controla o custo.

Resumindo: agents erram, podem travar em loop e custam mais que uma simples pergunta. Boa arquitetura é justamente colocar os freios certos.

## Juntando tudo: o diagrama

```
                    ┌───────────────────────────┐
                    │   INSTRUÇÕES / PROMPT      │
                    │   (personalidade, regras)  │
                    └────────────┬──────────────┘
                                 │
                                 ▼
   ┌──────────┐         ┌─────────────────┐         ┌──────────┐
   │ MEMÓRIA  │◄───────►│   MODELO / LLM  │◄───────►│  TOOLS   │
   │ curto +  │         │   (o cérebro)   │         │ (as mãos)│
   │ longo    │         └────────┬────────┘         └────┬─────┘
   │ prazo    │                  │                       │
   └──────────┘                  │  ┌────────────────────┘
                                 ▼  ▼
                    ┌───────────────────────────┐
                    │     LOOP DE EXECUÇÃO       │
                    │  decidir → agir → observar │
                    │  → repetir até concluir    │
                    │  (com máximo de passos)    │
                    └───────────────────────────┘
```

O **modelo** está no centro, lendo as **instruções**, consultando a **memória**, chamando as **tools** — tudo orquestrado pelo **loop**, que para quando a tarefa termina ou quando bate o limite de passos.

## Exercício

Desenhe (em texto mesmo, como os diagramas acima) a arquitetura de um agent para uma tarefa à sua escolha. Para cada componente, escreva o que ele seria no seu caso:

1. **Modelo**: qual o papel dele aqui?
2. **Instruções**: escreva 2 ou 3 regras do prompt de sistema.
3. **Tools**: liste pelo menos 2 tools que o agent precisaria.
4. **Memória**: o que precisaria ser lembrado a curto prazo? E a longo prazo?
5. **Loop**: qual seria a **condição de parada** e qual o **máximo de passos** razoável para evitar custo e loops infinitos?

---

<div align="center">

[« 15 - O que são Skills](15-o-que-sao-skills.md) — [Índice](../README.md#roadmap) — [17 - Multi-Agent Systems »](17-multi-agent-systems.md)

</div>
