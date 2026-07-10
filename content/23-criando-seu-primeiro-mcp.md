# 23 - Criando seu primeiro MCP

No [capítulo 22](22-mcp-client-e-mcp-server.md) você viu o MCP por fora: um **server** expõe ferramentas, um **client** as consome, e no meio deles trafega o protocolo. Agora vamos construir um server de verdade — e você vai descobrir que é bem menos trabalho do que parece. Este capítulo caminha pelo exemplo **[`examples/mcp-hello`](../examples/mcp-hello)**, que já está pronto no repositório para você rodar e modificar.

O truque: você **não escreve o protocolo**. Escreve funções Python normais e deixa um SDK cuidar do resto.

## Instalando o SDK

Existem SDKs oficiais de MCP para várias linguagens. Aqui usamos o de **Python**, pela leitura mais fácil. Dentro dele vem o **FastMCP**, um atalho que transforma funções comuns em ferramentas MCP.

```bash
# de dentro da pasta examples/mcp-hello
pip install mcp
```

> Dica: crie um ambiente virtual antes (`python -m venv .venv` e depois `source .venv/bin/activate`), para não misturar com o Python global do seu sistema.

## Caminhando pelo `server.py`

O arquivo inteiro tem menos de 40 linhas de código. Vamos por partes.

**1. Criar o server.** Você importa o `FastMCP` e cria uma instância com um nome. Esse nome é como o client vai identificar o seu conjunto de ferramentas:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ia4noobs-hello")
```

**2. Registrar uma tool.** Aqui está o coração de tudo. Você escreve uma função Python e coloca o decorator `@mcp.tool()` em cima. Só isso já transforma a função numa ferramenta que o modelo pode chamar:

```python
@mcp.tool()
def somar(a: int, b: int) -> int:
    """Soma dois numeros inteiros e retorna o resultado.

    Use quando o usuario pedir para somar, adicionar ou calcular o total
    de dois numeros.
    """
    return a + b
```

Três detalhes desta função valem ouro, porque **o SDK os lê e monta a descrição da tool a partir deles**:

- **O nome da tool vem do nome da função**: `somar`.
- **As anotações de tipo viram o *schema*.** O `a: int, b: int` diz ao modelo que esta tool recebe dois parâmetros inteiros; o `-> int` diz que devolve um inteiro. É assim que o modelo sabe *o que enviar* sem adivinhar.
- **A docstring é a descrição que o modelo lê.** Aquele texto entre aspas triplas não é comentário decorativo: é *exatamente* o que o modelo consulta para decidir **quando** chamar a ferramenta. Repare que ela não só diz o que a função faz, mas *em que situação usá-la* ("Use quando o usuario pedir para somar..."). Isso reduz muito a chance de o modelo chamar a tool errada.

A segunda ferramenta do exemplo segue o mesmo molde, agora com texto:

```python
@mcp.tool()
def saudacao(nome: str) -> str:
    """Gera uma mensagem de boas-vindas personalizada para um nome.

    Use quando o usuario quiser cumprimentar ou saudar alguem pelo nome.
    """
    return f"Ola, {nome}! Bem-vindo(a) ao mundo do MCP."
```

**3. Rodar o server.** No fim do arquivo, o bloco padrão do Python só executa quando você roda o arquivo diretamente:

```python
if __name__ == "__main__":
    mcp.run()
```

O `mcp.run()` inicia o server usando o transporte padrão: **stdio** (entrada e saída padrão do processo). O server passa a "conversar" com o client por esse canal.

## Rodando

Com o SDK instalado, é um comando:

```bash
python server.py
```

E aqui vem o **primeiro susto de todo iniciante**: o terminal parece *travar*. Nenhuma mensagem, cursor parado. **Está tudo certo.** Um server MCP stdio não tem "tela": ele está esperando um client se conectar e mandar mensagens pela entrada padrão. Como você o rodou na mão, não há ninguém do outro lado — ele fica escutando o silêncio. Aperte `Ctrl+C` para sair. Rodar sozinho só serve para confirmar que o arquivo não tem erro de sintaxe.

## Conectando a um host

Para a tool ganhar vida, um **host/client** de IA precisa iniciar o seu server. A maioria dos hosts (apps de chat, IDEs com IA) tem um arquivo de configuração onde você aponta o comando que sobe o server. O formato costuma ser assim (o caminho e o nome variam conforme o host — trecho **ilustrativo**):

```json
{
  "mcpServers": {
    "ia4noobs-hello": {
      "command": "python",
      "args": ["server.py"]
    }
  }
}
```

Depois de recarregar o host, ele sobe o seu server, pergunta "quais tools você tem?" e recebe de volta `somar` e `saudacao` com suas descrições. Aí é só pedir em linguagem natural — *"some 7 e 5"* ou *"me dê boas-vindas, meu nome é Ana"* — e o modelo decide chamar a ferramenta certa.

> Muitos SDKs trazem também um **inspector**: uma ferramenta que conecta no seu server e lista/testa as tools sem precisar de um host completo. É a forma mais rápida de depurar enquanto desenvolve.

## Por dentro

Por que ficou tão simples? Porque o FastMCP **esconde o JSON-RPC** — aquele protocolo de mensagens que você viu no [capítulo 22](22-mcp-client-e-mcp-server.md).

Quando o host pergunta quais ferramentas existem, quem responde com a lista, os nomes, os tipos de parâmetro e as descrições é o SDK — lendo as suas funções por baixo dos panos. Quando o modelo decide chamar `somar` com `a=7` e `b=5`, chega uma mensagem JSON-RPC pelo stdio; o SDK a interpreta, converte os argumentos para os tipos certos, chama a sua função `somar(7, 5)`, pega o `12` que ela devolve e o embrulha de volta numa resposta JSON-RPC. Você **nunca** monta nem lê essas mensagens à mão.

Em outras palavras: aquelas anotações de tipo e a docstring que parecem "só boa prática" de Python são, na prática, **a interface que o modelo enxerga**. O SDK é o tradutor entre o seu código Python e o protocolo. É por isso que o `server.py` inteiro cabe numa tela.

## Gotchas honestos

- **"Travou" ao rodar sozinho.** Já explicado: é o comportamento normal do stdio esperando um client. Não é bug.
- **Docstring ruim = tool chamada na hora errada.** Se a descrição for vaga ("faz uma conta"), o modelo pode não chamar quando deveria — ou chamar quando não deveria. Uma boa descrição diz *o que faz* **e** *quando usar*. Isso conecta direto com o que vimos em [o que é uma tool](17-o-que-e-uma-tool.md).
- **Cuidado com tools poderosas.** Seu server roda **código de verdade**. Uma tool que apaga arquivos, roda comandos do sistema ou faz pagamentos é útil — e perigosa. Comece pelo mínimo, valide as entradas e dê a cada tool só o acesso que ela precisa. Segurança em IA tem capítulo próprio: [capítulo 26](26-seguranca-em-ia.md).

## Exercício

1. Abra `examples/mcp-hello`, instale o SDK e rode `python server.py`. Confirme que ele "trava" esperando um client (e entenda por quê). Saia com `Ctrl+C`.
2. **Adicione uma terceira tool** ao `server.py`. Sugestão: `inverter_texto(texto: str) -> str` que devolve o texto de trás para frente (dica em Python: `texto[::-1]`). Escreva uma docstring que diga **o que faz e quando usar**.
3. Reescreva a docstring da sua nova tool de propósito de forma **vaga** e depois de forma **clara**. Qual das duas você chamaria, se fosse o modelo? Esse é o exercício mental que separa uma tool útil de uma inútil.
4. Conecte o `mcp-hello` a um host de IA da sua escolha e peça algo que faça o modelo chamar cada uma das tools.
5. Pense numa tool **útil para o seu contexto** (consultar o clima, buscar um pedido, ler uma planilha). Escreva só a assinatura e a docstring — sem implementar. Ela é segura de expor? Que acesso ela precisaria?

---

<div align="center">

[« 22 - MCP Client e MCP Server](22-mcp-client-e-mcp-server.md) — [Índice](../README.md#roadmap) — [24 - Rodando modelos localmente »](24-rodando-modelos-localmente.md)

</div>
