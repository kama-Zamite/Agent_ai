from django.urls import path
from .views import gerar_relatorio_aluno

urlpatterns = [
    path("relatorio-aluno/", gerar_relatorio_aluno),
]

