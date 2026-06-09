"""
Servidor MCP "Hello World" — IA4Noobs

Este e um exemplo MINIMO de um servidor MCP (Model Context Protocol).
Um servidor MCP expoe "tools" (ferramentas) que um modelo de IA pode chamar
por meio de um CLIENT/host compativel com MCP (ex: um app ou IDE de IA).

Aqui usamos a biblioteca oficial `mcp` no estilo FastMCP, que deixa tudo
bem simples: voce so escreve funcoes Python normais e decora com @mcp.tool().
"""

# Importamos a classe FastMCP do SDK oficial de MCP em Python.
# Ela cuida de toda a "parte chata" do protocolo (mensagens, transporte, etc.)
# e nos deixa focar apenas na logica das nossas ferramentas.
from mcp.server.fastmcp import FastMCP

# Criamos a instancia do servidor.
# O texto "ia4noobs-hello" e o NOME do servidor: e como o client vai
# identificar este conjunto de ferramentas.
mcp = FastMCP("ia4noobs-hello")


# --- Ferramenta 1: somar -------------------------------------------------

# O decorator @mcp.tool() registra a funcao abaixo como uma "tool" do MCP.
# Pontos importantes:
#   1. As ANOTACOES DE TIPO (a: int, b: int) -> int viram o "schema" da tool,
#      ou seja, o modelo sabe quais parametros enviar e de que tipo.
#   2. A DOCSTRING (o texto entre aspas triplas) e a DESCRICAO da tool.
#      E EXATAMENTE ela que o modelo de IA LE para decidir QUANDO chamar a
#      ferramenta. Por isso ela deve ser clara e objetiva.
@mcp.tool()
def somar(a: int, b: int) -> int:
    """Soma dois numeros inteiros e retorna o resultado.

    Use quando o usuario pedir para somar, adicionar ou calcular o total
    de dois numeros.
    """
    return a + b


# --- Ferramenta 2: saudacao ----------------------------------------------

@mcp.tool()
def saudacao(nome: str) -> str:
    """Gera uma mensagem de boas-vindas personalizada para um nome.

    Use quando o usuario quiser cumprimentar ou saudar alguem pelo nome.
    """
    return f"Ola, {nome}! Bem-vindo(a) ao mundo do MCP."


# --- Inicializacao do servidor -------------------------------------------

# Este bloco so roda quando executamos o arquivo diretamente
# (ex: `python server.py`), e nao quando ele e importado por outro modulo.
if __name__ == "__main__":
    # mcp.run() inicia o servidor usando o transporte padrao: STDIO.
    # No transporte stdio, o servidor "conversa" com o client pela entrada e
    # saida padrao do processo. Por isso, ao rodar sozinho, ele parece
    # "travado": na verdade ele esta ESPERANDO um client MCP se conectar.
    mcp.run()
