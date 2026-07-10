# 22 - MCP Client e MCP Server

No capítulo anterior vimos *para que serve* o MCP. Agora vamos abrir a caixa e ver **como os dois lados conversam** — porque, no fim, MCP é só isso: dois programas trocando mensagens combinadas. Quando você entender quem fala o quê, o resto do guia (criar seu próprio server, plugar num app) vira detalhe.

## Os dois papéis: quem pede e quem entrega

O MCP segue um modelo **cliente-servidor**. São dois papéis, e a distinção é a coisa mais importante do capítulo:

- **MCP Client (cliente)**: vive **dentro de um host de IA** — um app que você já usa, tipo um chat, uma IDE ou um assistente de código. O client é o pedaço que **fala o protocolo** e se conecta aos servers. Ele faz duas coisas: **descobre** quais ferramentas existem e **manda executar** quando o modelo decide usar uma. Você quase nunca escreve um client — ele já vem pronto no app.
- **MCP Server (servidor)**: um programa separado que **expõe** ferramentas, dados e prompts. É o que **você** costuma escrever quando quer plugar a sua ferramenta ou a sua base de dados na IA. O [`examples/mcp-hello`](../examples/mcp-hello) deste guia é exatamente isso: um server pequeno com duas tools.

A relação é **N–N** no nível do host: um **host** fala com **vários** servers ao mesmo tempo (um de arquivos, um do GitHub, um do seu banco) — cada um por um client próprio, numa conexão 1:1 client↔server. E um mesmo server pode atender **vários** clients (o Claude Desktop hoje, uma IDE amanhã). Ninguém precisa saber quem está do outro lado — todos falam a mesma língua.

Vale separar dois termos que aparecem juntos:

- **Host**: a aplicação de IA inteira (ex.: o Claude Desktop, uma IDE). É quem conversa com o modelo.
- **Client**: o componente, *dentro* do host, que mantém a conexão com **um** server. Um host com três servers conectados tem três clients rodando.

```text
        HOST de IA (app de chat / IDE)
        ┌───────────────────────────────┐
        │   Modelo de IA (o "cérebro")  │
        │                               │
        │   ┌─────────┐   ┌─────────┐   │
        │   │ Client  │   │ Client  │   │
        │   └────┬────┘   └────┬────┘   │
        └────────┼─────────────┼────────┘
                 │             │
            ┌────▼────┐   ┌────▼────┐
            │ Server  │   │ Server  │
            │ Arquivos│   │ GitHub  │
            └─────────┘   └─────────┘
```

## A conversa, de verdade

MCP não é abstrato: é um punhado de mensagens em **JSON-RPC 2.0** (um formato padrão de "eu peço, você responde"). Vamos ver as mensagens **reais** que trafegam entre um client e um server, na ordem em que acontecem. Não precisa decorar — só reparar no padrão.

**Passo 1 — Aperto de mão (`initialize`).** Assim que conecta, o client se apresenta e diz qual versão do protocolo fala. É como duas pessoas confirmando que falam o mesmo idioma antes de começar.

```json
{ "jsonrpc": "2.0", "id": 1, "method": "initialize",
  "params": { "protocolVersion": "2024-11-05",
              "clientInfo": { "name": "meu-app", "version": "1.0" } } }
```

**Passo 2 — "O que você tem aí?" (`tools/list`).** O client pergunta ao server quais ferramentas ele oferece:

```json
{ "jsonrpc": "2.0", "id": 2, "method": "tools/list" }
```

E o server responde com a **vitrine** — cada tool com nome, descrição e o formato dos argumentos que espera (o `inputSchema`):

```json
{ "jsonrpc": "2.0", "id": 2,
  "result": {
    "tools": [
      { "name": "buscar_documento",
        "description": "Busca um documento pelo título",
        "inputSchema": {
          "type": "object",
          "properties": { "titulo": { "type": "string" } },
          "required": ["titulo"]
        } }
    ]
  } }
```

Repare: o server **se descreve sozinho**. Ele diz o que faz e o que precisa receber, num formato padrão. É por isso que **qualquer** client MCP entende **qualquer** server MCP sem integração feita à mão — é a "tomada universal" de que falamos no capítulo anterior. Aquela `description` é o mesmo papel da docstring no `mcp-hello`: é o texto que o modelo lê para decidir *quando* usar a ferramenta.

**Passo 3 — "Executa isso" (`tools/call`).** O modelo, no meio da conversa, decide usar a tool. O client então manda o server rodá-la, com os argumentos preenchidos:

```json
{ "jsonrpc": "2.0", "id": 3, "method": "tools/call",
  "params": { "name": "buscar_documento",
              "arguments": { "titulo": "política de troca" } } }
```

O server executa o código de verdade (consulta um banco, lê um arquivo, chama uma API) e devolve o resultado:

```json
{ "jsonrpc": "2.0", "id": 3,
  "result": { "content": [ { "type": "text",
              "text": "Trocas em até 30 dias com nota fiscal." } ] } }
```

E é isso. O modelo **nunca** toca a ferramenta direto: ele *pede* ao client, o client *chama* o server, o server *executa* e devolve. Esse intermediário é o que mantém tudo padronizado e controlável.

Além de **tools** (ações), o server também pode expor **resources** (dados para o modelo ler, tipo o conteúdo de um arquivo) e **prompts** (modelos de prompt prontos). O mecanismo é o mesmo — muda só o `method` (`resources/list`, `prompts/list`). O foco do guia são as tools, mas saiba que os outros dois existem.

## Por dentro: como o `id` costura pedido e resposta

Reparou que toda mensagem tem um campo `id`? Ele é a alma do JSON-RPC. O client pode disparar vários pedidos sem esperar cada resposta chegar — e as respostas podem voltar fora de ordem. O `id` é a **etiqueta** que casa cada resposta com o seu pedido: o client mandou `tools/call` com `"id": 3`, então quando chega uma mensagem com `"id": 3` no `result`, ele sabe que **aquilo** é a resposta daquela chamada, e não de outra. Pense numa lanchonete com senha: você pega a senha 3, e quando chamam "3!", é o seu pedido — não importa se o 4 ficou pronto antes.

O `initialize` do começo tem função parecida, só que para a **sessão inteira**: ele abre a conversa e faz os dois lados combinarem a versão do protocolo. Se as versões não forem compatíveis, é aqui que dá errado — antes de qualquer tool ser chamada. Handshake primeiro, trabalho depois.

## Transporte: por onde as mensagens viajam

Essas mensagens JSON precisam de um "cano" para trafegar. Os dois mais comuns:

- **stdio** — para servers **locais**, na sua máquina. O host **inicia o server como um processo** e conversa com ele pela entrada e saída padrão (o mesmo stdin/stdout de qualquer programa de terminal). É o que o `mcp-hello` usa: ao rodar `python server.py`, o terminal parece "travado" — na verdade o server está *esperando* um client falar com ele pelo stdin. Rápido, simples, sem rede no meio.
- **HTTP** — para servers **remotos**, acessados pela rede. Use quando o server roda em outro lugar: um serviço na nuvem, uma ferramenta compartilhada pelo time inteiro.

> Regra prática: **está na sua máquina → stdio**; **está na rede/nuvem → HTTP**.

## Limites honestos

- **Você quase sempre escreve o server, não o client.** O client vem pronto no app de IA. Seu trabalho é expor a *sua* ferramenta como um server bem descrito.
- **Server roda código e acessa seus dados.** Conectar um server é dar uma chave à IA. Confie na origem, entenda o que ele expõe e prefira começar por tools de **leitura** antes de liberar ações que alteram coisas.
- **Versões precisam bater.** O `protocolVersion` do handshake existe justamente para isso. O MCP é um **padrão em evolução** — as datas de versão mudam, e client e server precisam falar versões compatíveis para se entenderem.

## Exercício

1. No exemplo [`examples/mcp-hello`](../examples/mcp-hello): quem é o **client** e quem é o **server**? Onde vive cada um? (Dica: você rodou `python server.py` — isso é qual dos dois?)
2. Imagine **um único client** (seu app de IA) usando **dois servers ao mesmo tempo**. Dê um exemplo de dois servers que fariam sentido juntos numa mesma tarefa, e diga qual tool cada um contribuiria.
3. Escolha o transporte (**stdio** ou **HTTP**) para cada caso e justifique: (a) um server que lê arquivos do **seu notebook**; (b) um server que o time inteiro acessa, rodando **num servidor na nuvem**.

---

<div align="center">

[« 21 - O que é MCP](21-o-que-e-mcp.md) — [Índice](../README.md#roadmap) — [23 - Criando seu primeiro MCP »](23-criando-seu-primeiro-mcp.md)

</div>
