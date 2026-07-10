# Publicação no índice 4noobs

Este arquivo ajuda a preparar o PR no repositório principal `he4rt/4noobs`.

Antes de abrir PR, valide a ideia no canal `#4noobs` do Discord da HE4RT, como indicado no template de issues do projeto.

## Checklist do PR

Do lado do IA4Noobs (feito):

- [x] O guia está finalizado e revisado (7 módulos, 30 capítulos + glossário, 6 exemplos; revisão técnica concluída).
- [x] O README segue o template de roadmap do 4noobs.
- [x] O conteúdo é original e não fere direitos autorais.
- [x] Os links apontam para o repositório publicado (`https://github.com/sirelves/ia4noobs`).

Do lado do `he4rt/4noobs` (fazer ao abrir o PR lá):

- [ ] A entrada foi adicionada no `README.MD` do `he4rt/4noobs` (seção 🤖 Diversos).
- [ ] A entrada foi adicionada em `.github/config.json` do `he4rt/4noobs`.
- [ ] Ideia validada no canal `#4noobs` do Discord da HE4RT.

## Entrada para o README.MD

Adicione uma linha na tabela da seção **🤖 Diversos** (categoria que hoje reúne QA, DevOps e Acessibilidade). As colunas são `Nome | Descrição | Contribuidores | Link`:

```md
| IA | Aprenda Inteligência Artificial do zero: fundamentos, tokens e contexto, prompt engineering (few-shot, chain-of-thought), embeddings, RAG, agents, tools, MCP, rodar modelos localmente e como levar aplicações de IA para produção (segurança, avaliação e custos). | [Elves S.](https://github.com/sirelves) | [Clique aqui ➡️](https://github.com/sirelves/ia4noobs) |
```

## Entrada para .github/config.json

Use este bloco como base para adicionar o guia em `.github/config.json`.

```json
{
  "name": "IA4noobs",
  "tags": ["IA", "LLM", "Prompt Engineering", "Embeddings", "RAG", "Agents", "MCP"],
  "image": "https://api.iconify.design/mdi/brain.svg?color=%237c3aed&width=120&height=120",
  "description": "Aprenda Inteligência Artificial do zero: fundamentos, tokens e contexto, prompt engineering (few-shot, chain-of-thought), embeddings, RAG, agents, tools, MCP, rodar modelos localmente e como levar aplicações de IA para produção (segurança, avaliação e custos).",
  "category": "Diversos",
  "author": {
    "name": "Elves S.",
    "username": "sirelves",
    "avatar_url": "https://github.com/sirelves.png"
  },
  "url": "https://github.com/sirelves/ia4noobs"
}
```
