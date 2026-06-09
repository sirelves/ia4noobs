# 19 - MCP Client e MCP Server

No capítulo anterior vimos *para que serve* o MCP. Agora vamos entender **como ele funciona por dentro**: os dois lados da conversa (client e server) e o que exatamente um server oferece.

## Os dois lados: client e server

O MCP segue um modelo **cliente-servidor**. São dois papéis:

- **MCP Client (cliente)**: vive **dentro de um host de IA** — um aplicativo que você usa, como um app de chat, uma IDE ou um assistente de código. O client é a parte que **fala o protocolo MCP** e se conecta aos servers.
- **MCP Server (servidor)**: é um programa separado que **expõe capacidades** (ferramentas, dados, prompts) para o client consumir.

Vale separar dois termos que aparecem juntos:

- **Host**: a aplicação de IA inteira (ex: o Claude Desktop, uma IDE). É quem fala com o modelo.
- **Client**: o componente, dentro do host, que mantém a conexão com **um** server. Um host pode ter vários clients, um para cada server conectado.

```
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

## O que um server expõe

Um server MCP pode oferecer **três tipos de capacidade**. É importante conhecer os três:

### 1. Tools (ferramentas)

São **ações que o modelo pode executar** — geralmente algo que muda estado ou roda um processo. O modelo decide quando chamá-las.

> Exemplo: uma tool `criar_issue` no GitHub, ou `executar_consulta_sql` em um banco.

### 2. Resources (recursos)

São **dados/arquivos para leitura**, que dão contexto ao modelo. Pense neles como "informação para o modelo ler", não como ações.

> Exemplo: o conteúdo de um arquivo `README.md`, uma linha de uma tabela, um documento.

### 3. Prompts

São **modelos de prompt reutilizáveis** — templates prontos que o usuário ou o host podem disparar para guiar a IA em uma tarefa comum.

> Exemplo: um prompt `revisar_pull_request` que já vem com instruções de como fazer uma boa revisão.

| Capacidade | O que é | Quem controla |
|------------|---------|---------------|
| **Tools** | Ações que o modelo executa | Geralmente o modelo |
| **Resources** | Dados para leitura/contexto | Geralmente a aplicação |
| **Prompts** | Templates reutilizáveis | Geralmente o usuário |

## Como client e server conversam

A comunicação acontece por **mensagens estruturadas** no formato **JSON-RPC 2.0**. Sem decorar nada: a ideia é que cada lado manda mensagens de **requisição** e recebe **respostas** em um formato padronizado.

Em alto nível, uma sessão é mais ou menos assim:

```
1. Client conecta no Server  ──►  "olá, quem é você?" (handshake)
2. Server responde            ──►  "sou o server de arquivos, versão X"
3. Client pergunta            ──►  "quais tools você tem?"
4. Server lista as tools      ──►  [ler_arquivo, escrever_arquivo, ...]
5. Modelo decide usar uma     ──►  Client chama:  ler_arquivo("notas.txt")
6. Server executa e responde  ──►  conteúdo do arquivo
```

O modelo nunca acessa a ferramenta diretamente: ele **pede** ao client, o client **chama** o server, o server **executa** e devolve o resultado. Esse intermediário é o que mantém tudo padronizado e controlável.

## Transportes: como as mensagens trafegam

As mensagens JSON-RPC precisam de um "canal" para viajar. Os dois transportes mais comuns são:

- **stdio** — para servers **locais**. O host inicia o server como um processo no seu computador e conversa com ele pela entrada/saída padrão (stdin/stdout). Rápido e simples; ótimo para ferramentas que rodam na sua máquina.
- **HTTP** (com **SSE** / *streamable HTTP*) — para servers **remotos**, acessados pela rede. Útil quando o server roda em outro lugar (um serviço na nuvem, por exemplo).

> Regra prática: **server local → stdio**; **server remoto → HTTP**.

## Exemplos de servers reais

Existem muitos servers MCP prontos pela comunidade. Alguns exemplos comuns, de forma neutra:

- **Sistema de arquivos**: ler e escrever arquivos em pastas que você autorizar.
- **GitHub**: ler issues, abrir pull requests, navegar em repositórios.
- **Banco de dados** (Postgres, SQLite): consultar tabelas e esquemas.
- **Web / navegador**: buscar páginas ou automatizar um navegador.
- **Ferramentas de produtividade**: agendas, notas, mensageria.

Você pode **instalar** servers existentes ou **criar o seu** — é o que vamos fazer no próximo capítulo.

## Um lembrete de segurança

Um server MCP **roda código** e pode **acessar seus dados**. Conectar um server é como dar uma chave à IA. Antes de conectar qualquer server:

- Confie na **origem** do server (de quem é? é código aberto e revisado?).
- Entenda **quais tools e dados** ele expõe.
- Prefira começar com servers de **leitura** antes de liberar ações que alteram coisas.

## Exercício

1. Desenhe (no papel ou em texto) o diagrama **host → client → server** com suas próprias palavras, etiquetando cada parte.
2. Para um server MCP de **GitHub**, dê um exemplo de cada capacidade: uma **tool**, um **resource** e um **prompt**.
3. Você quer conectar um server que roda **no seu próprio computador**. Qual transporte usaria — **stdio** ou **HTTP**? Justifique.

---

<div align="center">

[« 18 - O que é MCP](18-o-que-e-mcp.md) — [Índice](../README.md#roadmap) — [20 - Criando seu primeiro MCP »](20-criando-seu-primeiro-mcp.md)

</div>
