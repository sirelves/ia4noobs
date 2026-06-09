# 05 - O que é Janela de Contexto

Agora que você sabe o que são tokens, dá para entender um dos conceitos mais importantes no uso de IA: a **janela de contexto**. Ela explica por que conversas longas começam a "dar branco" e por que às vezes a IA esquece o que você disse lá no começo.

## A definição

A **janela de contexto** é a quantidade máxima de tokens que o modelo consegue "enxergar" de uma vez. E atenção: ela conta **tudo junto**:

- o que **você** escreveu (a entrada),
- mais o que o modelo **vai responder** (a saída),
- mais, numa conversa, o **histórico** das mensagens anteriores.

Tudo isso precisa caber dentro do limite ao mesmo tempo.

## A analogia da mesa de trabalho

Pense na janela de contexto como uma **mesa de trabalho** (ou a memória de curto prazo da IA).

Você vai colocando papéis na mesa: sua pergunta, os documentos que colou, as respostas anteriores. A mesa é grande, mas **tem um tamanho fixo**. Enquanto cabe, o modelo consegue olhar tudo e responder considerando o conjunto.

O problema aparece quando a mesa enche.

## O que acontece quando a conversa fica longa demais

Quando você ultrapassa o limite, **algo precisa sair da mesa** para abrir espaço. E geralmente quem sai é o **começo** da conversa — as mensagens mais antigas.

Na prática, isso causa efeitos como:

- A IA "esquece" um detalhe que você deu lá no início.
- Ela se repete ou perde o fio da meada.
- Em alguns casos, o sistema corta (trunca) parte do texto automaticamente.

Não é má vontade nem preguiça: é simplesmente o conteúdo antigo saindo da janela para o novo caber.

## Por que os limites são diferentes

Cada modelo tem uma janela de tamanho diferente. Alguns aguentam alguns **milhares** de tokens; outros, mais modernos, chegam a **centenas de milhares** ou até **milhões** de tokens.

```text
Modelo A:  ~8 mil tokens     →  mesa pequena
Modelo B:  ~128 mil tokens   →  mesa grande
Modelo C:  ~1 milhão tokens  →  mesa enorme
```

Janelas maiores permitem analisar documentos grandes de uma vez, mas costumam custar mais caro e nem sempre são necessárias. (Os números acima são só ilustrativos; eles mudam o tempo todo conforme novas versões saem.)

## Impacto prático no seu uso

A janela de contexto aparece o tempo todo, mesmo que você não veja o nome:

- **Resumir um texto enorme**: se o texto não cabe na janela, você precisa quebrá-lo em partes.
- **Conversas longas**: depois de muitas mensagens, a IA pode perder o contexto inicial.
- **Colar documentos grandes**: um PDF gigante pode estourar o limite sozinho.

## Dicas para lidar com o limite

Você não precisa decorar números. Basta adotar bons hábitos:

- **Seja objetivo.** Mande só o que importa; corte enrolação e repetição.
- **Resuma o histórico.** Em conversas longas, peça à IA um resumo do que já foi combinado e siga a partir dele.
- **Recomece quando travar.** Se a conversa está confusa ou "esquecida", abra um chat novo e cole só o essencial.
- **Quebre tarefas grandes.** Documentos enormes podem ser processados em pedaços.

## Recapitulando

- Janela de contexto = quanto o modelo enxerga de uma vez, contando entrada **e** saída.
- É como uma mesa de tamanho fixo; quando enche, o conteúdo antigo sai.
- Modelos têm limites diferentes, de milhares a milhões de tokens.
- Para lidar: seja objetivo, resuma, recomece e divida tarefas grandes.

## E o próximo passo

Reparou que tudo gira em torno de **o que** e **como** você escreve para a IA? Quanto mais clara e objetiva for a sua mensagem, melhor o resultado — e menos você esbarra nos limites. Essa arte de escrever bons pedidos tem nome: **Prompt Engineering**. É exatamente o assunto do próximo módulo.

## Exercício

1. Explique, com a analogia da mesa de trabalho, o que acontece quando uma conversa fica longa demais.
2. A janela de contexto conta só a sua pergunta, ou também a resposta da IA e o histórico? Por que isso importa?
3. Você precisa resumir um documento que é maior que a janela de contexto do modelo. Descreva **uma** estratégia para conseguir fazer isso mesmo assim.

---

<div align="center">

[« 04 - O que são Tokens](04-o-que-sao-tokens.md) — [Índice](../README.md#roadmap) — [06 - O que é Prompt Engineering »](06-o-que-e-prompt-engineering.md)

</div>
