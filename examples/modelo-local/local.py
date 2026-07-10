# -*- coding: utf-8 -*-
"""
Rodando um modelo de IA localmente com Ollama — IA4Noobs.

Este script conversa com um modelo de IA que roda NA SUA MÁQUINA, de graça e
sem chave de API, usando o Ollama. Fazemos uma chamada HTTP ao servidor local
do Ollama usando apenas a biblioteca padrão do Python (urllib) — ZERO
dependências para instalar.

Rode com:  python3 local.py
"""

import json
import urllib.error
import urllib.request


# ---------------------------------------------------------------------------
# 1) CONFIGURAÇÃO
# ---------------------------------------------------------------------------
# Quando você roda o Ollama, ele sobe um pequeno servidor HTTP nesta porta,
# na sua própria máquina (localhost = "este computador aqui").
URL = "http://localhost:11434/api/generate"

# Nome do modelo que você baixou com "ollama pull". O llama3.2 é pequeno e
# roda bem em máquinas comuns. Se você baixou outro, troque aqui.
MODELO = "llama3.2"

# A pergunta que vamos mandar para o modelo.
PROMPT = "Explique, em 2 frases e em português, o que é um modelo de linguagem."


# ---------------------------------------------------------------------------
# 2) MONTANDO A REQUISIÇÃO
# ---------------------------------------------------------------------------
# A API do Ollama espera um JSON com o modelo, o prompt e algumas opções.
# "stream": False faz o Ollama devolver a resposta INTEIRA de uma vez (em vez
# de ir mandando pedacinho por pedacinho), o que deixa o código mais simples.
corpo = {
    "model": MODELO,
    "prompt": PROMPT,
    "stream": False,
}

# Transformamos o dicionário Python em texto JSON e depois em bytes, que é o
# formato que a requisição HTTP precisa.
dados = json.dumps(corpo).encode("utf-8")

requisicao = urllib.request.Request(
    URL,
    data=dados,
    headers={"Content-Type": "application/json"},
    method="POST",
)


# ---------------------------------------------------------------------------
# 3) FAZENDO A CHAMADA (com tratamento de erro amigável)
# ---------------------------------------------------------------------------
print(f"Enviando pergunta para o modelo '{MODELO}' (rodando localmente)...\n")

try:
    # Abre a conexão e espera a resposta. timeout evita travar para sempre.
    with urllib.request.urlopen(requisicao, timeout=120) as resposta:
        resposta_json = json.loads(resposta.read().decode("utf-8"))

    # O texto gerado pelo modelo vem no campo "response".
    texto = resposta_json.get("response", "").strip()

    print("Resposta do modelo:")
    print("-" * 60)
    print(texto)
    print("-" * 60)

except urllib.error.URLError:
    # Este erro quase sempre significa que o Ollama NÃO está rodando, ou o
    # modelo não foi baixado. Damos uma mensagem clara em vez de um stack trace.
    print("Não consegui falar com o Ollama. :(")
    print()
    print("Verifique se:")
    print("  1. O Ollama está instalado (https://ollama.com).")
    print("  2. O servidor está no ar. Em um terminal, rode:")
    print("       ollama serve")
    print(f"  3. O modelo '{MODELO}' foi baixado. Rode:")
    print(f"       ollama pull {MODELO}")
    print()
    print("Depois, rode este script de novo.")
