<!-- Logo 4noobs -->

<p align="center">
  <a href="https://github.com/he4rt/4noobs" target="_blank">
    <img src="https://raw.githubusercontent.com/he4rt/4noobs/master/.github/header_4noobs.svg" alt="4noobs">
  </a>
</p>

<!-- Title -->

<p align="center">
  <h2 align="center">IA4Noobs</h2>

  <h1 align="center">
    <img src="https://api.iconify.design/mdi/brain.svg?color=%237c3aed&width=120&height=120" alt="Logo de IA" width="120">
  </h1>

  <p align="center">
    <br />
    <a href="#roadmap"><strong>Explore a documentação »</strong></a>
    <br />
    <br />
    <a href="#como-contribuir">Contribuir</a>
    ·
    <a href="#exemplos">Ver exemplos</a>
    ·
    <a href="CONTRIBUTING.md">Guia de contribuição</a>
  </p>
</p>

## Sobre o Projeto

IA4Noobs é um guia introdutório de Inteligência Artificial para pessoas que estão começando e querem entender, sem enrolação, como as IAs modernas funcionam e como usá-las bem no dia a dia e em projetos.

A proposta é sair do "eu uso o ChatGPT, mas não sei o que acontece por trás" para um entendimento prático: o que são tokens e contexto, como escrever bons prompts, o que são embeddings, RAG, agents, tools e MCP, e o que muda quando você leva uma aplicação de IA para produção.

Este guia foca em **conceitos e prática**, não em matemática pesada. Você não precisa saber cálculo nem treinar modelos para aproveitar.

## Para quem é este guia?

Este material foi pensado para quem:

- usa (ou quer usar) ferramentas como ChatGPT, Claude ou Gemini e quer entender o que está acontecendo;
- é desenvolvedor(a) e quer começar a construir aplicações com IA;
- ouviu falar de "prompt engineering", "RAG", "agents" e "MCP", mas se perde nos termos;
- quer uma base sólida em português antes de partir para conteúdos mais avançados.

## Requisitos

Antes de começar, é útil ter:

- curiosidade e vontade de testar as coisas;
- uma conta em alguma ferramenta de IA (ChatGPT, Claude, Gemini ou similar);
- noções básicas de programação **para os módulos 4, 5 e 6** (os primeiros não exigem código);
- um editor de código, se quiser rodar os exemplos.

> Não precisa ser especialista. A ideia é aprender errando, testando e perguntando.

## ROADMAP

O guia é dividido em 7 módulos. Você pode ler na ordem ou pular para o que mais interessa.

### Módulo 1 — Fundamentos

- [00 - Introdução](content/00-introducao.md)
- [01 - O que é Inteligência Artificial](content/01-o-que-e-inteligencia-artificial.md)
- [02 - O que é IA Generativa](content/02-o-que-e-ia-generativa.md)
- [03 - IA Multimodal](content/03-ia-multimodal.md)
- [04 - Como o ChatGPT funciona](content/04-como-o-chatgpt-funciona.md)
- [05 - O que são Tokens](content/05-o-que-sao-tokens.md)
- [06 - O que é Janela de Contexto](content/06-o-que-e-janela-de-contexto.md)
- [07 - Escolhendo o modelo certo](content/07-escolhendo-o-modelo-certo.md)

### Módulo 2 — Conversando com IA

- [08 - O que é Prompt Engineering](content/08-o-que-e-prompt-engineering.md)
- [09 - Como fazer perguntas melhores](content/09-como-fazer-perguntas-melhores.md)
- [10 - Few-shot e Chain-of-Thought](content/10-few-shot-e-chain-of-thought.md)
- [11 - Como estruturar respostas](content/11-como-estruturar-respostas.md)
- [12 - Principais erros ao usar IA](content/12-principais-erros-ao-usar-ia.md)

### Módulo 3 — Conhecimento

- [13 - O que são Embeddings](content/13-o-que-sao-embeddings.md)
- [14 - O que é RAG](content/14-o-que-e-rag.md)
- [15 - O que é Banco Vetorial](content/15-o-que-e-banco-vetorial.md)

### Módulo 4 — Agents

- [16 - O que é um Agent](content/16-o-que-e-um-agent.md)
- [17 - O que é uma Tool](content/17-o-que-e-uma-tool.md)
- [18 - O que são Skills](content/18-o-que-sao-skills.md)
- [19 - Arquitetura básica de Agents](content/19-arquitetura-basica-de-agents.md)
- [20 - Multi-Agent Systems](content/20-multi-agent-systems.md)

### Módulo 5 — MCP

- [21 - O que é MCP](content/21-o-que-e-mcp.md)
- [22 - MCP Client e MCP Server](content/22-mcp-client-e-mcp-server.md)
- [23 - Criando seu primeiro MCP](content/23-criando-seu-primeiro-mcp.md)

### Módulo 6 — Produção

- [24 - Rodando modelos localmente](content/24-rodando-modelos-localmente.md)
- [25 - Como criar aplicações com IA](content/25-como-criar-aplicacoes-com-ia.md)
- [26 - Segurança em IA](content/26-seguranca-em-ia.md)
- [27 - Como avaliar respostas de IA](content/27-como-avaliar-respostas-de-ia.md)
- [28 - Custos e Escalabilidade](content/28-custos-e-escalabilidade.md)

### Módulo 7 — Prática

- [29 - Projeto final: um assistente de FAQ com RAG](content/29-projeto-final-faq-rag.md)

### Apoio

- [Glossário](content/glossario.md)

## Exemplos

Este repositório também traz exemplos pequenos para praticar:

- [Prompts: ruim vs bom](examples/primeiro-prompt) — comparando prompts e por que alguns funcionam melhor.
- [Sua primeira chamada de API](examples/chamar-api) — o "Hello World" de falar com um LLM via código.
- [Few-shot na prática](examples/few-shot) — zero-shot vs few-shot na mesma tarefa, lado a lado.
- [Rodando um modelo local](examples/modelo-local) — chamando um LLM na sua máquina com Ollama, sem chave de API.
- [RAG mínimo em Python](examples/rag-mini) — busca por similaridade explicada com código comentado.
- [Servidor MCP "Hello World"](examples/mcp-hello) — um MCP server mínimo para entender a estrutura.

## Como estudar

Uma sugestão simples:

1. Leia um capítulo.
2. Teste o conceito em uma ferramenta de IA real.
3. Mude algo pequeno no prompt ou no exemplo.
4. Repare no que mudou na resposta.
5. Explique o conceito com suas próprias palavras.

IA se aprende **conversando com ela**. Tenha uma janela de chat aberta enquanto lê.

## Onde continuar estudando

Terminou o guia e quer ir mais fundo? Alguns materiais gratuitos e de qualidade:

- **[CS50's Introduction to Artificial Intelligence with Python](https://cs50.harvard.edu/ai)** (Harvard) — curso gratuito e clássico sobre os fundamentos da IA (busca, otimização, machine learning) com projetos em Python. É **mais técnico e matemático** que este guia, então é um ótimo próximo passo depois daqui.
- **[Documentação da Anthropic](https://docs.anthropic.com)** e **[da OpenAI](https://platform.openai.com/docs)** — referências oficiais para construir aplicações, com guias de prompt, agents e boas práticas.
- **[Índice do 4noobs](https://github.com/he4rt/4noobs)** — guias de várias linguagens e tecnologias da comunidade HE4RT para fortalecer sua base.

## Como Contribuir

Contribuições fazem com que a comunidade open source seja um lugar incrível para aprender, inspirar e criar. Todas contribuições são **extremamente apreciadas** — e este guia tem espaço de sobra para a sua.

1. Realize um Fork do projeto
2. Crie um branch com a sua contribuição (`git checkout -b feature/featureBraba`)
3. Realize o Commit (`git commit -m 'Adicionado conteudo brabo'`)
4. Realize o Push no Branch (`git push origin feature/featureBraba`)
5. Abra um Pull Request

Quer o passo a passo detalhado, padrões de escrita e ideias do que fazer? Leia o **[CONTRIBUTING.md](CONTRIBUTING.md)**. Não sabe por onde começar? Procure as issues com a label `good first issue` ou abra uma usando os nossos [templates de issue](.github/ISSUE_TEMPLATE).

## Publicação no 4noobs

Quando o guia estiver revisado e publicado no GitHub, use o arquivo [PUBLISHING.md](PUBLISHING.md) para preparar a entrada no índice principal do `he4rt/4noobs`.

## Autores

- **Elves S.** - _Autor_ - [@sirelves](https://github.com/sirelves)
- **IA4Noobs contributors** - _Comunidade_

---

<p align="center">
  <a href="https://github.com/he4rt/4noobs" target="_blank">
    <img src="https://raw.githubusercontent.com/he4rt/4noobs/master/.github/footer_4noobs.svg" width="380" alt="4noobs footer">
  </a>
</p>
