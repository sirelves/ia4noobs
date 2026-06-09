# -*- coding: utf-8 -*-
"""
RAG mínimo — busca por similaridade (apenas biblioteca padrão do Python).

Este script mostra o CORAÇÃO de um RAG: a etapa de "retrieval" (recuperação).
Ou seja: dada uma pergunta, achamos os trechos mais parecidos dentro de uma
base de documentos.

IMPORTANTE (simplificação didática):
- O "embedding" aqui é FALSO/simplificado: usamos um vetor de frequência de
  palavras (bag-of-words) sobre um vocabulário montado a partir dos documentos.
  Num RAG de verdade, você usaria um MODELO DE EMBEDDINGS real (ex.: um modelo
  que entende significado), que transforma texto em vetores onde frases com
  sentido parecido ficam "próximas" mesmo sem repetir as mesmas palavras.
- Não há LLM aqui. Só fazemos a busca. Num RAG completo, os trechos recuperados
  seriam colados no prompt de um LLM para gerar a resposta final.
- Não há banco vetorial. Uma simples lista em memória faz esse papel.

Rode com:  python3 busca.py
"""

import math
import re


# ---------------------------------------------------------------------------
# 1) A "BASE DE CONHECIMENTO"
# ---------------------------------------------------------------------------
# Num RAG real, isto seriam seus documentos (PDFs, páginas, artigos) já
# quebrados em pequenos pedaços ("chunks"). Aqui usamos frases curtas em pt-BR
# sobre temas variados, só para o exemplo ficar simples de entender.
DOCUMENTOS = [
    "O gato dorme o dia inteiro no sofá da sala.",
    "Python é uma linguagem de programação fácil de aprender.",
    "A fotossíntese transforma luz solar em energia para as plantas.",
    "O Brasil é o maior produtor de café do mundo.",
    "Cachorros gostam de passear e brincar no parque.",
    "Aprender a programar abre muitas portas no mercado de trabalho.",
    "O café da manhã é considerado a refeição mais importante do dia.",
    "As estrelas que vemos à noite estão a anos-luz de distância.",
]


# ---------------------------------------------------------------------------
# 2) TOKENIZAÇÃO — quebrar o texto em palavras
# ---------------------------------------------------------------------------
def tokenizar(texto):
    """Coloca tudo em minúsculas e extrai apenas as palavras (sem pontuação).

    Ex.: "O gato dorme!" -> ["o", "gato", "dorme"]
    """
    texto = texto.lower()
    # \w+ pega sequências de letras/números; inclui acentos via flag UNICODE.
    return re.findall(r"\w+", texto, flags=re.UNICODE)


# ---------------------------------------------------------------------------
# 3) VOCABULÁRIO — todas as palavras conhecidas pela base
# ---------------------------------------------------------------------------
# O vetor de cada documento terá UMA POSIÇÃO para cada palavra do vocabulário.
# Construímos o vocabulário a partir de TODOS os documentos.
def construir_vocabulario(documentos):
    vocab = set()
    for doc in documentos:
        for palavra in tokenizar(doc):
            vocab.add(palavra)
    # Ordenamos para que a posição de cada palavra no vetor seja sempre a mesma.
    return sorted(vocab)


# ---------------------------------------------------------------------------
# 4) "EMBEDDING" SIMPLIFICADO — texto vira vetor de números
# ---------------------------------------------------------------------------
# Esta é a peça que, num RAG real, seria um modelo de embeddings de verdade.
# Aqui é só uma CONTAGEM: para cada palavra do vocabulário, quantas vezes ela
# aparece no texto. Frases que compartilham palavras ficam com vetores parecidos.
def texto_para_vetor(texto, vocabulario):
    # Conta quantas vezes cada palavra aparece neste texto.
    contagem = {}
    for palavra in tokenizar(texto):
        contagem[palavra] = contagem.get(palavra, 0) + 1
    # Monta o vetor seguindo a ordem do vocabulário.
    return [contagem.get(palavra, 0) for palavra in vocabulario]


# ---------------------------------------------------------------------------
# 5) SIMILARIDADE DO COSSENO — o quão "parecidos" são dois vetores
# ---------------------------------------------------------------------------
# Mede o ângulo entre dois vetores. Resultado entre 0 e 1 (para contagens):
#   1.0  -> mesma direção (muito parecidos)
#   0.0  -> nada em comum
# É a mesma ideia usada por bancos vetoriais para achar "o mais próximo".
def similaridade_cosseno(vetor_a, vetor_b):
    produto_escalar = sum(a * b for a, b in zip(vetor_a, vetor_b))
    norma_a = math.sqrt(sum(a * a for a in vetor_a))
    norma_b = math.sqrt(sum(b * b for b in vetor_b))
    # Evita divisão por zero (texto vazio ou sem palavras conhecidas).
    if norma_a == 0 or norma_b == 0:
        return 0.0
    return produto_escalar / (norma_a * norma_b)


# ---------------------------------------------------------------------------
# 6) O "RETRIEVAL" — buscar os documentos mais parecidos com a pergunta
# ---------------------------------------------------------------------------
def buscar(pergunta, documentos, vocabulario, top_n=3):
    """Retorna os top_n documentos mais parecidos com a pergunta.

    Este é EXATAMENTE o passo de "retrieval" do RAG:
    transformamos a pergunta em vetor e comparamos com cada documento.
    """
    vetor_pergunta = texto_para_vetor(pergunta, vocabulario)

    resultados = []
    for doc in documentos:
        vetor_doc = texto_para_vetor(doc, vocabulario)
        score = similaridade_cosseno(vetor_pergunta, vetor_doc)
        resultados.append((score, doc))

    # Ordena do mais parecido (maior score) para o menos parecido.
    resultados.sort(key=lambda item: item[0], reverse=True)
    return resultados[:top_n]


# ---------------------------------------------------------------------------
# 7) EXECUÇÃO — junta tudo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Monta o vocabulário uma vez (num RAG real, os vetores ficariam salvos
    # num banco vetorial, calculados uma única vez e reaproveitados).
    vocabulario = construir_vocabulario(DOCUMENTOS)

    # Você pode digitar uma pergunta. Se apenas apertar Enter (ou não houver
    # entrada disponível), usamos uma pergunta de exemplo.
    try:
        pergunta = input("Digite sua pergunta (ou Enter para o exemplo): ").strip()
    except EOFError:
        pergunta = ""

    if not pergunta:
        pergunta = "Quero aprender a programar"

    print("\nPergunta:", pergunta)
    print("-" * 60)

    melhores = buscar(pergunta, DOCUMENTOS, vocabulario, top_n=3)

    print("Top 3 documentos mais parecidos (o 'retrieval' do RAG):\n")
    for posicao, (score, doc) in enumerate(melhores, start=1):
        print(f"{posicao}. (score {score:.3f}) {doc}")

    print("-" * 60)
    print(
        "Num RAG de verdade, estes trechos recuperados seriam colocados\n"
        "dentro do prompt de um LLM, que então geraria a resposta final\n"
        "usando este contexto."
    )
