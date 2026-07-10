# -*- coding: utf-8 -*-
"""
Primeira chamada a um LLM via API — IA4Noobs.

Este é o exemplo MAIS BÁSICO possível: enviar UMA pergunta para um modelo de
IA pela API oficial da OpenAI e imprimir a resposta no terminal.

Rode com:  python3 chamar.py
"""

import os
import sys

# A biblioteca `openai` é o SDK oficial. Ela cuida de montar a requisição HTTP,
# enviar sua chave e devolver a resposta já organizada em objetos Python.
from openai import OpenAI


# ---------------------------------------------------------------------------
# 1) A CHAVE DE API
# ---------------------------------------------------------------------------
# NUNCA escreva sua chave direto no código (e nunca suba ela pro GitHub!).
# O jeito certo é guardar em uma VARIÁVEL DE AMBIENTE chamada OPENAI_API_KEY
# e ler daqui. O README explica como configurar essa variável.
chave = os.environ.get("OPENAI_API_KEY")

# Se a chave não existe, avisamos de forma amigável e saímos — sem despejar
# um "stack trace" gigante e assustador na tela.
if not chave:
    print("A variável de ambiente OPENAI_API_KEY não foi encontrada. :(")
    print()
    print("Para configurar, no Linux/macOS (terminal bash/zsh):")
    print('    export OPENAI_API_KEY="sua-chave-aqui"')
    print()
    print("No Windows (PowerShell):")
    print('    $env:OPENAI_API_KEY="sua-chave-aqui"')
    print()
    print("Você pega uma chave em: https://platform.openai.com/api-keys")
    sys.exit(1)  # encerra o programa indicando que algo deu errado


# ---------------------------------------------------------------------------
# 2) O CLIENTE
# ---------------------------------------------------------------------------
# Criamos o "cliente", que é o objeto por onde fazemos as chamadas.
# Ele pega a chave da variável de ambiente automaticamente, mas deixamos
# explícito aqui para ficar didático.
cliente = OpenAI(api_key=chave)


# ---------------------------------------------------------------------------
# 3) A CHAMADA
# ---------------------------------------------------------------------------
# Enviamos uma lista de "mensagens". Cada mensagem tem um papel (role):
#   - "system": instrução geral de como a IA deve se comportar.
#   - "user":   o que VOCÊ está perguntando.
# Usamos o modelo "gpt-4o-mini": é barato e mais que suficiente pra aprender.
print("Enviando pergunta para o modelo... (pode levar alguns segundos)\n")

resposta = cliente.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Você responde em português do Brasil, de forma curta e simples."},
        {"role": "user", "content": "Explique, em 2 frases, o que é inteligência artificial."},
    ],
)


# ---------------------------------------------------------------------------
# 4) A RESPOSTA
# ---------------------------------------------------------------------------
# A resposta vem dentro de `choices`. Pegamos a primeira (índice 0) e o
# conteúdo de texto da mensagem gerada pelo modelo.
texto = resposta.choices[0].message.content

print("Resposta do modelo:")
print("-" * 60)
print(texto)
print("-" * 60)


# ---------------------------------------------------------------------------
# 5) (OPCIONAL) VENDO O USO DE TOKENS
# ---------------------------------------------------------------------------
# Toda chamada de API cobra por TOKENS (pedaços de palavras). O objeto de
# resposta traz quantos tokens foram usados na sua pergunta (prompt), na
# resposta (completion) e no total. É por esses números que você é cobrado.
#
# Descomente as linhas abaixo para ver esses valores:
#
# uso = resposta.usage
# print()
# print("Tokens usados nesta chamada:")
# print(f"  Pergunta (prompt):    {uso.prompt_tokens}")
# print(f"  Resposta (completion): {uso.completion_tokens}")
# print(f"  Total:                {uso.total_tokens}")
#
# Quer entender melhor? Veja os capítulos "05 - O que são Tokens" e
# "28 - Custos e Escalabilidade" do guia.
