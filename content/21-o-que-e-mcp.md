# 21 - O que é MCP

No [capítulo 17](17-o-que-e-uma-tool.md) vimos que uma IA ganha superpoderes quando recebe **tools**: buscar na web, ler um arquivo, consultar um banco. Só que dar uma tool a um modelo tem um custo escondido de encanamento. Cada tool precisa ser descrita, chamada, autenticada e ter os erros tratados — e cada aplicação de IA fazia isso do seu próprio jeito. O **MCP** existe para acabar com essa bagunça.

## A dor: N × M integrações sob medida

Imagine que você tem **N** aplicações de IA (um chat, uma IDE, um assistente de suporte) e **M** ferramentas ou fontes de dados (Google Drive, GitHub, Postgres, Slack, sua API interna).

Sem um padrão, cada aplicação precisa de uma integração **sob medida** para cada ferramenta:

```text
                 ANTES (sem padrão)

  App de Chat ─────┬── código próprio ── Google Drive
                   ├── código próprio ── GitHub
                   └── código próprio ── Postgres

  IDE / Editor ────┬── código próprio ── Google Drive
                   ├── código próprio ── GitHub
                   └── código próprio ── Postgres
```

São **N × M** integrações para escrever e manter. Com 3 apps e 5 ferramentas, já são **15** pedaços de código diferentes — cada um com seu jeito de autenticar, de montar a chamada e de tratar erro. Agora sinta a dor de verdade: sai uma versão nova da API do GitHub e você tem que caçar e corrigir **todo** app que fala com ele. Um dev cria uma ferramenta nova e precisa reimplementá-la em cada aplicação. É trabalho que se multiplica sozinho — e ninguém reaproveita o do vizinho.

## A saída: um padrão único (N + M)

O **MCP (Model Context Protocol)** é um **protocolo aberto** que define uma forma **padronizada** de conectar aplicações de IA a ferramentas e dados externos.

Com um padrão no meio, o problema vira **N + M**: cada app aprende a falar "MCP" **uma vez**, cada ferramenta expõe "MCP" **uma vez**, e tudo se conecta.

```text
                 DEPOIS (com MCP)

  App de Chat ──┐                    ┌── Server MCP do Google Drive
                ├──►  protocolo  ◄───┤
  IDE / Editor ─┤       MCP          ├── Server MCP do GitHub
                │                    │
  Assistente ───┘                    └── Server MCP do Postgres
```

A analogia que pegou é a do **USB-C**. Antes, cada aparelho tinha um conector: um cabo pro celular, outro pra câmera, outro pro notebook. O USB-C trouxe **um encaixe só** que serve pra tudo. O MCP é o **USB-C das ferramentas de IA**: em vez de um adaptador sob medida por ferramenta, um padrão único, e qualquer IA pluga em qualquer serviço compatível. Foi a Anthropic (empresa do Claude) que publicou o protocolo de forma **aberta** — e é justamente por ser aberto que a comunidade começou a criar servers para tudo quanto é ferramenta.

## As peças: Client e Server falando JSON-RPC

O MCP tem duas pontas, e a estrutura cabe numa frase:

- **Client (Cliente)**: mora **dentro** do app de IA (o Claude Desktop, o Cursor, sua aplicação). É quem pergunta e quem pede.
- **Server (Servidor)**: um programinha separado que **expõe** tools e dados — o "adaptador" de uma ferramenta específica.

Os dois conversam num formato de mensagem chamado **JSON-RPC 2.0** — basicamente "chamar uma função remota mandando um JSON". Nada exótico: um pede, o outro responde, e um campo `id` casa cada resposta com o pedido certo. Vamos destrinchar essas duas pontas no [capítulo 22](22-mcp-client-e-mcp-server.md); aqui o importante é ver que **são mensagens de verdade**, não abstração.

Quando o app se conecta, o Client se apresenta ao Server (o "handshake"):

```json
{ "jsonrpc": "2.0", "id": 1, "method": "initialize",
  "params": { "protocolVersion": "2024-11-05",
              "clientInfo": { "name": "meu-app", "version": "1.0" } } }
```

Feito isso, o Client faz a pergunta que muda tudo — "quais ferramentas você tem?":

```json
{ "jsonrpc": "2.0", "id": 2, "method": "tools/list" }
```

E o Server responde com a **vitrine** de tools que oferece:

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

Repare que o Server não só lista o nome da tool: ele **descreve** o que ela faz e **qual formato de entrada** ela espera (`inputSchema`). É esse autoanúncio que faz a mágica funcionar.

Além de `tools` (ações que a IA executa), o protocolo também define **resources** (dados prontos pra ler, tipo um arquivo ou registro) e **prompts** (modelos de prompt reutilizáveis). Neste guia o foco são as tools, mas vale saber que os três existem.

## Por dentro: o Server se descreve, então qualquer Client entende

Aqui está o pulo do gato do MCP, e é uma ideia só. Naquela resposta do `tools/list`, o Server entregou uma **descrição em formato padrão**: nome, texto explicativo e o esquema de entrada de cada tool. Como o formato é sempre o mesmo, **qualquer Client MCP consegue ler a vitrine de qualquer Server MCP** — sem ninguém ter escrito código de cola específico para aquele par.

Pensa no que isso compra. O Client não precisa saber de antemão que existe uma tool chamada `buscar_documento`. Ele **pergunta** (`tools/list`), **recebe** a descrição e já sabe como chamar. Executar é só mandar outra mensagem, no mesmo padrão:

```json
{ "jsonrpc": "2.0", "id": 3, "method": "tools/call",
  "params": { "name": "buscar_documento",
              "arguments": { "titulo": "política de troca" } } }
```

E a resposta volta pronta pro modelo usar:

```json
{ "jsonrpc": "2.0", "id": 3,
  "result": { "content": [ { "type": "text",
              "text": "Trocas em até 30 dias com nota fiscal." } ] } }
```

É por isso que o padrão derruba o N × M. A "cola" deixou de ser código escrito à mão para cada combinação e virou uma **conversa padronizada** que todo mundo fala. Você escreve um Server uma vez e ele funciona em **todo** app que fale MCP. Instala o Server do GitHub uma vez e ele serve pro seu chat, pra sua IDE e pro próximo app que ainda nem existe. Essa é a "tomada universal" na prática — a descrição padrão é a tomada.

Detalhe de bastidor: Client e Server se falam por um **transporte**. Ou **stdio** (o Server roda como um processo local na sua máquina) ou **HTTP** (o Server está na rede). A conversa JSON-RPC é a mesma nos dois casos.

## Limites honestos

Duas verdades para você guardar:

**É um padrão novo, em evolução.** As mensagens acima são reais na estrutura, mas o protocolo ainda amadurece: campos, versões e recursos mudam entre releases (por isso existe o `protocolVersion` no handshake). O ecossistema cresce rápido, e nem todo server é bem-feito ou mantido.

**Instalar um Server MCP dá poder a ele.** Um Server pode ler seus arquivos, acessar suas APIs, mexer nos seus dados — é literalmente pra isso que ele serve. Instalar um server desconhecido é como instalar qualquer programa de origem duvidosa: você está entregando acesso real. Conecte só o que você confia e entende. Vamos tratar disso a fundo no [capítulo 26](26-seguranca-em-ia.md).

Quer ver um Server MCP de verdade, pequeno e completo? Dá uma olhada no exemplo [`examples/mcp-hello`](../examples/mcp-hello). E o passo a passo de construir o seu está no [capítulo 23](23-criando-seu-primeiro-mcp.md) — depois de entender Client e Server no [capítulo 22](22-mcp-client-e-mcp-server.md).

## Exercício

1. Explique com **suas próprias palavras** por que um padrão como o MCP transforma **N × M** integrações em **N + M**. Onde exatamente o trabalho deixou de se multiplicar?
2. Liste **3 ferramentas ou fontes de dados** do seu dia a dia (seu Google Drive, um repositório no GitHub, uma planilha, a API da sua empresa) que você gostaria de expor via MCP. Para cada uma, escreva **uma tool** que ela ofereceria: o `name`, uma `description` de uma linha e qual seria o argumento de entrada.
3. Olhando a resposta do `tools/list`, explique por que o campo `inputSchema` é o que permite que **qualquer** Client chame a tool sem código sob medida.

---

<div align="center">

[« 20 - Multi-Agent Systems](20-multi-agent-systems.md) — [Índice](../README.md#roadmap) — [22 - MCP Client e MCP Server »](22-mcp-client-e-mcp-server.md)

</div>
