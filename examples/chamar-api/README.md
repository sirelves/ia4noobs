# Chamar uma API de IA (a primeira chamada)

Este é o exemplo **mais básico** de todos: fazer **uma** chamada a um modelo de
IA (um LLM) pela API oficial da OpenAI e imprimir a resposta no terminal.

Até aqui você provavelmente usou IA por um site (ChatGPT, Claude, Gemini). Usar
a **API** é diferente: em vez de digitar num chat, é o seu **código** que
conversa com o modelo. É assim que se constrói qualquer aplicação com IA.

> Este exemplo acompanha os capítulos [05 - O que são Tokens](../../content/05-o-que-sao-tokens.md)
> e [28 - Custos e Escalabilidade](../../content/28-custos-e-escalabilidade.md).

---

## Atenção: chamar a API pode ter custo

Diferente do ChatGPT gratuito, a API é um serviço **pago por uso**. Cada chamada
custa alguns **centavos** (às vezes frações de centavo, com o modelo barato deste
exemplo). Você paga por **tokens** — os pedacinhos de texto que entram e saem do
modelo. Rodar este exemplo umas vezes custa quase nada, mas é bom saber disso
desde o começo. Contas novas costumam ganhar um crédito inicial de teste.

---

## Pré-requisitos

- **Python 3.8 ou superior**
- Uma **chave de API** da OpenAI (veja abaixo como pegar)

### Como pegar uma chave de API

1. Crie uma conta em [platform.openai.com](https://platform.openai.com).
2. Acesse [platform.openai.com/api-keys](https://platform.openai.com/api-keys).
3. Clique em **"Create new secret key"** e **copie** a chave (ela começa com `sk-`).
4. Guarde num lugar seguro — a OpenAI só mostra a chave **uma vez**.

> A chave é como uma senha: quem tiver ela pode gastar da sua conta. **Nunca**
> compartilhe nem suba ela para o GitHub.

---

## Como instalar e rodar

**1. Crie um ambiente virtual e instale a dependência:**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> No Windows, ative o ambiente com `.venv\Scripts\activate` no lugar de
> `source .venv/bin/activate`.

**2. Defina a sua chave numa variável de ambiente:**

No Linux/macOS (terminal bash/zsh):

```bash
export OPENAI_API_KEY="sua-chave-aqui"
```

No Windows (PowerShell):

```powershell
$env:OPENAI_API_KEY="sua-chave-aqui"
```

> Essa variável vale só para a janela de terminal atual. Se abrir outro
> terminal, precisa definir de novo. Veja o arquivo [`.env.example`](.env.example)
> como referência do nome esperado.

**3. Rode o script:**

```bash
python chamar.py
```

Se a chave não estiver configurada, o script avisa de forma amigável e explica
o que fazer — sem quebrar com um erro assustador.

---

## O que observar

- A resposta impressa é gerada pelo modelo `gpt-4o-mini`, que é barato e rápido.
- No final do arquivo `chamar.py` há um trecho **comentado** que mostra o **uso
  de tokens** (quantos tokens sua pergunta e a resposta consumiram). Descomente
  para ver — é exatamente o que a OpenAI usa para te cobrar. Isso conecta direto
  com os capítulos de **Tokens** e de **Custos**.

## Experimente

- Troque a pergunta (o texto do `"role": "user"`) e rode de novo.
- Mude a instrução do `"system"` (ex: peça respostas em forma de lista) e veja
  como o comportamento do modelo muda.
