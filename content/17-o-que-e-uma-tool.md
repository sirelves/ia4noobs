# 17 - O que é uma Tool

No [capítulo 16](16-o-que-e-um-agent.md) vimos que o que dá autonomia a um agent são as **tools**. Agora vamos entender o que elas são de verdade — e, principalmente, o mecanismo exato pelo qual um modelo as usa. Spoiler: o modelo **decide**, mas quem **executa** é o seu código. Essa separação é a ideia mais importante do capítulo.

## O que é uma tool

Uma **tool** (ferramenta) é uma capacidade que você dá ao modelo para **agir no mundo**, em vez de só falar sobre ele.

Lembra do [capítulo 04](04-como-o-chatgpt-funciona.md)? Um LLM, sozinho, só faz uma coisa: gera texto prevendo o próximo token. Ele não sabe que horas são agora, não acessa a internet, não lê o seu disco e é ruim de conta (vimos no [capítulo 05](05-o-que-sao-tokens.md) por que erra `4327 × 8`). A tool é a **mão** que falta ao cérebro: uma função de verdade, escrita por você, que o modelo pode pedir para rodar.

Exemplos típicos:

- **Buscar na web** — para informação atual, que não estava no treino.
- **Calcular** — para fazer contas com precisão, sem chutar tokens.
- **Ler um arquivo** — para acessar dados que estão no seu disco.
- **Chamar uma API** — previsão do tempo, cotação do dólar, enviar um e-mail.
- **Consultar um banco de dados** — buscar registros de um sistema real.

Cada tool é um "superpoder" específico que você empresta ao modelo. E a mágica é que **o modelo escolhe sozinho** quando e como usar cada um.

## Por dentro: o ciclo real de function calling

O nome técnico é **function calling** (ou **tool calling**). Muita gente imagina que o modelo "roda a função". Não é isso. O que acontece é um ciclo de **4 passos**, e vale ver o formato real (estilo API da OpenAI). A estrutura JSON abaixo é a de verdade; os textos de resultado são ilustrativos.

**Passo 1 — Você DECLARA a tool.** Antes de tudo, você entrega ao modelo uma "ficha" de cada tool, no formato **JSON Schema**: nome, descrição e os parâmetros que ela aceita (com tipos).

```json
{
  "type": "function",
  "function": {
    "name": "consultar_clima",
    "description": "Retorna o clima atual de uma cidade",
    "parameters": {
      "type": "object",
      "properties": {
        "cidade": { "type": "string", "description": "Nome da cidade, ex: São Paulo" },
        "unidade": { "type": "string", "enum": ["celsius", "fahrenheit"] }
      },
      "required": ["cidade"]
    }
  }
}
```

**Passo 2 — O modelo PEDE para chamar a tool.** O usuário pergunta "qual o clima em São Paulo?". Em vez de responder texto, o modelo devolve um `tool_call`: o nome da função e os argumentos que **ele mesmo** montou, em JSON.

```json
{
  "role": "assistant",
  "tool_calls": [
    {
      "id": "call_abc123",
      "type": "function",
      "function": {
        "name": "consultar_clima",
        "arguments": "{\"cidade\": \"São Paulo\", \"unidade\": \"celsius\"}"
      }
    }
  ]
}
```

Ponto-chave: **o modelo não executou nada.** Ele só disse "quero chamar `consultar_clima` com estes argumentos". É como preencher um pedido e passar para o balcão.

**Passo 3 — SEU código executa de verdade.** O seu programa lê esse pedido, chama a função Python (ou JS, ou o que for) real, e devolve o resultado ao modelo, marcado com o mesmo `id` da chamada.

```json
{
  "role": "tool",
  "tool_call_id": "call_abc123",
  "content": "{\"temp\": 23, \"condicao\": \"parcialmente nublado\"}"
}
```

**Passo 4 — O modelo LÊ o resultado e responde.** Agora, com o dado real em mãos, o modelo escreve a resposta final em linguagem natural:

> "Agora está 23 °C em São Paulo, com tempo parcialmente nublado."

Resumindo o loop, guarde esta frase:

> **O modelo é o cérebro que DECIDE; a tool é a mão que EXECUTA.**

Por que o modelo consegue produzir aquele JSON tão certinho no passo 2? Porque ele foi **treinado** para isso. Function calling é um caso de **saída estruturada** (que vimos no [capítulo 11](11-como-estruturar-respostas.md)): em vez de texto livre, o modelo emite um JSON que **nomeia** uma função e preenche seus argumentos, seguindo o schema que você declarou. Ele não tem acesso ao código da função nem à internet — ele só é muito bom em produzir o "pedido" no formato certo. Rodar o pedido é problema do seu programa.

## A descrição é o que faz o modelo acertar

Aqui está a parte que muita gente erra. **O modelo escolhe a tool lendo a descrição e os tipos dos parâmetros** — nada mais. Ele não vê o código por dentro. Se a descrição for ruim, ele usa a ferramenta errada, na hora errada, ou com o argumento errado.

- **Ruim**: `"description": "busca dados"` — busca o quê? Quando usar?
- **Boa**: `"description": "Busca a cotação atual de uma moeda em reais. Use quando o usuário pedir preço de dólar, euro, bitcoin, etc."`

Trate a descrição como se estivesse explicando para um colega **quando** acionar aquela função. Diga o que ela faz, quando usar e o que retorna. Os tipos dos parâmetros (`string`, `integer`, `boolean`) e restrições como `enum` também ajudam: eles dizem ao modelo o formato exato de cada argumento.

Isso fica lindo de ver no exemplo real [`examples/mcp-hello`](../examples/mcp-hello). Lá, cada tool é só uma função Python comum, e **a docstring da função É a descrição da tool**:

```python
@mcp.tool()
def somar(a: int, b: int) -> int:
    """Soma dois numeros inteiros e retorna o resultado.

    Use quando o usuario pedir para somar, adicionar ou calcular o total
    de dois numeros.
    """
    return a + b
```

Repare: as anotações de tipo (`a: int, b: int`) viram o schema dos parâmetros, e a docstring vira a `description`. É exatamente o JSON Schema do passo 1, só que gerado automaticamente a partir do código.

## Tools, agents e MCP

Volte ao [capítulo 16](16-o-que-e-um-agent.md): um agent é um loop que **pensa, age e observa**. Cada "agir" desse loop é, literalmente, **uma tool call** — os 4 passos que acabamos de ver, repetidos quantas vezes forem necessárias. É assim que o agent lê um arquivo, decide o que fazer com o conteúdo, chama outra tool, e vai encadeando.

E há um jeito **padrão** de expor tools para qualquer IA, sem reescrever tudo para cada modelo: o **MCP** (Model Context Protocol), que veremos no [capítulo 21](21-o-que-e-mcp.md). O `examples/mcp-hello` é justamente um servidor MCP mínimo. A ideia: você declara suas tools uma vez, num servidor MCP, e qualquer app de IA compatível passa a poder usá-las.

## Limites e segurança (a parte honesta)

O modelo **erra**. Como ele só decide com base na descrição, ele pode:

- **escolher a tool errada** (chamar `apagar_arquivo` quando você queria `ler_arquivo`);
- **inventar um argumento** que não faz sentido, ou num formato inválido.

Por isso, regra de ouro: **seu código deve VALIDAR tudo que vem do passo 2 antes de executar.** Nunca confie cegamente nos argumentos que o modelo montou — trate-os como entrada de um usuário desconhecido.

E cuidado redobrado com tools **poderosas**. Uma ferramenta que apaga arquivos, gasta dinheiro, envia e-mails ou mexe num banco de produção é perigosa nas mãos de um modelo que, vez ou outra, erra. Duas defesas simples:

1. **Dê só o necessário.** Se o agent só precisa ler, não entregue uma tool que também apaga.
2. **Confirme ações destrutivas.** Antes de executar algo irreversível, peça confirmação humana. Aprofundamos isso no [capítulo 26](26-seguranca-em-ia.md).

Descrições claras reduzem os erros; validação e permissões mínimas contêm o estrago quando o erro acontece mesmo assim.

## Exercício

1. Pegue uma das tools que você listou no exercício do [capítulo 16](16-o-que-e-um-agent.md).
2. Escreva a **declaração** dela em JSON, com `name`, `description` e `parameters` (com o `type` de cada parâmetro). Capriche na `description`: deixe claro **o que** faz e **quando** o modelo deve usá-la.
3. Simule o passo 2: escreva o `tool_call` que o modelo geraria para uma pergunta específica — qual argumento ele passaria?
4. Pense numa tool **perigosa** (apagar, pagar, enviar). Como você a protegeria? Escreva uma validação que seu código faria antes de executar, e diga se ela pediria confirmação humana.

---

<div align="center">

[« 16 - O que é um Agent](16-o-que-e-um-agent.md) — [Índice](../README.md#roadmap) — [18 - O que são Skills »](18-o-que-sao-skills.md)

</div>
