# Publicação no índice 4noobs

Este arquivo ajuda a preparar o PR no repositório principal `he4rt/4noobs`.

Antes de abrir PR, valide a ideia no canal `#4noobs` do Discord da HE4RT, como indicado no template de issues do projeto.

## Checklist do PR

- [ ] O guia está finalizado e revisado.
- [ ] O README segue o template de roadmap do 4noobs.
- [ ] O conteúdo não fere direitos autorais.
- [ ] A entrada foi adicionada no `README.MD` do `he4rt/4noobs`.
- [ ] A entrada foi adicionada em `.github/config.json` do `he4rt/4noobs`.
- [ ] Os links apontam para o repositório publicado.

## Entrada para o README.MD

Adicione uma linha na tabela da seção **🤖 Diversos** (categoria que hoje reúne QA, DevOps e Acessibilidade). As colunas são `Nome | Descrição | Contribuidores | Link`:

```md
| IA | Aprenda Inteligência Artificial do zero: fundamentos, prompt engineering, embeddings, RAG, agents, MCP e como levar aplicações de IA para produção. | [Elves S.](https://github.com/sirelves) | [Clique aqui ➡️](https://github.com/sirelves/ia4noobs) |
```

## Entrada para .github/config.json

Use este bloco como base para adicionar o guia em `.github/config.json`.

```json
{
  "name": "IA4noobs",
  "tags": ["IA", "LLM", "Prompt Engineering", "RAG", "Agents", "MCP"],
  "image": "https://api.iconify.design/mdi/brain.svg?color=%237c3aed&width=120&height=120",
  "description": "Aprenda Inteligência Artificial do zero: fundamentos, prompt engineering, embeddings, RAG, agents, MCP e como levar aplicações de IA para produção.",
  "category": "Diversos",
  "author": {
    "name": "Elves S.",
    "username": "sirelves",
    "avatar_url": "https://github.com/sirelves.png"
  },
  "url": "https://github.com/sirelves/ia4noobs"
}
```
