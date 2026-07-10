# 13 - O que são Embeddings

Até agora você viu como conversar com uma IA. Agora vamos entender uma peça que está por trás de muita coisa — busca semântica, recomendação e o RAG do próximo capítulo: os **embeddings**.

A ideia é simples de sentir, mesmo que o nome assuste. Bora?

## A ideia central

Computador não entende texto. Ele entende número.

Um **embedding** é o jeito de transformar um texto (uma palavra, uma frase ou um documento inteiro) em uma **lista de números** que representa o **significado** daquele texto.

Essa lista de números a gente chama de **vetor**.

```text
"gato"  ->  [0.81, 0.20, -0.05, 0.77, ...]
"frase" ->  [0.12, -0.66, 0.40, 0.09, ...]
```

Não precisa entender cada número. O importante é a ideia:

> Textos com significados **parecidos** viram listas de números **parecidas**.

## A analogia do mapa

Pense em um mapa de cidades.

Cada cidade tem uma coordenada (latitude e longitude). Cidades que ficam **perto** no mapa estão **próximas** de verdade. Cidades distantes estão longe.

Embeddings fazem o mesmo, mas com **significados** em vez de lugares:

- Coisas parecidas ficam **perto**.
- Coisas diferentes ficam **longe**.

Veja um mapa imaginário de palavras (usando só 2 coordenadas pra facilitar):

```text
        ^  (eixo "animais")
        |
  felino ● gato ● gatinho
        |        ● cachorro
        |
--------+-----------------------> (eixo "veículos")
        |        ● carro
        |   caminhão ●  ônibus ●
        |
```

Repare: `gato`, `gatinho` e `felino` ficam **agrupados**. `caminhão`, `carro` e `ônibus` formam **outro grupo**, bem longe dos bichos.

O modelo não foi "ensinado" manualmente a isso. Ele aprendeu lendo muito texto — já já a gente vê como.

## Medindo o "perto": similaridade de cosseno

"Perto no mapa" é bonito de falar, mas o computador precisa de um **número**. O jeito mais usado de medir isso se chama **similaridade de cosseno** (*cosine similarity*).

A intuição, sem fórmula pesada: pense em cada vetor como uma **seta** saindo da origem do mapa. A similaridade de cosseno olha o **ângulo** entre duas setas.

- Setas apontando para a **mesma direção** (ângulo pequeno) → muito parecido → valor perto de **1**.
- Setas em direções **sem relação** (ângulo aberto) → pouco a ver → valor perto de **0**.

É isso que "estar perto no mapa" significa numericamente: mesma direção. O valor vai de -1 a 1, mas na prática, com textos, você quase sempre lida com valores positivos — e quanto **maior**, mais parecido.

### Os números de verdade

Chega de "alto" e "baixo". Aqui estão similaridades **reais**, calculadas com um modelo de embedding pequeno (o `potion-base-8M`). São números de verdade — guarde só uma ressalva que explico logo abaixo:

| Par de textos | Similaridade | Leitura |
|---|---|---|
| `gato` ↔ `gatinho` | **0.60** | quase sinônimos → bem alto |
| `gato` ↔ `felino` | **0.20** | mesma família, palavra mais técnica |
| `gato` ↔ `cachorro` | **0.14** | ambos animais, espécies diferentes |
| `gato` ↔ `caminhão` | **0.05** | nada a ver → bem baixo |

Repare na **ordem**, que é o ouro aqui: sinônimo (0.60) > mesma categoria (0.14–0.20) > sem relação (0.05). O modelo colocou `gatinho` colado em `gato`, deixou `cachorro` no mesmo bairro (ambos são animais) e mandou `caminhão` pro outro lado da cidade. Ninguém programou isso à mão.

Funciona até quando as **palavras são diferentes**. Compare estas duas buscas:

| Par de frases | Similaridade |
|---|---|
| "Como troco minha senha?" ↔ "Onde altero minha credencial de acesso?" | **0.40** |
| "Como troco minha senha?" ↔ "Qual a previsão do tempo?" | **0.32** |

A primeira dupla quase não tem palavra em comum ("senha" vs "credencial de acesso"), mas diz a **mesma coisa** — e ficou mais perto (0.40) do que a frase totalmente fora do assunto (0.32). É exatamente isso que faz uma busca por significado funcionar.

**A ressalva honesta:** esses números vêm de um modelo **pequeno e estático**. Por isso a diferença entre 0.40 e 0.32 é modesta — dá pra distinguir, mas está apertado. Modelos maiores (os de produção da OpenAI, Cohere, Google) **abrem muito mais** essa distância: a paráfrase iria pra perto de 0.8 e a frase sem relação despencaria. A **ideia** é idêntica; a nitidez é que melhora com o modelo.

## Isso em código

Na prática você não calcula nada à mão. Um **modelo de embedding** devolve o vetor, e você compara com cosseno. Repare que o modelo de embedding é **diferente** do modelo de chat: o de chat conversa; o de embedding só faz uma coisa — texto entra, vetor sai.

```python
import numpy as np

# 1) Um "modelo de embedding" transforma texto em vetor.
#    (aqui é ilustrativo; na vida real você chama uma lib ou uma API)
vetor_gato     = modelo_embedding("gato")      # ex: [0.81, 0.20, -0.05, ...]
vetor_gatinho  = modelo_embedding("gatinho")
vetor_caminhao = modelo_embedding("caminhão")

# 2) Similaridade de cosseno: o "cosseno do ângulo" entre dois vetores.
def cosseno(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# 3) Quanto maior, mais parecido.
print(cosseno(vetor_gato, vetor_gatinho))   # ~0.60  (perto)
print(cosseno(vetor_gato, vetor_caminhao))  # ~0.05  (longe)
```

A função `cosseno` é o coração de quase toda busca semântica que existe — inclusive a do RAG.

## E as dimensões?

No nosso mapa de papel usamos **2** coordenadas (animal, veículo) porque dá pra desenhar. Embeddings de verdade têm **centenas ou milhares** de coordenadas — o `potion-base-8M` usa 256; modelos grandes usam 1.536, 3.072 ou mais.

Impossível desenhar isso num papel. Mas não precisa: a matemática do cosseno funciona igual com 2 ou com 3.072 dimensões. Cada dimensão captura um "aspecto" do significado que o modelo achou útil, e a soma delas é o que aproxima ou afasta os vetores. **Mais dimensões = mais nuance**, mesma ideia.

## Por dentro: como o modelo aprende os vetores

De onde saem esses números, se ninguém rotula "gato = 0.81"? Da **companhia das palavras**. Existe uma frase famosa em linguística que resume tudo:

> "Você conhece uma palavra pela companhia que ela mantém." — J.R. Firth

Isso se chama **hipótese distribucional**. Durante o treino, o modelo lê bilhões de frases e repara **em que contexto** cada palavra costuma aparecer. `gato` aparece perto de "miou", "ração", "ronronou", "dono". `cachorro` aparece perto de "latiu", "ração", "passeio", "dono" — contextos que se sobrepõem bastante. `caminhão` aparece perto de "estrada", "carga", "motorista" — outro mundo.

O modelo então ajusta os vetores para que **palavras que vivem em contextos parecidos fiquem com vetores parecidos**. Sinônimos e temas próximos vão sendo puxados pra perto; assuntos distantes vão sendo empurrados pra longe — tudo por estatística de coocorrência, **sem rótulo humano** dizendo o que é o quê. É por isso que `gato` e `gatinho` deram 0.60: eles aparecem quase nos mesmos lugares.

## Pra que isso serve?

Embeddings destravam coisas muito úteis:

- **Busca semântica**: em vez de casar a palavra exata, você acha o que **quer dizer** o mesmo. "carro quebrado" traz "veículo com defeito".
- **Recomendação**: itens parecidos ficam perto. "Quem gostou disso também gostou daquilo."
- **Agrupamento (clustering)**: juntar automaticamente textos parecidos — tipo separar tickets de suporte por assunto.
- **Base do RAG**: achar os trechos de documento relevantes pra pergunta do usuário. É o alicerce do próximo capítulo — veja o [capítulo 14](14-o-que-e-rag.md).

Quer ver o cosseno rodando de verdade? O exemplo [`examples/rag-mini`](../examples/rag-mini) gera embeddings e calcula similaridade na prática.

## Seja honesto: os limites

- Embeddings capturam **padrões de uso da linguagem**, não a verdade. Eles não "sabem" o que é certo ou errado.
- A qualidade depende do modelo e dos dados de treino. Idiomas e assuntos pouco representados saem piores — modelo pequeno separa menos, como você viu nos números.
- Eles carregam **vieses** dos textos de treino.
- Comparar significados não é **entender** de verdade. É estatística bem feita, não consciência.

## Exercício

1. **No papel:** pense em 6 palavras — três de um grupo (ex: comidas) e três de outro (ex: esportes). Desenhe um mapa 2D e posicione as 6. Escreva por que `pizza` e `lasanha` ficam perto, e por que `pizza` e `futebol` ficam longe.
2. **Ordem de similaridade:** olhando a tabela do capítulo, ordene do mais parecido ao menos parecido: (`gato`↔`cachorro`), (`gato`↔`gatinho`), (`gato`↔`caminhão`). Confere com sua intuição? Por que `cachorro` fica no meio?
3. **Na prática:** abra o exemplo [`examples/rag-mini`](../examples/rag-mini), rode com suas próprias frases e veja os valores de cosseno saindo. Crie uma paráfrase (mesma ideia, outras palavras) e uma frase fora do tema, e confirme que a paráfrase fica mais perto.

---

<div align="center">

[« 12 - Principais erros ao usar IA](12-principais-erros-ao-usar-ia.md) — [Índice](../README.md#roadmap) — [14 - O que é RAG »](14-o-que-e-rag.md)

</div>
