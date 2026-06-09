# Prompts: ruim vs bom

O mesmo pedido, escrito de um jeito melhor, gera respostas **muito** melhores. A IA não adivinha o que está na sua cabeça: quanto mais clara for a sua instrução, mais útil será a resposta.

Abaixo estão pares de exemplo. Em cada um você vê um **prompt ruim** (vago) e um **prompt bom** (claro). A ideia não é só ler — é **testar**! Copie cada par e cole numa ferramenta de IA como [ChatGPT](https://chat.openai.com), [Claude](https://claude.ai) ou [Gemini](https://gemini.google.com) e compare as duas respostas. A diferença salta aos olhos.

---

### Caso 1: Escrever um e-mail

```text
❌ Prompt ruim:
Escreve um email pro meu chefe pedindo folga.
```

```text
✅ Prompt bom:
Você é um assistente que escreve e-mails profissionais e cordiais em português do Brasil.

Contexto: sou desenvolvedor e preciso pedir folga ao meu gestor na sexta-feira (12/06) por motivo pessoal. Trabalho com ele há 2 anos e tenho boa relação.

Tarefa: escreva um e-mail curto solicitando essa folga, deixando claro que organizei minhas tarefas para que nada fique parado.

Formato: assunto + corpo de até 4 frases, tom educado e direto.
```

**Por que melhora:** o segundo prompt define o papel da IA, dá contexto (quem você é, a data, a relação), uma tarefa clara e o formato esperado. A IA não precisa chutar nada.

---

### Caso 2: Resumir um texto

```text
❌ Prompt ruim:
Resume isso aqui: [cola o texto]
```

```text
✅ Prompt bom:
Resuma o texto abaixo para alguém que tem só 30 segundos para ler.

Requisitos:
- No máximo 5 bullet points.
- Linguagem simples, sem jargão.
- Termine com 1 frase dizendo qual é a principal conclusão.

Texto:
[cole o texto aqui]
```

**Por que melhora:** definimos o público ("alguém com 30 segundos"), o tamanho (5 bullets), o estilo (sem jargão) e o que deve aparecer no fim. Em vez de um resumo genérico, você recebe exatamente o que precisa.

---

### Caso 3: Gerar código

```text
❌ Prompt ruim:
Faz uma função que valida email.
```

```text
✅ Prompt bom:
Você é um desenvolvedor JavaScript experiente.

Tarefa: escreva uma função chamada `validarEmail(email)` que retorna `true` ou `false`.

Restrições:
- JavaScript puro, sem bibliotecas externas.
- Aceite e-mails comuns (ex: nome@dominio.com.br) e rejeite os inválidos.
- Inclua 3 exemplos de uso com comentários.

Formato: um único bloco de código comentado em português.
```

**Por que melhora:** especificamos a linguagem, o nome e a assinatura da função, as restrições (sem bibliotecas) e pedimos exemplos. Você recebe código pronto para usar, e não um esboço que precisa adivinhar.

---

### Caso 4: Planejar estudos

```text
❌ Prompt ruim:
Me ajuda a estudar programação.
```

```text
✅ Prompt bom:
Você é um mentor de carreira em tecnologia.

Contexto: sou iniciante, tenho 1 hora por dia (de segunda a sexta) e quero aprender lógica de programação com Python em 4 semanas.

Tarefa: monte um plano de estudos semana a semana.

Formato: uma tabela com colunas "Semana", "Tema", "O que fazer na prática" e "Como saber se aprendi".
```

**Por que melhora:** a IA agora sabe seu nível, seu tempo disponível, a linguagem e o prazo. Com o formato em tabela, o plano vira algo que dá para seguir de verdade, no lugar de uma lista solta de conselhos.

---

### Caso 5: Traduzir

```text
❌ Prompt ruim:
Traduz isso pro inglês: "Bora marcar a call?"
```

```text
✅ Prompt bom:
Traduza a frase abaixo para o inglês usado em ambiente de trabalho (tom profissional, mas amigável).

Além da tradução, explique em 1 linha por que escolheu essas palavras, já que é uma expressão informal.

Frase: "Bora marcar a call?"
```

**Por que melhora:** indicamos o tom (profissional e amigável) e o contexto (trabalho), evitando uma tradução literal e estranha. Pedir a explicação ainda te ajuda a aprender o idioma.

---

### Caso 6: Criar um post para redes sociais

```text
❌ Prompt ruim:
Cria um post sobre meu curso de IA.
```

```text
✅ Prompt bom:
Você é um redator de marketing especializado em redes sociais.

Contexto: estou lançando um curso gratuito de "Introdução à IA para iniciantes", voltado para quem nunca programou. Quero divulgar no Instagram.

Tarefa: escreva 1 legenda para o post.

Formato:
- Comece com uma pergunta que prenda a atenção.
- Até 4 linhas de texto.
- Termine com uma chamada para ação (CTA) e 3 hashtags relevantes.
- Tom descontraído, sem promessas exageradas.
```

**Por que melhora:** definimos a plataforma, o público, a estrutura (gancho + texto + CTA + hashtags) e o tom. O resultado já sai no formato certo para publicar, em vez de um texto genérico.

---

## Checklist de um bom prompt

Antes de enviar, confira se seu prompt tem o máximo possível destes itens:

- **Papel** — diga à IA quem ela deve ser (ex: "Você é um professor de matemática").
- **Contexto** — explique a situação, quem você é e qualquer detalhe relevante.
- **Tarefa** — peça de forma clara o que você quer que seja feito.
- **Formato** — diga como quer a resposta (lista, tabela, parágrafo, código, tamanho).
- **Exemplos** — quando útil, mostre um exemplo do que você espera.
- **Restrições** — defina limites (ex: "sem jargão", "no máximo 100 palavras", "sem bibliotecas externas").

Você não precisa usar todos sempre. Mas quanto mais vago for o pedido, mais a IA vai chutar.

---

## Pratique

Pegue uma ferramenta de IA e tente melhorar estes prompts ruins usando o checklist acima:

1. **"Me dá uma receita."** → Reescreva incluindo o que você tem na geladeira, quanto tempo você tem para cozinhar e para quantas pessoas.
2. **"Explica o que é blockchain."** → Reescreva definindo para quem é a explicação (ex: uma criança de 10 anos) e o tamanho máximo.
3. **"Corrige meu texto."** → Reescreva dizendo o tipo de texto, o tom desejado e se você quer apenas a correção ou também uma explicação dos erros.

Compare a resposta do prompt ruim com a do seu prompt melhorado. Sentiu a diferença? Esse é o poder do **prompt engineering**.

---

Veja o capítulo [06 - O que é Prompt Engineering](../../content/06-o-que-e-prompt-engineering.md) para a teoria.
