# 11 - Como estruturar respostas

Até agora você aprendeu a fazer perguntas melhores. Mas tem outra parte que você controla quase por completo: **o formato da resposta**. E aqui a coisa fica séria — não é só estética. É o que transforma a IA de "um chat que cospe texto" em uma peça que **um programa consegue usar**.

Pense na diferença: se a IA responde `"A Joana tem 27 anos e é de Recife."`, um humano lê e entende. Mas um programa não sabe recortar "27" de dentro daquele texto sem gambiarra. Agora, se ela responde `{"nome": "Joana", "idade": 27, "cidade": "Recife"}`, qualquer código pega o campo `idade` direto. **Estrutura é o que torna a saída legível por máquina** — e é por isso que este capítulo importa tanto para quem quer construir algo com IA.

## Formatos para humano lerem: markdown

Quando a resposta é para **você** ler, o objetivo é organização. E o formato mais natural é o **markdown** — títulos, listas, tabelas, negrito. A IA fala markdown fluentemente porque foi treinada em toneladas dele.

Peça **listas** para itens soltos:

```text
Liste 5 dicas para economizar energia em casa.
Bullets curtos, no máximo uma linha cada.
```

Peça **tabelas** para comparar lado a lado:

```text
Compare 3 planos de celular pré-pago numa tabela markdown
com as colunas: Plano | Preço mensal | Internet | Minutos.
```

Peça **passo a passo numerado** quando a ordem importa:

```text
Explique como trocar um pneu, em passos numerados,
para quem nunca fez isso.
```

E amarre o **tamanho** para não levar um textão:

```text
Resuma este artigo em no máximo 50 palavras.
[cole o texto]
```

Isso resolve 90% do uso no dia a dia. A outra parte — a que abre a porta para programar com IA — é pedir um formato que a máquina lê.

## O formato que máquinas leem: JSON

**JSON** (*JavaScript Object Notation*) é o jeito padrão de trocar dados estruturados entre programas na internet. Ele é só pares de `"chave": valor` entre chaves `{}`. A graça: é **rígido e previsível**, então um programa sempre sabe onde cada informação está.

Veja um pedido pensado para código — repare em três exigências que fazem diferença:

```text
Analise o texto abaixo e responda APENAS em JSON válido,
sem nenhum texto fora do JSON, com exatamente estes campos:
- "titulo": string curta
- "resumo": string de até 20 palavras
- "tags": lista de 1 a 3 palavras-chave

Se não houver título claro, use null em "titulo".

Texto:
"O Corinthians venceu por 2 a 1 num jogo cheio de polêmicas de arbitragem."
```

Uma resposta possível (exemplo **ilustrativo** — não é uma saída real capturada):

```json
{
  "titulo": "Corinthians vence com polêmica",
  "resumo": "Vitória por 2 a 1 marcada por decisões de arbitragem contestadas.",
  "tags": ["futebol", "arbitragem", "Corinthians"]
}
```

E é aqui que a mágica acontece: esse JSON **entra no seu código**. Em Python, você o transforma num dicionário e usa os campos como qualquer outro dado:

```python
import json

# resposta é a string que a IA devolveu
dados = json.loads(resposta)

print(dados["titulo"])       # "Corinthians vence com polêmica"
print(dados["tags"][0])      # "futebol"

for tag in dados["tags"]:
    salvar_no_banco(tag)     # agora é só usar
```

Sacou o pulo do gato? A IA deixou de ser um chat e virou uma **função** que recebe texto bagunçado e devolve dados limpos. É esse padrão que está por trás de aplicações reais de IA — voltaremos a ele no [capítulo 25](25-como-criar-aplicacoes-com-ia.md).

## Como pedir estrutura e ela realmente vir

Pedir JSON e receber JSON de verdade não é garantido — mas algumas técnicas aumentam MUITO a taxa de acerto:

- **Delimitadores claros.** Separe o texto de entrada das instruções com marcadores como `"""` ou crases triplas. Assim o modelo não confunde "o que analisar" com "o que fazer".
- **Diga o que fazer com campo vazio.** "Se não houver X, use `null`." Sem isso, o modelo inventa ou deixa buracos.
- **"Sem texto fora do JSON".** Modelos adoram enfeitar com `"Claro! Aqui está:"` antes do JSON. Isso quebra o `json.loads`. Peça explicitamente para não fazer.
- **Dê um exemplo do formato.** Essa é a mais poderosa: mostre 1 ou 2 exemplos de entrada→saída no próprio prompt. É o *few-shot* que você viu no [capítulo 10](10-few-shot-e-chain-of-thought.md), só que aplicado ao **formato** em vez do conteúdo. O modelo copia o molde.

```text
Extraia nome e idade. Exemplos:

"Pedro, 40 anos" → {"nome": "Pedro", "idade": 40}
"a Ana tem 15"   → {"nome": "Ana", "idade": 15}

Agora faça: "o João, que já fez 33"
```

## O jeito à prova de bala: JSON mode / saída estruturada

Tudo acima é "pedir com jeitinho". Mas várias APIs (OpenAI, Anthropic, Google e outras) oferecem um recurso que **força** a saída a ser um JSON válido: chama-se **structured output** ou **JSON mode**. Você passa um *schema* (a lista de campos e tipos que espera) e a API garante que a resposta vai respeitar aquele formato — chaves fechadas, aspas certas, tipos corretos.

A intuição de por que isso funciona está na próxima seção.

## Por dentro: decodificação restrita (constrained decoding)

Lembra do [capítulo 5](05-o-que-sao-tokens.md)? O modelo gera **um token por vez**, sempre escolhendo entre ~100 mil opções por probabilidade. Normalmente, todas as opções estão liberadas — por isso ele pode "escorregar" e escrever texto solto no lugar do JSON.

O **JSON mode** muda uma coisa só, mas decisiva: a cada passo, ele **filtra a lista de tokens permitidos** para deixar só os que mantêm o JSON válido. É a **decodificação restrita** (*constrained decoding*).

```text
Estado atual gerado:  {"idade":
                              │
                              ▼
   Tokens que o modelo QUERIA propor:   ["27", " vinte", "muitos", "!", ...]
                              │
                              ▼
   Filtro do schema (idade tem que ser número):
        "27"      → PERMITIDO   ✅
        " vinte"  → BLOQUEADO   ❌ (não é número)
        "muitos"  → BLOQUEADO   ❌
        "!"       → BLOQUEADO   ❌
                              │
                              ▼
   Só sobra token válido → o JSON NUNCA pode quebrar a sintaxe
```

*(Diagrama ilustrativo do mecanismo — os tokens exatos variam por implementação.)*

Ou seja: não é que o modelo "ficou mais esperto". É que a API **poda** as opções impossíveis antes de ele escolher. Por construção, é impossível sair um `{` sem o `}`, ou uma vírgula sobrando. Essa é a diferença entre *pedir* formato e *garantir* formato.

## Limites honestos

Estrutura ajuda demais, mas não é bala de prata:

- **Sem JSON mode, o modelo QUEBRA o formato às vezes.** Um campo a mais, aspas trocadas, um "Aqui está:" antes do JSON. Regra de ouro em produção: **sempre valide no código** (tente o `json.loads`, cheque se os campos existem) e tenha um **retry** — se falhou, peça de novo. Nunca confie de primeira.
- **Formato rígido demais pode piorar o conteúdo.** Se você prende o modelo num molde apertado, às vezes ele sacrifica a qualidade da resposta para caber no formato. Estrutura é ferramenta, não obrigação para tudo.
- **JSON gasta tokens extras.** Todas aquelas chaves, aspas e nomes de campo são tokens — e você paga por eles (revisão no [capítulo 5](05-o-que-sao-tokens.md)). Para uma resposta que só um humano vai ler, markdown simples sai mais barato.

## Recapitulando

- Você controla o formato — e isso vai de estética (markdown para humanos) até virar dado de máquina (JSON para programas).
- **JSON** com campos definidos deixa a saída pronta para o `json.loads` do seu código usar.
- Para a estrutura vir de verdade: use **delimitadores**, dê **exemplo do formato** (few-shot), diga "sem texto fora do JSON" e defina o que fazer com campo vazio.
- **JSON mode / saída estruturada** *força* um JSON válido via **decodificação restrita**: a API só deixa passar tokens que não quebram o formato.
- Mesmo assim, **valide sempre no código e tenha retry** — o modelo ainda escorrega.

## Exercício

1. Escreva um prompt que exija resposta **apenas em JSON** com exatamente 3 campos (ex.: `titulo`, `resumo`, `tags`) sobre uma notícia qualquer. Rode e veja se veio limpo.
2. **Quebre de propósito:** peça algo ambíguo, ou tire a instrução "sem texto fora do JSON", e observe o modelo escorregar (enfeitar, faltar campo, errar aspas). Isso mostra na prática por que validar no código é obrigatório.
3. Peça a **mesma informação** em dois formatos: uma **tabela markdown** e um **resumo em bullets**. Compare qual serve melhor para ler e qual serviria melhor para um programa consumir.

---

<div align="center">

[« 10 - Few-shot e Chain-of-Thought](10-few-shot-e-chain-of-thought.md) — [Índice](../README.md#roadmap) — [12 - Principais erros ao usar IA »](12-principais-erros-ao-usar-ia.md)

</div>
