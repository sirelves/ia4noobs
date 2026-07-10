# 24 - Rodando modelos localmente

Até aqui, quase tudo dependeu de uma **API** na nuvem: você manda o prompt para a OpenAI, a Anthropic ou o Google, e eles respondem. Mas dá para rodar um modelo de IA **na sua própria máquina** — de graça, sem chave de API e até sem internet. Neste capítulo você entende quando isso vale a pena, e principalmente **por que** um modelo cabe (ou não) no seu computador.

## Por que rodar local?

Três motivos principais:

- **Privacidade.** Os dados **não saem** do seu computador. Nada é enviado para uma empresa. Ótimo para informação sensível.
- **Custo.** Não tem cobrança por token. Depois de baixar o modelo, usar é "de graça" (você só paga a energia e o hardware que já tem).
- **Funciona offline.** Sem depender de internet nem da API estar no ar.

Isso é possível porque existem **modelos abertos** (lembra do [capítulo 07](07-escolhendo-o-modelo-certo.md)?) como Llama, Mistral, Qwen e outros, que você pode baixar e executar.

## A ferramenta mais fácil: Ollama

Rodar um LLM na mão era complicado. O **Ollama** simplificou isso a ponto de virar dois comandos. Ele cuida de baixar o modelo e servir uma API local na sua máquina.

O fluxo é este:

```text
[1] Instala o Ollama          (uma vez)
        |
        v
[2] Baixa um modelo:  ollama pull llama3.2
        |
        v
[3] Conversa:  ollama run llama3.2
        |
        v
   Ollama também abre uma API local em http://localhost:11434
   (para seus programas chamarem, igual você faria com a OpenAI)
```

Passo a passo:

1. Instale o Ollama em [ollama.com](https://ollama.com) (Windows, Mac e Linux).
2. Baixe um modelo pequeno: `ollama pull llama3.2`
3. Converse no terminal: `ollama run llama3.2`

Pronto — você tem uma IA rodando no seu computador.

## O tamanho do modelo: parâmetros

Modelos abertos vêm em tamanhos, medidos em **parâmetros** — tipo 1B, 8B, 70B (B = bilhões). Um **parâmetro** é um número que o modelo aprendeu no treino (voltando ao [glossário](glossario.md): são os "pesos" ajustados que guardam o conhecimento). Um modelo "7B" tem 7 bilhões desses números.

E aqui está a intuição que explica tudo neste capítulo: **cada parâmetro precisa ficar guardado na memória enquanto o modelo roda.** Não dá para prever o próximo token sem passar por todos os parâmetros. Então o tamanho do modelo em memória é, grosso modo:

```text
memória ≈ número de parâmetros × bytes por parâmetro
```

Se cada parâmetro ocupasse 2 bytes (o formato "16-bit", padrão de muitos modelos), um modelo 7B pediria mais ou menos:

```text
7.000.000.000 parâmetros × 2 bytes ≈ 14 GB
```

Ou seja: **um 7B em 16-bit quer uns 14 GB** de RAM (ou de VRAM, se for na GPU). Um 70B quer ~140 GB — por isso ele não roda num notebook comum, mas um 7B roda. Não é magia: é multiplicação. (Os números são **aproximados** e ignoram o custo extra do contexto e do sistema; servem para ordem de grandeza.)

| Tamanho | Roda em | Qualidade |
|---|---|---|
| Pequeno (1B–3B) | Quase qualquer notebook | Ok para tarefas simples |
| Médio (7B–13B) | Máquina boa, uns 16 GB de RAM | Bem útil no dia a dia |
| Grande (70B+) | Precisa de GPU forte / muita RAM | Perto dos modelos de API |

Regra prática: pegue um modelo **pequeno ou médio** e veja se dá conta. Só suba de tamanho se precisar.

## Quantização: como caber num hardware modesto

Se cada parâmetro custa memória, a saída óbvia para caber é: **fazer cada parâmetro ocupar menos**. É exatamente isso que a **quantização** faz.

A intuição: os pesos são números com casas decimais. No formato original (16-bit), cada peso usa 2 bytes e guarda muita precisão. A quantização **arredonda** esses números para uma representação mais grosseira — por exemplo, **4 bits por parâmetro** em vez de 16. Menos bits, menos memória, com uma **pequena perda de qualidade** (o modelo fica levemente menos preciso, mas continua funcionando bem para a maioria das tarefas).

Voltando à conta, com 4 bits (0,5 byte) por parâmetro:

```text
7B em 16-bit:  7 bi × 2 bytes    ≈ 14 GB
7B em  4-bit:  7 bi × 0,5 byte   ≈  4 GB   (aproximado)
```

O **mesmo modelo** passa de ~14 GB para ~4 GB. É isso que permite rodar um 7B decente num notebook com 8 GB de RAM. No Ollama, quando você faz `ollama pull llama3.2`, normalmente já vem uma versão quantizada (tipo `Q4`) por padrão — é por isso que o download tem uns poucos GB, e não dezenas.

> **Analogia:** é como salvar uma foto em JPEG com mais compressão. O arquivo fica muito menor e, de longe, você quase não nota diferença. Só olhando bem de perto aparecem os "borrões". Quantizar demais (2 bits, 1 bit) é comprimir até estragar — aí a qualidade cai de verdade.

## Por dentro: o trade-off memória × qualidade

Juntando os dois mecanismos deste capítulo — **parâmetros** definem quanta memória o modelo precisa, e **quantização** encolhe o custo de cada parâmetro:

```text
             precisão (bits/parâmetro)
   16-bit ──────────────────────────────►  4-bit
   ▲                                          ▲
   │ mais memória                mais leve    │
   │ máxima qualidade    pequena perda de     │
   │ (~14 GB p/ 7B)      qualidade (~4 GB)     │
```

O ponto-chave para escolher: **um modelo maior, porém quantizado, quase sempre bate um modelo menor em precisão cheia.** Um 13B em 4-bit (~7 GB) tende a ser melhor que um 7B em 16-bit (~14 GB) — e ainda ocupa menos memória. Por isso a pergunta certa não é só "qual tamanho?", mas "qual o maior modelo que **cabe** na minha máquina depois de quantizado?". Cabe na memória → roda. Não cabe → ou trava, ou fica lento porque começa a usar o disco.

## A API local: pluga igual a uma API paga

O detalhe mais poderoso: além do chat no terminal, o Ollama abre uma **API HTTP** em `http://localhost:11434`. Do ponto de vista do seu código, isso é só **outro endpoint** — em vez de mandar a requisição para os servidores da OpenAI, você manda para `localhost`. O formato é praticamente o mesmo (envia mensagens, recebe a resposta).

Isso significa que trocar "nuvem" por "local" pode ser mudar **uma linha de configuração** (a URL base) no seu programa. Todo o resto — prompts, tools, o loop de conversa — continua igual. Tem um exemplo mínimo, sem nenhuma dependência externa, em [`examples/modelo-local`](../examples/modelo-local).

## Quando vale (e quando não vale)

| Use local quando... | Use API na nuvem quando... |
|---|---|
| Os dados são sensíveis | Você precisa da qualidade de ponta |
| Quer custo previsível / zero por uso | Não quer gerenciar hardware |
| Precisa funcionar offline | O volume é alto e variável |
| Está estudando / experimentando | A tarefa é difícil demais para modelo pequeno |

A conta de custo (local vs. nuvem, hardware vs. por-token) aparece em detalhe no [capítulo 28](28-custos-e-escalabilidade.md).

## Seja honesto: os limites

- **Qualidade menor.** Um modelo que roda no seu notebook não é páreo para os maiores modelos de API em tarefas difíceis. É um trade-off real.
- **Precisa de máquina.** Modelos maiores exigem bastante RAM e, de preferência, GPU. Sem hardware, você fica só nos pequenos.
- **Você vira o responsável.** Atualização, disponibilidade e manutenção passam a ser problema seu, não de um fornecedor.
- **Consome recursos.** Enquanto roda, o modelo come RAM/CPU/GPU da sua máquina.

> **Aviso de validade:** ferramentas, nomes de modelos e tamanhos de download **mudam rápido**. Use as contas deste capítulo como **ordem de grandeza**, não como número exato — e confira o tamanho real na página do modelo antes de baixar.

## Exercício

1. **Estime a memória.** Sem baixar nada, calcule a RAM aproximada para: (a) um modelo 8B em 16-bit; (b) o mesmo 8B em 4-bit; (c) um 70B em 4-bit. Use `parâmetros × bytes por parâmetro`. Qual desses caberia na sua máquina?
2. **Compare dois tamanhos.** Instale o Ollama, baixe o `llama3.2` e um segundo modelo de tamanho diferente. Faça a **mesma pergunta** nos dois e note a diferença de qualidade **e** de velocidade.
3. **Decida local vs. nuvem.** Liste dois casos do seu dia a dia em que rodar local faria sentido (pense em privacidade ou offline), e dois em que a API na nuvem seria melhor. Justifique cada um em uma frase.

---

<div align="center">

[« 23 - Criando seu primeiro MCP](23-criando-seu-primeiro-mcp.md) — [Índice](../README.md#roadmap) — [25 - Como criar aplicações com IA »](25-como-criar-aplicacoes-com-ia.md)

</div>
