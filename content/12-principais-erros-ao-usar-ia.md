# 12 - Principais erros ao usar IA

Você já sabe pedir bem e estruturar respostas. Agora vamos falar do outro lado: os tropeços. Quase todo erro comum com IA nasce de **esquecer o que ela é de verdade** — um preditor de próximo token ([cap. 05](05-o-que-sao-tokens.md)), não um sistema que sabe, calcula ou lembra. Quando você entende o mecanismo, os erros deixam de ser surpresa e viram coisas que dá pra prever e evitar.

Pra cada erro abaixo eu te dou o **porquê** (ligado ao mecanismo dos capítulos anteriores) e o **como evitar**.

## Erro 1: Confiar nos fatos cegamente

A IA responde com a mesma confiança quando acerta e quando inventa. E o que ela inventa costuma soar perfeito: datas redondas, nomes plausíveis, citações bem formatadas.

- **Por que acontece:** o modelo não consulta uma verdade e depois escreve. Ele gera o texto **mais provável** dado o seu pedido ([cap. 04](04-como-o-chatgpt-funciona.md)). "Plausível" e "verdadeiro" quase sempre coincidem — mas quando não coincidem, ele não tem como perceber. Uma referência inventada tem exatamente o mesmo "cheiro" estatístico de uma real. Isso é a **alucinação**.
- **Como evitar:** trate cada fato específico (número, data, citação, lei, link) como suspeito até confirmar em fonte confiável. Peça que ela **marque o que tem certeza e o que você deve checar**. Para respostas ancoradas em documentos reais, o caminho é **RAG** ([cap. 14](14-o-que-e-rag.md)), que dá à IA o texto-fonte junto com a pergunta.

## Erro 2: Prompt vago

"Me ajuda com meu negócio" e "me dá um resumo disso" jogam quase todo o trabalho para o modelo — e ele preenche as lacunas com o palpite mais genérico possível.

- **Por que acontece:** sem detalhes, o texto mais provável é o mais **médio**. O modelo não sabe seu contexto; ele completa com o que aparece com mais frequência para pedidos parecidos. Vago na entrada, genérico na saída.
- **Como evitar:** dê contexto, objetivo, restrições e formato. Detalhe é o que empurra a resposta para o seu caso específico ([cap. 09](09-como-fazer-perguntas-melhores.md)).

```text
Vago:      me ajuda com meu negócio

Melhor:    Tenho uma loja de roupas pequena no Instagram e quero
           aumentar vendas no fim de semana. Me dê 3 ideias de
           promoção simples e baratas, em lista, com o passo a passo.
```

## Erro 3: Esperar conta ou matemática exata

Peça `4327 × 89` e é bem capaz de vir um número errado — com toda a confiança do mundo.

- **Por que acontece:** números **também viram tokens** ([cap. 05](05-o-que-sao-tokens.md)), e de um jeito bagunçado (`4327` pode virar `43` + `27`). O modelo não executa a conta: ele **prevê os tokens** de um resultado que *pareça* certo. Para números pequenos que apareceram muito no treino, acerta; para contas longas, chuta.
- **Como evitar:** peça o **passo a passo** (Chain of Thought, [cap. 10](10-few-shot-e-chain-of-thought.md)) — quebrar em etapas curtas melhora bastante. Melhor ainda: dê a ele uma **calculadora de verdade** via *tool* ([cap. 17](17-o-que-e-uma-tool.md)), aí a conta sai de um programa, não de um chute.

## Erro 4: Enfiar contexto demais

Colar o manual inteiro, três PDFs e o histórico completo "pra ela ter tudo" costuma **piorar** a resposta, não melhorar.

- **Por que acontece:** a janela de contexto é finita ([cap. 06](06-o-que-e-janela-de-contexto.md)). Encher além da conta estoura o limite ou desperdiça espaço — e existe o efeito **"lost in the middle"**: o modelo presta mais atenção no começo e no fim do que você mandou, e informação enterrada no meio de um bloco gigante muitas vezes é ignorada.
- **Como evitar:** mande **só o trecho relevante**. Menos contexto bem escolhido vence muito contexto jogado. (Também sai mais barato — você paga por token.)

## Erro 5: Achar que ele "lembra" de tudo

"Mas eu já te falei meu nome lá em cima" — e ele repete errado. Ou você abre um chat novo esperando que continue de onde parou.

- **Por que acontece:** o modelo não tem memória mágica. O que ele "sabe" da conversa é **o que está dentro da janela de contexto agora** ([cap. 06](06-o-que-e-janela-de-contexto.md)). Numa conversa longa, o começo pode sair da janela; num chat novo, nada do anterior está lá. Sem a informação na janela, ela simplesmente não existe para o modelo.
- **Como evitar:** em conversas longas, **relembre ou resuma** o que for essencial de tempos em tempos. Não assuma que ele guardou. (Recursos de "memória" de alguns produtos são um sistema por fora que **reinjeta** dados na janela — não é o modelo lembrando sozinho.)

## Erro 6: Antropomorfizar

Achar que ele "quer" te ajudar, "acredita" no que diz, "entende" seu problema ou tem uma opinião sincera.

- **Por que acontece:** ele foi treinado em texto humano, então soa humano. Mas por baixo é o mesmo mecanismo: prever o próximo token. Quando responde "eu acho que...", não há um "eu" com crença — é a continuação mais provável. Por isso ele **concorda fácil demais** se você empurrar, e "muda de opinião" sem convicção nenhuma: não havia opinião para começar.
- **Como evitar:** leia a saída como **texto gerado**, não como testemunho de alguém. Isso te deixa saudavelmente cético — principalmente quando ele afirma algo com firmeza.

## Erro 7: Usar IA onde código determinístico é melhor

Somar uma coluna de planilha, validar um CPF, ordenar mil nomes, conferir se um e-mail tem formato válido: dá pra pedir à IA, mas é a ferramenta errada.

- **Por que acontece:** essas tarefas têm **uma** resposta certa e uma regra exata. IA trabalha por probabilidade, então introduz chance de erro onde não deveria existir nenhuma — e ainda custa mais e é mais lenta que três linhas de código.
- **Como evitar:** regra de bolso — **IA para o ambíguo, código para o exato.** Redigir, resumir, classificar por sentido, sugerir ideias: IA. Contas, validações, regras fixas, dados estruturados: código (às vezes exposto à IA como *tool*, [cap. 17](17-o-que-e-uma-tool.md)).

## Por dentro: a raiz comum

Releia os sete erros e você vai notar que quase todos são a **mesma falha de modelo mental** vista de ângulos diferentes:

> A IA é um **preditor de texto plausível**. Ela não tem acesso direto à verdade, não faz contas, e não tem memória fora da janela de contexto.

- Confiar nos fatos, antropomorfizar → esquecer que **plausível ≠ verdadeiro**.
- Contas erradas, usar IA no lugar de código → esquecer que ela **prevê, não calcula**.
- Achar que lembra, enfiar contexto demais → esquecer como a **janela** funciona.
- Prompt vago → esquecer que, sem sinal seu, ela cai no **mais provável genérico**.

Guardando essa frase, você antecipa o erro antes de cometer.

## Um exemplo (ilustrativo)

Para você ver a alucinação acontecendo. **A troca abaixo é ilustrativa** — escrita para demonstrar o padrão, não copiada de uma execução real:

```text
Você:  Cite o artigo da LGPD que trata de "portabilidade de senha".
IA:    Claro! O Art. 23-B da LGPD (Lei 13.709/2018) garante ao titular
       a portabilidade de senha entre controladores, conforme o §2º...
```

Soa impecável: número de artigo, número da lei, parágrafo. Mas "portabilidade de senha" não é um tema da LGPD, e esse artigo, nesses termos, **não existe** — o modelo montou algo que *tem cara* de resposta jurídica. É exatamente o Erro 1: ninguém sinalizou incerteza. A única defesa é abrir o texto da lei e conferir.

## Limites honestos

Não existe usar IA "sem nunca errar" — nem para quem tem experiência. Alucinação e erro de conta não são bugs que somem numa atualização; são consequência de como a tecnologia funciona. O que muda com a prática não é parar de errar, é ter **processo**: verificar o que importa, dar o contexto e as *tools* certas, e **avaliar a resposta com método** em vez de aceitar de primeira ([cap. 27](27-como-avaliar-respostas-de-ia.md)). A defesa é o processo, não a fé na ferramenta.

## Exercício

1. **Provoque uma alucinação de propósito.** Peça uma citação, referência, artigo de lei ou dado bem específico sobre um assunto de nicho. Depois tente **confirmar em fonte oficial**. Existia? Anote o quão convincente estava a versão inventada.
2. **IA ou código?** Pegue três tarefas suas de verdade (ex.: "resumir e-mails", "somar despesas do mês", "validar CPFs de um cadastro") e classifique cada uma. Justifique em uma frase por que é ambígua (IA) ou exata (código).
3. **Reescreva um prompt vago.** Pegue um pedido genérico que você já fez e reescreva com contexto, objetivo, restrição e formato. Rode os dois e compare as respostas.

---

<div align="center">

[« 11 - Como estruturar respostas](11-como-estruturar-respostas.md) — [Índice](../README.md#roadmap) — [13 - O que são Embeddings »](13-o-que-sao-embeddings.md)

</div>
