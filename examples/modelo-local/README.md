# Rodando um modelo de IA localmente (com Ollama)

Até agora, os outros exemplos com API mandavam sua pergunta para os servidores
de uma empresa (a OpenAI), o que **custa dinheiro** e exige uma **chave**. Aqui
é diferente: o modelo de IA roda **na sua própria máquina**, de **graça** e
**sem chave de API**.

Fazemos isso com o **Ollama**, um programa que baixa e executa modelos de IA
localmente. O script `local.py` conversa com ele usando só a biblioteca padrão
do Python — **nada** para instalar via `pip`.

> Este exemplo acompanha o capítulo [24 - Rodando modelos localmente](../../content/24-rodando-modelos-localmente.md)
> e se conecta com os capítulos [26 - Segurança em IA](../../content/26-seguranca-em-ia.md) e
> [28 - Custos e Escalabilidade](../../content/28-custos-e-escalabilidade.md).

---

## O que é o Ollama?

O [Ollama](https://ollama.com) é uma ferramenta gratuita que deixa você **baixar
e rodar modelos de IA (LLMs) no seu computador**, com um comando só. Ele sobe um
pequeno servidor local (em `http://localhost:11434`) que outros programas — como
o nosso script — podem chamar.

### Vantagens de rodar local

- **Privacidade**: seus dados **não saem da sua máquina**. Nada é enviado para a
  nuvem de ninguém. Ótimo para informações sensíveis.
- **Custo zero**: depois de baixar o modelo, você pode usar quanto quiser sem
  pagar por token.
- **Funciona offline**: sem internet? Sem problema, o modelo já está no seu disco.

### Limitações (seja realista)

- Modelos que rodam num PC comum são **menores e menos capazes** que os gigantes
  de API (GPT, Claude, Gemini). Erram mais e "sabem" menos.
- Consomem **memória e processamento** da sua máquina; podem ser **lentos** sem
  uma placa de vídeo boa.

Ou seja: local é excelente para aprender, prototipar e para casos que exigem
privacidade — mas nem sempre substitui os modelos de API para tarefas difíceis.

---

## Pré-requisitos

- **Python 3.6 ou superior** (só a biblioteca padrão — nada de `pip install`)
- **Ollama** instalado e um modelo baixado (passos abaixo)

---

## Passo a passo

**1. Instale o Ollama:**

Baixe em [ollama.com](https://ollama.com) e instale (tem versão para Windows,
macOS e Linux).

**2. Baixe um modelo pequeno:**

```bash
ollama pull llama3.2
```

Isso baixa o modelo `llama3.2` (alguns GB). Só precisa fazer uma vez.

**3. Garanta que o servidor do Ollama está rodando:**

Na maioria das instalações ele já inicia sozinho. Se precisar, rode num
terminal:

```bash
ollama serve
```

**4. Rode o script:**

```bash
python local.py
```

Se o Ollama não estiver rodando ou o modelo não tiver sido baixado, o script
mostra uma mensagem clara explicando o que fazer (em vez de um erro assustador).

---

## Experimente

- Troque o `PROMPT` no topo do `local.py` e rode de novo.
- Baixe outro modelo (ex: `ollama pull mistral`), mude a variável `MODELO` no
  script e compare as respostas.
- Note que, ao rodar, **nenhuma** informação sai do seu computador — o mesmo
  código funcionaria até sem internet.
