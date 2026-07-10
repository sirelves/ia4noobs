# Zero-shot vs Few-shot

Este exemplo mostra, na prática, a diferença entre pedir algo para a IA **sem
exemplos** (zero-shot) e pedir a mesma coisa **dando alguns exemplos** primeiro
(few-shot). O script faz **duas chamadas** ao mesmo modelo, para a mesma tarefa
— classificar o sentimento de uma frase — e imprime os dois resultados para você
comparar.

> Este exemplo acompanha o capítulo [10 - Few-shot e Chain-of-Thought](../../content/10-few-shot-e-chain-of-thought.md).

---

## Os conceitos em poucas linhas

- **Zero-shot**: você só descreve a tarefa. Ex: *"classifique o sentimento desta
  frase"*. O modelo se vira com o que já sabe. Funciona bem em tarefas comuns,
  mas o **formato** da resposta é imprevisível.
- **Few-shot**: antes da pergunta de verdade, você dá **alguns exemplos** de
  entrada → saída (os "shots"). O modelo aprende pelo exemplo tanto **o que
  fazer** quanto **em que formato responder**. Ótimo quando você precisa de uma
  saída padronizada.
- **Chain-of-thought** (raciocínio passo a passo): uma técnica parecida em que
  você pede para o modelo **pensar em etapas** antes de responder (ex: *"explique
  seu raciocínio passo a passo"*). Ajuda em problemas de lógica e contas. Este
  exemplo foca em few-shot, mas a ideia é a mesma: **guiar** o modelo.

---

## Pré-requisitos

- **Python 3.8 ou superior**
- Uma **chave de API** da OpenAI

> Se você ainda não tem uma chave nem sabe configurar, siga primeiro o exemplo
> [`chamar-api`](../chamar-api/) — ele explica esse passo a passo em detalhe.
> Lembre: chamar a API custa alguns **centavos** por uso.

---

## Como instalar e rodar

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY="sua-chave-aqui"
python few_shot.py
```

> No Windows, ative o ambiente com `.venv\Scripts\activate` e defina a chave com
> `$env:OPENAI_API_KEY="sua-chave-aqui"` (PowerShell).

Se a chave não estiver configurada, o script avisa de forma amigável.

---

## Experimente (é aqui que se aprende!)

- Troque a `FRASE` no topo do script por outra e rode de novo.
- **Edite os exemplos** do few-shot (a lista de pares `user` → `assistant`).
  Tente tirar um exemplo, ou trocar as categorias por outras (ex: `URGENTE`,
  `NORMAL`, `SPAM`). Veja como a saída muda.
- Compare: a resposta do **zero-shot** costuma vir mais "solta" (às vezes uma
  frase inteira), enquanto a do **few-shot** sai curta e no formato que os
  exemplos ensinaram. Essa é a mágica de dar exemplos.
