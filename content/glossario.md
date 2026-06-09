# Glossário

## Agent

Um sistema de IA que não apenas responde a perguntas, mas decide quais ações tomar para cumprir um objetivo, usando ferramentas e repetindo o ciclo "pensar → agir → observar" até concluir a tarefa. Diferente de um chat simples, um agent pode buscar dados, executar código ou chamar APIs por conta própria.

## Alucinação (hallucination)

Quando um modelo de IA gera uma resposta que parece confiante e bem escrita, mas é falsa ou inventada. Acontece porque o modelo prevê o texto mais provável, sem ter uma garantia de que aquilo é verdade.

## Banco vetorial

Um tipo de banco de dados feito para guardar embeddings (vetores de números) e encontrar rapidamente os mais parecidos com uma busca. É a peça central do RAG, pois permite recuperar trechos de texto semelhantes ao que o usuário perguntou.

## Contexto (janela de contexto)

É o limite de quanto texto (medido em tokens) o modelo consegue "enxergar" de uma vez, somando o que você envia mais o que ele responde. Tudo o que estiver fora dessa janela é como se não existisse para o modelo.

```text
Janela de contexto = system prompt + histórico da conversa + sua mensagem + resposta
```

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

## Multi-agent

Abordagem em que vários agents trabalham juntos, cada um com um papel ou especialidade, coordenando-se para resolver um problema maior. É como montar um time, em que um agent planeja, outro pesquisa e outro escreve.

## Prompt

A instrução ou pergunta que você envia ao modelo. A qualidade e a clareza do prompt influenciam diretamente a qualidade da resposta.

## Prompt Engineering

A prática de escrever e refinar prompts para obter respostas melhores e mais confiáveis do modelo. Envolve técnicas como dar contexto, exemplos (few-shot), formato de saída desejado e instruções claras.

## Prompt Injection

Ataque em que alguém insere instruções maliciosas dentro do texto que o modelo vai ler, tentando fazê-lo ignorar suas regras ou vazar informações. É um risco especialmente sério quando o modelo lê conteúdo de fontes externas, como sites ou e-mails.

## RAG

Sigla para *Retrieval-Augmented Generation* (Geração Aumentada por Recuperação): técnica que busca trechos relevantes em uma base de dados (geralmente um banco vetorial) e os entrega ao modelo junto com a pergunta. Assim, a resposta fica baseada nos seus dados, reduzindo alucinações.

## RLHF

Sigla para *Reinforcement Learning from Human Feedback* (Aprendizado por Reforço com Feedback Humano): técnica de treino em que pessoas avaliam as respostas do modelo e esse feedback é usado para deixá-lo mais útil, seguro e alinhado às expectativas. É um dos motivos pelos quais os assistentes modernos parecem tão "educados" e prestativos.

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

## Zero-shot

Quando você pede uma tarefa ao modelo sem dar nenhum exemplo, contando apenas com o conhecimento que ele já tem. É o oposto do few-shot, em que você fornece exemplos para guiar a resposta.

---

<div align="center">

[« 24 - Custos e Escalabilidade](24-custos-e-escalabilidade.md) — [Índice](../README.md#roadmap)

</div>
