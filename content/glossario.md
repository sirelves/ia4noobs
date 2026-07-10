# Glossário

## Agent

Um sistema de IA que não apenas responde a perguntas, mas decide quais ações tomar para cumprir um objetivo, usando ferramentas e repetindo o ciclo "pensar → agir → observar" até concluir a tarefa. Diferente de um chat simples, um agent pode buscar dados, executar código ou chamar APIs por conta própria.

## Alucinação (hallucination)

Quando um modelo de IA gera uma resposta que parece confiante e bem escrita, mas é falsa ou inventada. Acontece porque o modelo prevê o texto mais provável, sem ter uma garantia de que aquilo é verdade.

## ANN (busca aproximada de vizinhos)

Sigla para *Approximate Nearest Neighbor* (vizinho mais próximo aproximado). É a técnica que um banco vetorial usa para achar os vetores mais parecidos sem comparar a busca com todos (o que travaria em milhões de itens). Em troca de raramente errar o vizinho perfeito, fica muito mais rápido. O índice mais comum é o HNSW, que "salta" de vizinho em vizinho até chegar perto.

## Atenção (attention)

Mecanismo central do Transformer. Ao gerar cada token, o modelo "olha" para todos os tokens anteriores e pesa quais são mais relevantes para decidir o próximo. É de onde vem o "contexto": por isso ele consegue ligar um "ela" à pessoa certa da frase.

## Avaliação (eval)

Processo de medir a qualidade das respostas de uma IA de forma sistemática, usando um conjunto de testes (entradas + resposta esperada) em vez de achismo. Métodos comuns: checagem por regra, comparação com referência, LLM-as-judge (um LLM avaliando outro) e revisão humana.

## Banco vetorial

Um tipo de banco de dados feito para guardar embeddings (vetores de números) e encontrar rapidamente os mais parecidos com uma busca. É a peça central do RAG, pois permite recuperar trechos de texto semelhantes ao que o usuário perguntou.

## Chain-of-Thought (cadeia de raciocínio)

Técnica de prompt em que se pede ao modelo para mostrar o raciocínio passo a passo antes de dar a resposta final. Ao "pensar em voz alta", ele tende a errar menos em problemas de lógica, contas ou várias etapas — parecido com resolver uma conta no papel em vez de de cabeça.

## Contexto (janela de contexto)

É o limite de quanto texto (medido em tokens) o modelo consegue "enxergar" de uma vez, somando o que você envia mais o que ele responde. Tudo o que estiver fora dessa janela é como se não existisse para o modelo.

```text
Janela de contexto = system prompt + histórico da conversa + sua mensagem + resposta
```

## Difusão (diffusion)

Mecanismo usado por muitos geradores de imagem. O modelo parte de puro ruído (uma tela de chuviscos) e vai "limpando" esse ruído passo a passo, guiado pelo seu texto, até sobrar a imagem pedida. É diferente da geração de texto, que sai um token por vez.

## Embedding

Uma forma de representar texto (ou imagem, áudio etc.) como uma lista de números que captura o seu significado. Textos com sentido parecido geram embeddings próximos, o que permite comparar e buscar conteúdo por semelhança.

## Few-shot

Técnica de prompt em que você mostra alguns exemplos de entrada e saída antes de pedir a tarefa, ajudando o modelo a entender o padrão esperado. É um meio-termo entre o zero-shot (nenhum exemplo) e o fine-tuning (re-treinar o modelo).

```text
Pergunta: 2 + 2  → Resposta: 4
Pergunta: 5 + 3  → Resposta: 8
Pergunta: 7 + 1  → Resposta:
```

## Fine-tuning

Processo de pegar um modelo já treinado e continuar o treino com dados específicos seus, para que ele fique melhor em uma tarefa ou estilo. É mais caro e trabalhoso que ajustar o prompt, mas pode valer a pena para casos muito especializados.

## Function calling / Tool calling

Recurso que permite ao modelo pedir para executar uma função/ferramenta externa (como consultar o clima ou buscar no banco) e usar o resultado na resposta. O modelo não roda a função sozinho: ele indica qual chamar e com quais argumentos, e o seu código executa.

## IA Generativa

Ramo da IA focado em criar conteúdo novo, como texto, imagens, áudio ou código, em vez de apenas classificar ou prever valores. Os LLMs são um exemplo de IA Generativa voltada para texto.

## In-context learning (aprendizado em contexto)

A capacidade do modelo de "aprender" uma tarefa a partir dos exemplos e instruções do próprio prompt, sem nenhum re-treino (nenhum peso muda). É o que faz o few-shot funcionar: os exemplos condicionam a continuação mais provável. O efeito some quando a conversa acaba.

## Inteligência Artificial

Área da computação que busca fazer máquinas realizarem tarefas que normalmente exigiriam inteligência humana, como entender linguagem, reconhecer imagens ou tomar decisões. É o termo guarda-chuva que engloba Machine Learning, IA Generativa e muito mais.

## LLM (Modelo de Linguagem)

Sigla para *Large Language Model* (Grande Modelo de Linguagem): um modelo treinado em enormes quantidades de texto para prever a próxima palavra e, assim, conseguir conversar, resumir, traduzir e escrever. ChatGPT, Claude e Gemini são exemplos de produtos baseados em LLMs.

## Machine Learning

Subárea da IA em que o sistema aprende padrões a partir de dados, em vez de seguir regras escritas manualmente. Quanto mais e melhores os dados, melhor tende a ser o aprendizado.

## MCP (Model Context Protocol)

Um padrão aberto que define como modelos de IA se conectam a ferramentas e fontes de dados externas de forma padronizada. Em vez de cada aplicação criar sua própria integração, o MCP funciona como uma "tomada universal" entre o modelo e o mundo externo.

## MCP Client

A parte que fica do lado da aplicação de IA (como um chat ou IDE) e que se conecta a um ou mais MCP Servers para usar suas ferramentas e dados. É quem faz os pedidos seguindo o protocolo MCP.

## MCP Server

Um programa que expõe ferramentas, dados ou ações (como acessar arquivos, um banco ou uma API) para serem usados via MCP. Qualquer MCP Client compatível pode se conectar a ele, sem precisar de integração sob medida.

## Modelo aberto e modelo fechado

Modelo **fechado** é acessado por API/produto de uma empresa (ex: GPT, Claude, Gemini): fácil de usar, mas os dados saem para o fornecedor e você paga por uso. Modelo **aberto** pode ser baixado e executado na sua própria máquina ou servidor (ex: Llama, Mistral): mais privacidade e sem custo por token, mas exige hardware e setup.

## Multi-agent

Abordagem em que vários agents trabalham juntos, cada um com um papel ou especialidade, coordenando-se para resolver um problema maior. É como montar um time, em que um agent planeja, outro pesquisa e outro escreve.

## Multimodal

Diz respeito a modelos de IA que lidam com mais de um tipo de dado (modalidade) além de texto — como imagem, áudio e vídeo. Pode ser na **entrada** (você manda uma foto e a IA interpreta) ou na **saída** (você pede em texto e a IA gera a imagem).

## Ollama

Ferramenta que facilita baixar e rodar modelos de IA abertos (como Llama) localmente, na sua própria máquina. Com poucos comandos, ela cuida do download do modelo e ainda abre uma API local para seus programas usarem sem chave de API.

## Parâmetros

Os valores internos que um modelo ajusta durante o treino — os "pesos" (as conexões) do modelo. A quantidade (ex: 8B = 8 bilhões) dá uma ideia do tamanho: modelos maiores costumam ser mais capazes, mas exigem mais memória e poder de processamento para rodar.

## Pré-treinamento

Primeira e mais cara fase de treino de um LLM: ler uma quantidade gigantesca de texto (boa parte da internet, livros, código) treinando só para prever a próxima palavra. É aqui que o modelo absorve gramática, fatos e estilos. O resultado é um "autocompletar" cru, que ainda não sabe conversar — quem ensina isso são as fases seguintes (SFT e RLHF).

## Prompt

A instrução ou pergunta que você envia ao modelo. A qualidade e a clareza do prompt influenciam diretamente a qualidade da resposta.

## Prompt Engineering

A prática de escrever e refinar prompts para obter respostas melhores e mais confiáveis do modelo. Envolve técnicas como dar contexto, exemplos (few-shot), formato de saída desejado e instruções claras.

## Prompt Injection

Ataque em que alguém insere instruções maliciosas dentro do texto que o modelo vai ler, tentando fazê-lo ignorar suas regras ou vazar informações. É um risco especialmente sério quando o modelo lê conteúdo de fontes externas, como sites ou e-mails.

## Quantização

Técnica para reduzir a memória que um modelo ocupa, diminuindo a precisão dos seus parâmetros (ex: de 16 bits para 4 bits por parâmetro). O modelo fica bem menor com uma pequena perda de qualidade — é o que permite rodar modelos grandes em hardware modesto. Como salvar uma foto em JPEG com mais compressão.

## RAG

Sigla para *Retrieval-Augmented Generation* (Geração Aumentada por Recuperação): técnica que busca trechos relevantes em uma base de dados (geralmente um banco vetorial) e os entrega ao modelo junto com a pergunta. Assim, a resposta fica baseada nos seus dados, reduzindo alucinações.

## ReAct

Nome do padrão mais comum de agent: intercalar *Reasoning* (raciocinar) e *Acting* (agir) — o loop pensar → agir → observar → repetir. Alternar pensamento e ação deixa o modelo ajustar o plano com base no que observa a cada passo.

## RLHF

Sigla para *Reinforcement Learning from Human Feedback* (Aprendizado por Reforço com Feedback Humano): técnica de treino em que pessoas avaliam as respostas do modelo e esse feedback é usado para deixá-lo mais útil, seguro e alinhado às expectativas. É um dos motivos pelos quais os assistentes modernos parecem tão "educados" e prestativos.

## SFT (ajuste fino supervisionado)

Sigla para *Supervised Fine-Tuning*. Segunda fase de treino de um assistente: humanos escrevem exemplos de "pergunta boa → resposta boa" e o modelo aprende o formato de seguir instruções e conversar. Vem depois do pré-treinamento e antes do RLHF.

## Similaridade de cosseno

Medida de quão parecidos são dois embeddings. Olha o ângulo entre os dois vetores: mesma direção (ângulo pequeno) = valor perto de 1 = muito parecido; direções sem relação = valor perto de 0. É como se mede "perto no mapa" de significados.

## Skill

Uma capacidade ou conjunto de instruções e recursos especializados que um agent pode carregar para realizar um tipo específico de tarefa. Funciona como um "módulo" que o agent ativa quando a tarefa combina com aquela habilidade.

## System prompt

Uma instrução inicial e geralmente invisível ao usuário que define o papel, o tom e as regras do modelo durante a conversa. É onde se diz, por exemplo, "você é um assistente de suporte educado e objetivo".

## Temperatura

Parâmetro que controla o quão criativa ou aleatória é a resposta do modelo. Valores baixos deixam a saída mais focada e previsível; valores altos a deixam mais variada e criativa.

```text
temperatura 0.0  → respostas mais determinísticas e consistentes
temperatura 1.0  → respostas mais variadas e criativas
```

## Token

A menor unidade de texto que o modelo processa: pode ser uma palavra, um pedaço de palavra ou um sinal de pontuação. Modelos contam preços e limites em tokens, não em caracteres ou palavras.

## Tokenização

O processo de quebrar um texto em tokens antes de o modelo processá-lo. Entender isso ajuda a estimar custos e a respeitar a janela de contexto.

```text
"Inteligência Artificial" → ["Intelig", "ência", " Artificial"]
```

## Tool

Uma ferramenta externa que o modelo pode usar para fazer algo que sozinho não faria, como buscar na web, consultar um banco ou enviar um e-mail. As tools são acionadas via function calling / tool calling.

## Transformer

A arquitetura por trás dos LLMs modernos. Sua peça central é a atenção, que pesa a relevância de cada token anterior ao gerar o próximo. Foi o que permitiu os modelos manterem coerência por textos longos.

## Zero-shot

Quando você pede uma tarefa ao modelo sem dar nenhum exemplo, contando apenas com o conhecimento que ele já tem. É o oposto do few-shot, em que você fornece exemplos para guiar a resposta.

---

<div align="center">

[« 29 - Projeto final: um assistente de FAQ com RAG](29-projeto-final-faq-rag.md) — [Índice](../README.md#roadmap)

</div>
