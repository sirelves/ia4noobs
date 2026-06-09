# 14 - O que é uma Tool

No capítulo anterior vimos que o que dá autonomia a um agent são as **tools**. Agora vamos entender direito o que elas são e como funcionam por dentro.

## O que é uma tool

Uma **tool** (ferramenta) é uma função ou capacidade que o agent pode **chamar** para fazer algo que o LLM sozinho não consegue.

Lembra que um LLM só gera texto? Ele não sabe que horas são agora, não acessa a internet, não lê seus arquivos e é ruim de conta. As tools resolvem isso. Exemplos típicos:

- **Buscar na web** — para informação atual.
- **Calcular** — para fazer contas com precisão.
- **Ler um arquivo** — para acessar dados que você tem no disco.
- **Chamar uma API** — previsão do tempo, cotação do dólar, enviar um e-mail.
- **Consultar um banco de dados** — buscar registros de um sistema.

Cada tool é, basicamente, um "superpoder" específico que você empresta ao agent.

## Como funciona o "tool calling"

O nome técnico é **tool calling** (ou **function calling**). O fluxo é assim:

```
1. Você dá ao modelo a LISTA de tools disponíveis (com descrição).
2. O modelo DECIDE chamar uma tool e diz quais argumentos usar.
3. O SISTEMA executa a tool de verdade (o código roda).
4. O resultado VOLTA para o modelo.
5. O modelo usa o resultado para continuar (ou responde de vez).
```

Um detalhe importante: **o modelo não executa a tool sozinho**. Ele só **decide** que quer chamá-la e com quais argumentos — é como preencher um pedido. Quem realmente roda o código é o sistema em volta do modelo (o seu programa). Depois, o resultado é devolvido ao modelo.

Visualizando:

```
   MODELO                SISTEMA              MUNDO
     │                     │                    │
     │  "quero chamar      │                    │
     │   buscar_web        │                    │
     │   ('preço bitcoin')"│                    │
     ├────────────────────►│                    │
     │                     │  executa de verdade│
     │                     ├───────────────────►│
     │                     │   "R$ 350.000"     │
     │                     │◄───────────────────┤
     │   resultado:        │                    │
     │   "R$ 350.000"      │                    │
     │◄────────────────────┤                    │
     │                     │                    │
     │  "O preço é         │                    │
     │   R$ 350.000."      │                    │
```

## Exemplo: definindo uma tool

Uma tool normalmente é descrita com três coisas: um **nome**, uma **descrição** (o que ela faz) e os **parâmetros** que ela aceita. Em JSON, fica mais ou menos assim:

```json
{
  "name": "buscar_clima",
  "description": "Retorna a previsão do tempo atual de uma cidade. Use quando o usuário perguntar sobre tempo, temperatura ou chuva.",
  "parameters": {
    "cidade": {
      "type": "string",
      "description": "Nome da cidade, ex: 'São Paulo'"
    }
  }
}
```

E o ciclo de chamada, em pseudo-código:

```python
# 1. O modelo, ao ver a pergunta "vai chover em Recife?",
#    decide chamar a tool e gera:
chamada = {
    "tool": "buscar_clima",
    "args": { "cidade": "Recife" }
}

# 2. O SISTEMA executa a função de verdade:
resultado = buscar_clima(cidade="Recife")   # -> "Nublado, 27°C, 60% chance de chuva"

# 3. O resultado volta para o modelo, que então responde ao usuário:
# "Em Recife está nublado, 27°C, com 60% de chance de chuva."
```

Repare que o modelo **escolheu** a tool e **preencheu** o argumento `cidade` sozinho, a partir da pergunta. Esse é o pulo do gato.

## Boas tools têm descrições claras

Aqui está a parte que muita gente erra: **o modelo escolhe a tool pela descrição**. Ele não vê o código por dentro — ele lê o nome e a descrição e decide qual usar.

Por isso, descrições boas são essenciais:

- **Ruim**: `"description": "busca dados"` — busca o quê? Quando usar?
- **Boa**: `"description": "Busca a cotação atual de uma moeda em reais. Use quando o usuário pedir preço de dólar, euro, bitcoin, etc."`

Quanto mais clara a descrição (o que faz, quando usar, o que retorna), mais o modelo acerta na hora de escolher. Trate a descrição como se você estivesse explicando para um colega quando usar aquela função.

Vale lembrar a honestidade do capítulo anterior: o modelo **pode escolher a tool errada** ou passar um argumento ruim. Descrições claras reduzem isso, mas não eliminam.

## Exercício

Pegue uma das tools que você listou no exercício do capítulo 13.

1. Escreva a definição dela em JSON, com `name`, `description` e `parameters`.
2. Capriche na `description`: deixe claro **o que** a tool faz e **quando** o agent deve usá-la.
3. Escreva, em pseudo-código, um exemplo de chamada: qual argumento o modelo passaria e qual resultado a tool devolveria.
4. Bônus: reescreva a descrição de propósito de forma vaga e pense — o modelo conseguiria saber quando usar?

---

<div align="center">

[« 13 - O que é um Agent](13-o-que-e-um-agent.md) — [Índice](../README.md#roadmap) — [15 - O que são Skills »](15-o-que-sao-skills.md)

</div>
