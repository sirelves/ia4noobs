# -*- coding: utf-8 -*-
"""
Zero-shot vs Few-shot na prática — IA4Noobs.

Este script faz DUAS chamadas ao mesmo modelo, para a MESMA tarefa (classificar
o sentimento de uma frase), para você comparar:
  (a) ZERO-SHOT: pedimos direto, sem dar nenhum exemplo.
  (b) FEW-SHOT:  damos alguns exemplos de entrada -> saída antes de perguntar.

Rode com:  python3 few_shot.py
"""

import os
import sys

from openai import OpenAI


# ---------------------------------------------------------------------------
# 1) A CHAVE DE API (mesmo padrão do exemplo "chamar-api")
# ---------------------------------------------------------------------------
chave = os.environ.get("OPENAI_API_KEY")

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
    sys.exit(1)

cliente = OpenAI(api_key=chave)


# A frase que queremos classificar nas duas abordagens.
# Escolhemos algo um pouco ambíguo de propósito, para os exemplos fazerem
# diferença. "Nem vem" costuma indicar irritação/negatividade.
FRASE = "O produto chegou no prazo, mas nem vem que a embalagem estava toda amassada."


def classificar_zero_shot(frase):
    """(a) ZERO-SHOT: pede a classificação SEM dar exemplos.

    Só explicamos a tarefa. O modelo se vira sozinho — e pode responder num
    formato imprevisível (uma frase inteira, uma explicação longa, etc.).
    """
    resposta = cliente.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Classifique o sentimento desta frase: {frase}",
            },
        ],
    )
    return resposta.choices[0].message.content.strip()


def classificar_few_shot(frase):
    """(b) FEW-SHOT: mostra EXEMPLOS de entrada -> saída antes de perguntar.

    Ao ver o padrão "Frase: ... / Sentimento: UMA_PALAVRA", o modelo aprende
    tanto a TAREFA quanto o FORMATO exato que esperamos. O resultado tende a
    ser mais consistente (só POSITIVO, NEGATIVO ou NEUTRO).
    """
    resposta = cliente.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Você classifica o sentimento de frases em português. "
                    "Responda APENAS com uma palavra: POSITIVO, NEGATIVO ou NEUTRO."
                ),
            },
            # --- Os "shots" (exemplos). São conversas de mentira que ensinam
            #     o modelo pelo exemplo. Cada par usuário -> assistente mostra
            #     uma entrada e a saída ideal. ---
            {"role": "user", "content": "Frase: Adorei o atendimento, super rápido!"},
            {"role": "assistant", "content": "POSITIVO"},
            {"role": "user", "content": "Frase: O pedido veio errado e ninguém me respondeu."},
            {"role": "assistant", "content": "NEGATIVO"},
            {"role": "user", "content": "Frase: O produto é do tamanho que estava na descrição."},
            {"role": "assistant", "content": "NEUTRO"},
            # --- Agora, enfim, a frase de verdade que queremos classificar. ---
            {"role": "user", "content": f"Frase: {frase}"},
        ],
    )
    return resposta.choices[0].message.content.strip()


# ---------------------------------------------------------------------------
# 2) EXECUÇÃO — roda as duas abordagens e mostra lado a lado
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("Frase a classificar:")
    print(f"  {FRASE}")
    print()
    print("Consultando o modelo nas duas abordagens...\n")

    resultado_zero = classificar_zero_shot(FRASE)
    resultado_few = classificar_few_shot(FRASE)

    print("=" * 60)
    print("ZERO-SHOT (sem exemplos)")
    print("-" * 60)
    print(resultado_zero)
    print("=" * 60)
    print("FEW-SHOT (com exemplos)")
    print("-" * 60)
    print(resultado_few)
    print("=" * 60)
    print(
        "\nRepare: no zero-shot a resposta costuma vir mais 'solta' (talvez uma\n"
        "frase inteira). No few-shot, os exemplos ensinam o FORMATO e a saída\n"
        "sai curta e padronizada. É por isso que exemplos ajudam tanto."
    )
