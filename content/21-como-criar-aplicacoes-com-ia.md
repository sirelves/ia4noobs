# 21 - Como criar aplicações com IA

Você já sabe conversar com modelos, escrever prompts e até montar um MCP. Agora vem a parte de "mundo real": transformar isso em uma **aplicação** que outras pessoas usam. E aqui as decisões mudam. Não é mais só "funciona no meu chat", é "funciona para 1000 usuários, sem vazar minha chave e sem estourar o orçamento".

## A arquitetura típica

Quase todo app com IA segue a mesma espinha dorsal:

```
[ Cliente ]        [ Seu Backend ]            [ API do LLM ]
 navegador  --->   recebe pedido       --->   modelo gera
 ou app            monta o prompt              a resposta
            <---   valida a resposta    <---
                   (opcional)
                   [ RAG / banco vetorial ]
                   [ Tools / agents ]
```

As peças:

- **Cliente (frontend)**: a tela. Web, mobile, CLI. Coleta o input do usuário e mostra o resultado.
- **Backend**: o cérebro da operação. Recebe o pedido do cliente, monta o prompt, chama o LLM, trata a resposta e devolve.
- **API do LLM**: o serviço externo (OpenAI, Anthropic, Google, ou um modelo seu). É só uma chamada HTTP.
- **RAG / banco vetorial** (opcional): quando o modelo precisa de conhecimento que ele não tem. Você busca trechos relevantes e injeta no prompt.
- **Tools / agents** (opcional): quando o modelo precisa **agir** — consultar um banco, chamar uma API, executar uma função.

## A regra de ouro: nunca chame o LLM direto do frontend

Parece tentador. Você tem a chave, tem o `fetch`, por que não chamar a API do modelo direto do navegador? **Não faça isso.** Três motivos:

1. **A chave de API vaza.** Tudo que está no frontend é público. Qualquer pessoa abre o DevTools, copia sua chave e passa a gastar no seu nome. Em horas você tem uma fatura absurda.
2. **Custo sem controle.** Sem um backend no meio, você não consegue limitar quem usa, quanto usa, nem barrar abuso.
3. **Sem validação.** Você não consegue checar, filtrar ou registrar o que entra e o que sai.

O padrão correto é sempre **cliente → seu backend → LLM**. O backend é o único que conhece a chave.

```js
// ERRADO — chave exposta no navegador
fetch("https://api.llm.com/v1/chat", {
  headers: { Authorization: `Bearer ${SUA_CHAVE}` }, // 🔥 vaza
});

// CERTO — frontend fala só com o SEU backend
fetch("/api/perguntar", {
  method: "POST",
  body: JSON.stringify({ pergunta }),
});
```

E a chave fica em **variável de ambiente** no servidor, nunca escrita no código nem commitada:

```js
const apiKey = process.env.LLM_API_KEY; // lido do ambiente
```

## Escolha do modelo: capaz vs barato vs rápido

Não existe "o melhor modelo". Existe o **certo para a tarefa**. Pense em três eixos:

| Eixo | Quando priorizar |
| --- | --- |
| **Capaz** (modelo grande) | Raciocínio complexo, código, análise difícil |
| **Barato** (modelo pequeno) | Tarefas simples e em alto volume (classificar, extrair) |
| **Rápido** (baixa latência) | Resposta em tempo real, chat ao vivo |

Dica prática: comece com um modelo capaz para validar a ideia. Depois, para cada tarefa repetitiva, teste se um modelo menor e mais barato dá conta. Muita coisa não precisa do modelo topo de linha.

## O prompt template mora no servidor

No app, o usuário **não** escreve o prompt inteiro. Ele dá só um pedaço (a pergunta, o texto, o dado). Seu backend tem um **template** que envolve esse input com instruções fixas:

```text
[ instruções do sistema — definidas por você, no servidor ]
Você é um assistente de suporte. Responda em português, de forma curta.
Se não souber, diga que não sabe.

[ contexto opcional — vindo do RAG ]
{trechos_relevantes}

[ input do usuário ]
{pergunta_do_usuario}
```

Manter o template no servidor te dá controle: você ajusta o comportamento sem mexer no cliente, e o usuário não consegue ver nem trocar suas instruções facilmente (mas cuidado — ele pode *tentar*; veremos isso no próximo capítulo).

## Tratar a resposta: o LLM não é confiável por padrão

A resposta do modelo é texto. Trate como dado externo não confiável:

- **Valide o formato.** Pediu JSON? Faça parse e cheque os campos. Se vier quebrado, tente de novo ou caia num fallback.
- **Lide com erros e timeout.** A API pode ficar lenta, retornar erro 429 (limite) ou cair. Sempre tenha timeout e mensagem de erro amigável.
- **Tente de novo com cuidado.** Para falhas temporárias, um retry com espera ajuda. Mas não fique em loop infinito gastando dinheiro.

```js
try {
  const resp = await chamarLLM(prompt, { timeout: 30000 });
  const dados = JSON.parse(resp);          // valida formato
  if (!dados.resposta) throw new Error("resposta vazia");
  return dados;
} catch (e) {
  return { erro: "Não consegui responder agora. Tente novamente." };
}
```

## Juntando tudo

Um app de IA bem feito é, na maior parte, **engenharia de software normal**: validação, tratamento de erro, segredos protegidos, custo controlado. A "mágica" do LLM é só uma chamada HTTP no meio do caminho. Quem trata bem as bordas (entrada, saída, falha, custo) entrega um produto sólido. Quem só cola a chamada da API entrega um protótipo frágil.

## Exercício

Desenhe, no papel ou num arquivo `.txt`, a arquitetura de um app de IA que você gostaria de construir (ex.: um resumidor de artigos). Marque:

1. O que é **cliente** e o que é **backend**.
2. Em que ponto a **chave de API** é usada (deve estar só no backend).
3. Se você precisa de **RAG** ou **tools** — e por quê.
4. Como você vai **validar a resposta** e o que mostra ao usuário em caso de erro.

---

<div align="center">

[« 20 - Criando seu primeiro MCP](20-criando-seu-primeiro-mcp.md) — [Índice](../README.md#roadmap) — [22 - Segurança em IA »](22-seguranca-em-ia.md)

</div>
