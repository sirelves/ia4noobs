# Como contribuir com o IA4Noobs

Que bom que você quer ajudar! 🎉 Este guia é **open source e feito pela comunidade**. Toda contribuição conta: corrigir um typo, melhorar uma explicação, adicionar um exemplo ou escrever um capítulo inteiro.

Este documento existe para deixar o caminho claro — algo que faz toda a diferença para quem está começando a contribuir.

## Antes de começar

Se a sua ideia for grande (um capítulo novo, reorganizar um módulo, um exemplo grande), vale **abrir uma issue primeiro** para conversarmos. Assim a gente evita trabalho duplicado e alinha o formato.

Para contribuições pequenas (typo, link quebrado, um parágrafo mais claro), pode mandar o Pull Request direto.

## Passo a passo

1. Faça um **fork** do projeto.
2. Crie uma branch descritiva:
   ```bash
   git checkout -b feature/capitulo-embeddings
   ```
3. Faça suas alterações seguindo o [padrão de escrita](#padrão-de-escrita).
4. Faça commits claros:
   ```bash
   git commit -m "Adiciona capítulo sobre embeddings"
   ```
5. Envie para o seu fork:
   ```bash
   git push origin feature/capitulo-embeddings
   ```
6. Abra um **Pull Request** descrevendo o que mudou e por quê.

## Ideias de contribuição

Não precisa inventar nada do zero. Algumas formas de ajudar:

- **Melhorar explicações** que ficaram confusas ou longas demais.
- **Adicionar exemplos** práticos e exercícios ao fim dos capítulos.
- **Corrigir termos técnicos** ou traduções que ficaram estranhas.
- **Adicionar analogias** que ajudem iniciantes a entender.
- **Revisar capítulos** procurando erros, links quebrados e informações desatualizadas (IA muda rápido!).
- **Criar diagramas ou imagens** para conceitos visuais (embeddings, arquitetura de agents, fluxo de RAG).
- **Adicionar termos ao [glossário](content/glossario.md)**.
- **Traduzir** trechos ou exemplos.

Procure as issues com a label `good first issue` se quiser um ponto de partida.

## Padrão de escrita

Para o guia ficar coeso, siga estes princípios — os mesmos do resto do material:

- **Português claro e direto.** Frases curtas. Evite jargão sem explicar.
- **Fale com quem está começando.** Assuma que a pessoa nunca viu o assunto. Use analogias do mundo real.
- **Mostre, não só conte.** Sempre que possível, traga um exemplo concreto (um prompt, um trecho de código, um comparativo).
- **Sem matemática pesada.** O foco é intuição e prática. Se precisar de fórmula, explique o que ela significa em palavras.
- **Seja honesto sobre limitações.** IA erra, "alucina" e tem custo. Não venda mágica.

### Estrutura de um capítulo

Cada capítulo fica em `content/` com o nome no formato `NN-titulo-em-kebab-case.md` e segue este esqueleto:

```markdown
# NN - Título do Capítulo

Parágrafo curto explicando o que é o assunto e por que ele importa.

## Um subtópico

Texto, listas e exemplos.

## Outro subtópico

...

## Exercício

Uma ou duas perguntas/tarefas para a pessoa praticar.

---

<div align="center">

[« NN - Capítulo anterior](NN-anterior.md) — [Índice](../README.md#roadmap) — [NN - Próximo capítulo »](NN-proximo.md)

</div>
```

Pontos importantes:

- O **rodapé de navegação** entre capítulos é obrigatório (anterior · índice · próximo). O primeiro capítulo não tem "anterior"; o último não tem "próximo".
- Blocos de código sempre com a linguagem marcada (` ```python `, ` ```bash `, ` ```text `).
- Se adicionar um capítulo novo no meio, lembre de **atualizar os links de navegação** dos capítulos vizinhos e o **ROADMAP** no [README](README.md).
- Adicionou um termo novo importante? Inclua no [glossário](content/glossario.md).

## Exemplos de código

Os exemplos ficam em `examples/`. Cada um deve ter um `README.md` explicando como rodar.

- Mantenha as dependências **mínimas**. Quanto mais fácil de rodar, melhor.
- **Nunca** versione chaves de API, tokens ou segredos. Use variáveis de ambiente e um `.env.example`.
- Comente o código pensando em quem está aprendendo.

## Dúvidas?

Entre no Discord da [HE4RT Developers](https://discord.gg/he4rt) e procure o canal `#4noobs`. A comunidade ajuda. 💜

Obrigado por contribuir!
