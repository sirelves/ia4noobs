# 20 - Criando seu primeiro MCP

Hora de colocar a mão na massa. Vamos criar um **server MCP mínimo** que expõe **uma tool simples**. A ideia aqui é entender o *fluxo* — depois você adapta para coisas mais úteis.

Nosso objetivo: um server com uma tool que **soma dois números** (e, de bônus, uma que devolve **a hora atual**). Simples de propósito, para você focar na estrutura.

## O que você vai precisar

Você não precisa implementar o protocolo JSON-RPC na mão. Existem **SDKs oficiais** que cuidam de toda a parte chata (handshake, mensagens, transporte). Os principais são:

- **Python** — pacote `mcp` (inclui o utilitário **FastMCP**, que deixa tudo bem direto).
- **TypeScript / JavaScript** — SDK oficial para Node.

Aqui usaremos **Python**, por ser mais fácil de ler para quem está começando.

```bash
# Crie uma pasta para o projeto e instale o SDK
pip install "mcp[cli]"
```

> Dica: use um ambiente virtual (`python -m venv .venv` e `source .venv/bin/activate`) para não bagunçar seu Python global.

## A estrutura básica de um server

Todo server MCP segue mais ou menos os mesmos passos:

1. **Criar o server** (dar um nome a ele).
2. **Registrar uma ou mais tools** — cada tool tem **nome**, **descrição** e **parâmetros**.
3. **Rodar o server** (escolhendo o transporte, normalmente `stdio` para local).

A **descrição** e os **nomes dos parâmetros** importam muito: é por eles que o modelo entende *quando* e *como* usar a tool. Escreva descrições claras!

## Exemplo de código (Python)

```python
# servidor.py
from mcp.server.fastmcp import FastMCP
from datetime import datetime

# 1. Cria o server e dá um nome a ele
mcp = FastMCP("meu-primeiro-server")


# 2. Registra uma tool.
# O decorador @mcp.tool() transforma a função numa ferramenta MCP.
# - O NOME da tool vem do nome da função: "somar"
# - A DESCRIÇÃO vem da docstring (o texto entre aspas triplas)
# - Os PARÂMETROS vêm dos argumentos da função (a, b) e seus tipos
@mcp.tool()
def somar(a: int, b: int) -> int:
    """Soma dois números inteiros e devolve o resultado."""
    return a + b


# Uma segunda tool, sem parâmetros: devolve a hora atual
@mcp.tool()
def hora_atual() -> str:
    """Retorna a data e hora atuais no formato ISO."""
    return datetime.now().isoformat()


# 3. Roda o server usando o transporte stdio (server local)
if __name__ == "__main__":
    mcp.run(transport="stdio")
```

Repare como o SDK faz o trabalho pesado: você só descreve **o que** sua tool faz. O nome, a descrição e os tipos dos parâmetros viram automaticamente as informações que o modelo recebe para decidir usar a ferramenta.

## Como testar

Um server sozinho não faz nada — ele precisa de um **client / host de IA** conectado. Em alto nível, o teste é assim:

1. **Configure o host** para conhecer seu server. Muitos hosts (apps de chat, IDEs) têm um arquivo de configuração onde você aponta o comando que inicia o server, por exemplo:

```json
{
  "mcpServers": {
    "meu-primeiro-server": {
      "command": "python",
      "args": ["servidor.py"]
    }
  }
}
```

2. **Reinicie/recarregue o host.** Ele vai iniciar seu server e perguntar quais tools existem.
3. **Peça algo em linguagem natural**, como *"some 7 e 5"* ou *"que horas são?"*. Se tudo estiver certo, o modelo vai chamar a sua tool e usar o resultado na resposta.

> Muitos SDKs também trazem um **inspector** (ferramenta de inspeção) que conecta no seu server e lista/testa as tools sem precisar de um host completo. É ótimo para depurar enquanto desenvolve.

## Lembre-se da segurança

Seu server **roda código de verdade**. Por isso, alguns cuidados desde o primeiro projeto:

- **Não exponha ações perigosas sem necessidade.** Uma tool que apaga arquivos, roda comandos do sistema ou faz pagamentos é poderosa — e arriscada. Comece pelo mínimo.
- **Valide as entradas.** Não confie cegamente nos parâmetros que chegam.
- **Princípio do menor privilégio.** Dê à tool só o acesso que ela realmente precisa (uma pasta específica, somente leitura, etc.).
- **Cuidado ao instalar servers de terceiros.** Vimos no capítulo anterior: confie na origem antes de conectar.

## Próximo passo: o exemplo do repositório

Para praticar com um projeto que já roda, veja o exemplo **`examples/mcp-hello`** deste repositório. Ele traz um server MCP mínimo pronto para você **rodar, conectar e modificar**. Sugestão: depois de rodá-lo, adicione **sua própria tool** e teste.

## Exercício

1. Reproduza o `servidor.py` acima na sua máquina e rode-o (mesmo que só com o inspector). Confirme que as tools `somar` e `hora_atual` aparecem.
2. **Crie uma terceira tool** sua — por exemplo, `saudar(nome: str)` que devolve `"Olá, {nome}!"`. Escreva uma **descrição clara** na docstring.
3. Pense em uma tool **útil mas potencialmente perigosa** (ex: apagar arquivos). Liste **2 cuidados de segurança** que você adotaria antes de expô-la num server MCP.
4. Abra o exemplo `examples/mcp-hello`, rode-o e conecte-o a um host de IA da sua escolha.

---

<div align="center">

[« 19 - MCP Client e MCP Server](19-mcp-client-e-mcp-server.md) — [Índice](../README.md#roadmap) — [21 - Como criar aplicações com IA »](21-como-criar-aplicacoes-com-ia.md)

</div>
