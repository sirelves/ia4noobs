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
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/openai/openai-original.svg" alt="Logo de IA" width="120">
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

O guia é dividido em 6 módulos. Você pode ler na ordem ou pular para o que mais interessa.

### Módulo 1 — Fundamentos

- [00 - Introdução](content/00-introducao.md)
- [01 - O que é Inteligência Artificial](content/01-o-que-e-inteligencia-artificial.md)
- [02 - O que é IA Generativa](content/02-o-que-e-ia-generativa.md)
- [03 - Como o ChatGPT funciona](content/03-como-o-chatgpt-funciona.md)
- [04 - O que são Tokens](content/04-o-que-sao-tokens.md)
- [05 - O que é Janela de Contexto](content/05-o-que-e-janela-de-contexto.md)

### Módulo 2 — Conversando com IA

- [06 - O que é Prompt Engineering](content/06-o-que-e-prompt-engineering.md)
- [07 - Como fazer perguntas melhores](content/07-como-fazer-perguntas-melhores.md)
- [08 - Como estruturar respostas](content/08-como-estruturar-respostas.md)
- [09 - Principais erros ao usar IA](content/09-principais-erros-ao-usar-ia.md)

### Módulo 3 — Conhecimento

- [10 - O que são Embeddings](content/10-o-que-sao-embeddings.md)
- [11 - O que é RAG](content/11-o-que-e-rag.md)
- [12 - O que é Banco Vetorial](content/12-o-que-e-banco-vetorial.md)

### Módulo 4 — Agents

- [13 - O que é um Agent](content/13-o-que-e-um-agent.md)
- [14 - O que é uma Tool](content/14-o-que-e-uma-tool.md)
- [15 - O que são Skills](content/15-o-que-sao-skills.md)
- [16 - Arquitetura básica de Agents](content/16-arquitetura-basica-de-agents.md)
- [17 - Multi-Agent Systems](content/17-multi-agent-systems.md)

### Módulo 5 — MCP

- [18 - O que é MCP](content/18-o-que-e-mcp.md)
- [19 - MCP Client e MCP Server](content/19-mcp-client-e-mcp-server.md)
- [20 - Criando seu primeiro MCP](content/20-criando-seu-primeiro-mcp.md)

### Módulo 6 — Produção

- [21 - Como criar aplicações com IA](content/21-como-criar-aplicacoes-com-ia.md)
- [22 - Segurança em IA](content/22-seguranca-em-ia.md)
- [23 - Como avaliar respostas de IA](content/23-como-avaliar-respostas-de-ia.md)
- [24 - Custos e Escalabilidade](content/24-custos-e-escalabilidade.md)

### Apoio

- [Glossário](content/glossario.md)

## Exemplos

Este repositório também traz exemplos pequenos para praticar:

- [Prompts: ruim vs bom](examples/primeiro-prompt) — comparando prompts e por que alguns funcionam melhor.
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
