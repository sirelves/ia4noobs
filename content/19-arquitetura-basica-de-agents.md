# 19 - Arquitetura básica de Agents

Já vimos as peças soltas: o [loop de um agent](16-o-que-e-um-agent.md), as [tools](17-o-que-e-uma-tool.md), as [skills](18-o-que-sao-skills.md). Agora vamos **juntar tudo** num único desenho e entender como um agent é montado por dentro — quem decide, quem lembra, quem executa e o que impede a coisa de rodar para sempre.

## Os cinco componentes

Um agent é feito de cinco partes. Cada uma tem um nome e um papel bem definido — e a intuição fica fácil se você pensar numa pessoa trabalhando numa tarefa.

**1. Cérebro — o LLM.** É o modelo que **decide o próximo passo**. Ele lê a situação, raciocina e escolhe: chamo uma tool? qual? ou já respondo? O cérebro não executa nada — ele só decide. Guarde essa frase, ela é a chave do capítulo.

**2. Memória — o que ele sabe.** Vem em dois tipos, e a diferença é prática, não filosófica:
- **Curto prazo** é a [janela de contexto](06-o-que-e-janela-de-contexto.md): o objetivo atual, os passos já dados, os resultados recentes. É a "memória de trabalho" da tarefa. Acabou a conversa, sumiu.
- **Longo prazo** é o que **persiste**: arquivos, um banco de dados, ou um [banco vetorial](15-o-que-e-banco-vetorial.md) de onde ele busca por significado. É onde fica o que não cabe (ou não deveria caber) na janela toda hora.

**3. Planejamento — quebrar o objetivo em passos.** "Reservar uma viagem" não é uma ação; são várias: buscar voos, comparar preços, escolher hotel, somar o total. O planejamento é o cérebro **decompondo** o objetivo grande em passos pequenos e executáveis. Às vezes isso é um passo explícito ("primeiro faça uma lista"), às vezes está diluído no raciocínio de cada volta.

**4. Tools — as mãos.** São as capacidades de **agir** no mundo: buscar na web, ler um arquivo, chamar uma API, rodar uma conta. O cérebro decide, as mãos executam. Detalhamos isso no [capítulo 17](17-o-que-e-uma-tool.md).

**5. Orquestrador / Loop — o motor.** É o ciclo **decidir → agir → observar → repetir**, com uma **condição de parada**. É ele que costura os quatro componentes acima e sabe quando encerrar. Sem condição de parada, não é um agent útil — é uma conta de luz.

### O diagrama

```
                   ┌──────────────────────────────┐
                   │   OBJETIVO + INSTRUÇÕES        │
                   │   (o que fazer, as regras)     │
                   └───────────────┬────────────────┘
                                   ▼
   ┌───────────┐         ┌───────────────────┐         ┌───────────┐
   │  MEMÓRIA   │◄───────►│   CÉREBRO (LLM)    │◄───────►│   TOOLS    │
   │ curto:      │  lê /   │  decide o próximo  │ chama / │  buscar,   │
   │  contexto   │ escreve │  passo · planeja   │ recebe  │  ler, API, │
   │ longo:      │         │  (NÃO executa)     │         │  calcular  │
   │  arq/banco  │         └─────────┬──────────┘         └─────┬──────┘
   └───────────┘                    │                          │
        ▲                           ▼                          │
        │              ┌──────────────────────────┐            │
        │              │   ORQUESTRADOR / LOOP      │            │
        └──────────────┤  decide→age→observa→...   │◄───────────┘
          resume/salva  │  PARA quando: concluiu,   │  observação
                        │  bateu max de passos,     │  (resultado
                        │  ou deu erro fatal        │   da tool)
                        └──────────────────────────┘
```

> **Ilustração** — os nomes e o fluxo são reais; o layout é didático. Num framework de verdade (LangGraph, o Agents SDK da OpenAI, o Claude Agent SDK) esses blocos existem, mas com outros nomes e mais fios.

## Dois jeitos de controlar o loop: ReAct vs. plan-and-execute

Como o cérebro conduz o trabalho? Há dois padrões clássicos, e a diferença é *quando* ele planeja.

**ReAct** (de *Reasoning + Acting*, raciocinar + agir) **intercala** pensar e agir a cada passo, reagindo ao que observa:

```
Pensamento: preciso da cotação do dólar hoje.
Ação:       buscar_web("cotação dólar hoje")
Observação: "R$ 5,40"
Pensamento: agora calculo 100 × 5,40.
Ação:       calcular("100 * 5.40")
Observação: "540"
Pensamento: tenho a resposta.
Resposta:   "100 dólares são R$ 540,00 hoje."
```

A força do ReAct é **reagir**: se a busca voltar vazia, ele muda o rumo na próxima volta. Serve para tarefas exploratórias, onde você não sabe de antemão os passos.

**Plan-and-execute** faz o contrário: o cérebro **planeja tudo primeiro** e só depois executa a lista.

```
Plano:  1. buscar voos SP→Recife    (ilustração)
        2. buscar hotel em Recife
        3. somar voo + hotel
        4. montar a resposta
Executa 1 → 2 → 3 → 4, um após o outro.
```

A força é **previsibilidade e custo**: o plano sai numa chamada, e os passos podem até rodar em paralelo. Serve para tarefas de estrutura conhecida. O preço é rigidez — se o passo 2 falhar, um plano "burro" segue reto. Por isso, na prática, se combinam: planeja no começo e **re-planeja** quando algo foge do esperado.

Regra de bolso: **tarefa imprevisível → ReAct; tarefa com receita conhecida → plan-and-execute.** Um assistente que pesquisa e vai ajustando o rumo pede ReAct; um robô que toda noite fecha o mesmo relatório em 4 etapas pede plan-and-execute.

## O problema que todo agent enfrenta: o contexto estoura

Repare no loop: a cada volta, o histórico **cresce**. Pensamento, ação, observação, pensamento, ação, observação... Vinte voltas depois, a janela de contexto está lotada — e ela [tem um teto](06-o-que-e-janela-de-contexto.md). Estourou, a coisa quebra ou fica cara, porque você [paga por token](05-o-que-sao-tokens.md) em toda chamada.

Três estratégias para segurar isso, geralmente combinadas:

- **Resumir o histórico antigo.** Trocar as 15 primeiras voltas por um parágrafo: "já busquei voos e hotel, total R$ 1.800". Perde detalhe, economiza espaço.
- **Empurrar para a memória longa.** Salvar o resultado num arquivo/banco e manter no contexto só um ponteiro ("resultados em `voos.json`").
- **Buscar sob demanda com [RAG](14-o-que-e-rag.md).** Em vez de carregar tudo, guardar num banco vetorial e trazer para o contexto só o trecho relevante para o passo atual.

A ideia comum às três: **o contexto é caro e finito, então trate-o como bancada de trabalho, não como depósito.** Você deixa na bancada só as ferramentas do passo atual; o resto fica guardado no armário (memória longa) e você busca quando precisa.

## Os freios: tratamento de erro e limites

Um agent erra e trava. Boa arquitetura é colocar os freios certos:

- **Validar a saída da tool.** A tool voltou o que devia? Um JSON quebrado ou uma resposta vazia precisam ser detectados — não repassados ao cérebro como se fossem verdade.
- **Retry com limite.** API caiu? Tenta de novo — mas no máximo 2 ou 3 vezes, senão você tenta o infinito.
- **Timeout.** Uma tool que não responde não pode congelar o agent para sempre. Corta após X segundos.
- **Máximo de passos.** O freio mais importante. Sem um teto (ex: "no máximo 15 passos"), um agent pode **entrar em loop** repetindo a mesma ação e **queimar dinheiro** sem parar. Bateu o limite, ele encerra e relata o que conseguiu.

## Por dentro

Aqui está a peça que confunde quase todo iniciante: **o LLM não roda nada sozinho.**

O orquestrador é **código comum** — um `while` em Python — que costura tudo. A cada volta ele faz isto:

```
memoria = [objetivo, instruções]     (ilustração do laço real)
passo = 0
enquanto passo < MAX_PASSOS:
    decisao = chama_o_LLM(memoria)          # 1. o cérebro DECIDE
    se decisao == "terminei":
        retorna resposta                     # 2. condição de parada
    resultado = executa_tool(decisao)        # 3. o CÓDIGO executa a mão
    memoria.append(decisao, resultado)       # 4. atualiza o histórico
    passo += 1                                # 5. e repete
```

Quando o cérebro "decide chamar `buscar_web`", ele não busca nada. Ele só **devolve um texto** dizendo "quero chamar `buscar_web` com esse argumento". Quem lê esse texto, chama a função de verdade e pega o resultado é o **orquestrador**. Depois o código enfia o resultado de volta na memória e **chama o LLM outra vez**, agora com o histórico atualizado. O LLM é sem estado: ele não "lembra" da volta anterior — quem lembra é a `memoria` que o código remonta e reenvia a cada chamada.

Ou seja: **o agent é um loop de código que re-consulta o cérebro repetidamente.** A "autonomia" não está no modelo; está no laço que insiste em perguntar de novo até a tarefa fechar.

## Limites honestos

- **Mais partes, mais pontos de falha.** Memória longa, planejamento, cinco tools — cada peça pode quebrar. Um agent com muitas engrenagens é mais difícil de depurar que um script direto.
- **Custo e latência.** Cada volta é uma chamada ao modelo. Um agent de 20 passos custa e demora muito mais que uma pergunta única. Isso pesa em escala — assunto do [capítulo 28](28-custos-e-escalabilidade.md).
- **Comece simples.** Não monte os cinco componentes de largada. Um cérebro + duas tools + um loop com teto já é um agent. Adicione memória longa quando o contexto realmente estourar, planejamento quando as tarefas ficarem longas. Componente só entra quando há um problema presente pedindo por ele.

## Exercício

Desenhe (em texto, como os diagramas acima) a arquitetura de um agent para uma tarefa à sua escolha — ex: "revisar meus e-mails e resumir os importantes".

1. **Cérebro**: qual a decisão típica que ele toma a cada passo?
2. **Tools**: liste pelo menos 2 que o agent precisaria.
3. **Memória**: o que fica no **curto prazo** (contexto) e o que vai para o **longo prazo** (arquivo/banco)? Justifique a divisão.
4. **Loop**: qual a **condição de parada** e qual o **máximo de passos** razoável para não queimar dinheiro?
5. **Controle**: essa tarefa combina mais com **ReAct** ou **plan-and-execute**? Por quê?

---

<div align="center">

[« 18 - O que são Skills](18-o-que-sao-skills.md) — [Índice](../README.md#roadmap) — [20 - Multi-Agent Systems »](20-multi-agent-systems.md)

</div>
