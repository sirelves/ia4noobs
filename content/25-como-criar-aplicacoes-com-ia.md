# 25 - Como criar aplicações com IA

Você já sabe conversar com modelos, escrever prompts e até montar um MCP. Agora vem a parte de "mundo real": transformar isso em uma **aplicação** que outras pessoas usam. E aqui a mentalidade muda. Não é mais "funciona no meu chat", é "funciona para 1000 usuários, sem vazar minha chave, sem estourar o orçamento e sem quebrar quando o modelo responde besteira".

A ideia central deste capítulo vai contra o hype: **a IA é UM componente do seu app, não o app inteiro.** O código determinístico (o que você já sabe programar) faz o que é exato — contas, validações, regras, salvar no banco. A IA faz o que é ambíguo — entender linguagem, resumir, classificar, gerar texto. Misturar os dois papéis é a fonte da maioria dos erros ([cap. 12](12-principais-erros-ao-usar-ia.md)).

## O fluxo básico: montar, chamar, tratar

Todo app com LLM, por baixo, faz o mesmo ciclo. Seu código **monta** uma entrada (prompt + contexto), **chama** a API do modelo, **recebe** a resposta e **trata** ela antes de usar:

```
   [ Usuário ]
       │  "quanto foi meu último pedido?"
       ▼
┌─────────────────────────────────────────────┐
│  SEU BACKEND  (código determinístico)        │
│                                              │
│  1. MONTA:  template de prompt               │
│             + contexto (RAG / banco)         │
│             + input do usuário               │
│                    │                         │
│                    ▼                         │
│  2. CHAMA ─────────────────►  [ API do LLM ] │
│                                    │ gera    │
│  3. RECEBE  ◄──────────────────────┘ texto   │
│                    │                         │
│                    ▼                         │
│  4. TRATA:  valida formato? erro? retry?     │
│             executa tool? loga?              │
└─────────────────────────────────────────────┘
       │  resposta pronta e verificada
       ▼
   [ Usuário ]
```

Repare: a "mágica" do modelo é o passo 2, uma simples chamada HTTP. Os passos 1, 3 e 4 são **engenharia de software normal** — e é neles que mora a diferença entre um protótipo frágil e um produto sólido.

### Regra de ouro: nunca chame o LLM direto do frontend

A chamada ao modelo mora no **backend**, sempre. Tudo que está no navegador é público: se sua chave de API estiver lá, qualquer um abre o DevTools, copia e gasta no seu nome — fatura absurda em horas. Além disso, sem um servidor no meio você não controla quem usa, não limita abuso e não valida nada. O padrão é **cliente → seu backend → LLM**, e a chave vive em variável de ambiente no servidor (`process.env.LLM_API_KEY`), nunca no código nem no commit.

## Os componentes de uma app séria

Um chat de brinquedo é só "montar, chamar, mostrar". Um app de verdade adiciona camadas conforme a necessidade. Você não precisa de todas — pegue só as que o seu problema pede.

- **Gestão de prompts** — não espalhe strings de prompt pelo código. Guarde **templates reutilizáveis** num lugar só, versionados, com espaços para preencher (o input do usuário, o contexto). Ajustar o comportamento vira editar um template, não caçar texto no meio da lógica. Base disso é o [cap. 08 - Prompt Engineering](08-o-que-e-prompt-engineering.md).
- **Contexto / RAG** — quando o modelo precisa de dados que ele não tem (seus documentos, seu FAQ, seu banco), você **busca os trechos relevantes e injeta no prompt**. É o [cap. 14 - RAG](14-o-que-e-rag.md). Sem isso, o modelo inventa (alucina) sobre o que não conhece.
- **Tools / function calling** — quando o modelo precisa **agir** (consultar um pedido, mandar e-mail, fazer uma conta), você dá a ele funções que seu código executa. O [cap. 17 - O que é uma tool](17-o-que-e-uma-tool.md) detalha. Lembre: quem executa a função é o seu código, não o modelo — ele só pede.
- **Saída estruturada** — se a resposta vai alimentar outro sistema (um banco, uma tela, outra API), você não quer texto solto. Peça **JSON com campos definidos** e faça o parse. É o [cap. 11 - Como estruturar respostas](11-como-estruturar-respostas.md).
- **Tratamento de erro** — a API vai falhar às vezes. Tenha **timeout** (não espere para sempre), **retry com backoff** (tentar de novo esperando um pouco mais a cada vez, para falhas temporárias como o erro 429 de limite) e um **fallback** para quando a resposta vier inválida.
- **Streaming** — mostrar a resposta saindo aos poucos, palavra por palavra, em vez de esperar o texto inteiro. Não deixa mais rápido, mas *parece*, e a experiência melhora muito num chat.
- **Cache** — se a mesma pergunta chega mil vezes, não pague mil chamadas. Guarde a resposta e reuse. Economiza dinheiro e latência.
- **Logs + avaliação** — registre entradas e saídas para conseguir depurar e **medir se a IA está respondendo bem** ao longo do tempo. Sem isso você está no escuro. Aprofundado no [cap. 27 - Como avaliar respostas](27-como-avaliar-respostas-de-ia.md).

## Por dentro: a arquitetura de referência mínima

Junte as peças e você tem o desenho mínimo de uma app confiável. O truque é enxergar **onde é IA (ambíguo) e onde é código (exato)**:

```
[ Cliente ]                    (só fala com o SEU backend)
    │ input do usuário
    ▼
[ Backend ]  ──── CÓDIGO DETERMINÍSTICO ────────────────
    │
    ├─► valida o input           (código: exato)
    ├─► checa CACHE ──── achou? ──► devolve, fim         ◄─ economia
    │
    ├─► busca contexto no RAG    (código: consulta banco)
    ├─► monta o prompt           (código: preenche template)
    │
    ├─► CHAMA O LLM ──────────────► [ API do modelo ]     ◄─ IA: ambíguo
    │      com timeout             (resume/classifica/gera)
    │      + retry/backoff
    │
    ├─► valida a resposta        (código: parse do JSON,
    │      inválida? → fallback         checa campos)
    │
    ├─► precisa agir? ──► executa TOOL  (código roda a função)
    │
    ├─► grava no CACHE + LOG     (código)
    ▼
[ Cliente ]  resposta verificada
```

Note a proporção: a IA é **uma caixa** no meio de muitas caixas de código. Boring technology em volta, IA no ponto exato onde ela é insubstituível. Quem trata bem as bordas (entrada, saída, falha, custo) entrega produto; quem só cola a chamada da API entrega demo.

## Exemplo trabalhado: assistente de FAQ (RAG + LLM)

Imagine um assistente que responde perguntas sobre a documentação da sua empresa. O fluxo:

1. **Uma vez, offline:** você quebra a documentação em pedaços e indexa num banco vetorial ([cap. 14](14-o-que-e-rag.md)).
2. **Chega a pergunta** "como cancelo minha assinatura?". O código **busca** os 3 trechos mais parecidos no banco (isso é código + busca, não é IA ainda).
3. O código **monta** o prompt: instruções fixas + os trechos encontrados + a pergunta.
4. **Chama o LLM**, que faz a parte ambígua: ler os trechos e escrever uma resposta em português claro.
5. O código **valida** (veio vazio? cita fonte?), **loga** e devolve.

Perceba que o modelo só entra no passo 4. Buscar, montar, validar e logar são código comum. Esse é exatamente o [Projeto final - FAQ com RAG (cap. 29)](29-projeto-final-faq-rag.md), e o esqueleto da chamada à API está em [`examples/chamar-api`](../examples/chamar-api).

## Limites honestos (comece simples)

Antes de sonhar grande, encare o que a IA tem de chato:

- **Não-determinismo.** Mesma entrada pode dar saídas diferentes. Isso quebra a intuição de quem programa ("função pura sempre devolve o mesmo"). Como conviver: **valide** a saída sempre, **fixe a temperatura** baixa para tarefas que exigem consistência, e tenha **fallback** quando vier algo fora do esperado. Nunca confie que "veio certo desta vez, vai vir sempre".
- **Latência e custo.** Cada chamada demora (segundos) e custa (por token). Volume alto vira conta alta. O [cap. 28 - Custos e escalabilidade](28-custos-e-escalabilidade.md) mostra como medir e cortar.
- **A API pode falhar ou mudar.** É um serviço externo: fica lento, cai, muda preço ou descontinua um modelo. Seu código precisa aguentar isso (timeout, retry, fallback) e não amarrar tudo num único fornecedor sem pensar.
- **Comece simples.** Não monte agente com 10 tools e RAG multimodal no dia 1. Faça o menor fluxo que resolve, meça, e só então adicione camada. Over-engineering aqui custa caro em dinheiro e em bug.

> **Ilustração, não medida real:** os desenhos e a divisão "IA vs código" acima são esquemáticos, para você pegar a intuição da arquitetura. Números de latência e custo variam por modelo e provedor — sempre confira na fonte oficial e meça no seu caso.

## Exercício

Pegue um app de IA que você gostaria de construir (ex.: um resumidor de artigos, um assistente de FAQ). No papel ou num `.txt`, **desenhe a arquitetura** e responda:

1. Marque cada caixa como **IA (ambíguo)** ou **código (exato)**. Onde a IA é realmente insubstituível?
2. Em que ponto a **chave de API** é usada? (Deve estar só no backend.)
3. Você precisa de **RAG** ou **tools**? Por quê — que dado ou ação o modelo não tem sozinho?
4. Liste **3 lugares onde pode falhar** (timeout, JSON quebrado, resposta sem sentido, custo alto) e, para cada um, **qual é a sua defesa** (retry, fallback, validação, cache).

---

<div align="center">

[« 24 - Rodando modelos localmente](24-rodando-modelos-localmente.md) — [Índice](../README.md#roadmap) — [26 - Segurança em IA »](26-seguranca-em-ia.md)

</div>
