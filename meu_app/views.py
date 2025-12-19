from django.shortcuts import render

import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings

HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

HEADERS = {
    "Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}",
    "Content-Type": "application/json"
}

def gerador(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 300
        }
    }

    response = requests.post(
        HUGGINGFACE_API_URL,
        headers=HEADERS,
        json=payload,
        timeout=60
    )

    return response.json()

@api_view(["POST"])
def gerar_relatorio_aluno(request):
    dados = request.data

    prompt = f"""
    Crie um relatório pedagógico detalhado para um aluno.

    Nome do aluno: {dados.get("nome")}
    curso: {dados.get("curso")}
    Notas: {dados.get("notas")}
    presenca: {dados.get("presenca")}

    O relatório deve:
    - Avaliar o desempenho académico
    - Comentar a assiduidade
    - Indicar pontos fortes
    - Indicar pontos a melhorar
    - Usar linguagem formal e clara
    """

    resultado = gerador(prompt)

    if isinstance(resultado, list):
        relatorio = resultado[0].get("generated_text", "")
    elif isinstance(resultado, dict):
        relatorio = resultado.get("generated_text", "")
    else:
        relatorio = str(resultado)

    return Response({"relatorio": relatorio})

