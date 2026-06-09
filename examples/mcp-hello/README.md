# Servidor MCP "Hello World"

Este e um exemplo **minimo** de um servidor MCP (Model Context Protocol) escrito em Python.
Ele expoe duas **tools** (ferramentas) bem simples que um modelo de IA pode chamar:

- `somar(a, b)` — soma dois numeros inteiros.
- `saudacao(nome)` — gera uma mensagem de boas-vindas personalizada.

O objetivo aqui nao e fazer algo "util de verdade", e sim mostrar a **estrutura**
de um servidor MCP: como criar o servidor, como declarar tools e como a IA descobre
quando usar cada uma (dica: e atraves da **docstring** de cada funcao).

> Este exemplo acompanha o capitulo [20 - Criando seu primeiro MCP](../../content/20-criando-seu-primeiro-mcp.md).

---

## Pre-requisitos

- **Python 3.10 ou superior**
- Saber instalar dependencias com `pip` (mostramos abaixo)

---

## Como instalar e rodar

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python server.py
```

> No Windows, ative o ambiente virtual com `.venv\Scripts\activate` no lugar de `source .venv/bin/activate`.

Ao rodar `python server.py`, o terminal vai parecer "parado". **Isso e normal!**
O servidor usa o transporte **stdio** e fica esperando um client MCP se conectar.
Para encerrar, pressione `Ctrl + C`.

---

## Como testar

Um servidor MCP **nao roda sozinho** — ele e usado por um **client/host de IA**
(por exemplo, um app de chat ou uma IDE compativel com MCP). O fluxo e:

1. O client (host de IA) inicia o servidor.
2. O modelo, durante a conversa, decide chamar uma tool com base na **descricao**
   (a docstring) de cada ferramenta.
3. O servidor executa a funcao Python e devolve o resultado para o modelo.

Na pratica, os clients MCP costumam ter um **arquivo de configuracao** onde voce
aponta o comando que inicia o servidor. De forma generica, voce indicaria algo como
"rode `python server.py` neste diretorio". Cada client tem seu proprio formato de
configuracao, entao consulte a documentacao do app/IDE que voce estiver usando.

Sozinho, o servidor apenas fica aguardando conexoes via stdio — sem um client,
nao ha com quem conversar.

---

## Nota de seguranca

Um servidor MCP **executa codigo** e pode **acessar dados** da sua maquina ou de
servicos externos. Por isso:

- **Exponha apenas as acoes realmente necessarias** — cada tool e uma porta aberta.
- **Confie apenas em servers que voce conhece** ou que voce mesmo escreveu.
- Pense bem antes de dar a uma tool acesso a arquivos, redes ou comandos do sistema.
