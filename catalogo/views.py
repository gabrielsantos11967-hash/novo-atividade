from django.conf import settings
from django.shortcuts import render

from .models import Modalidade, Turma


def inicio(request):
    modalidades = Modalidade.objects.filter(ativa=True)
    return render(
        request,
        "catalogo/inicio.html",
        {
            "nome_academia": settings.ACADEMIA_NOME,
            "endereco_academia": settings.ACADEMIA_ENDERECO,
            "telefone_academia": settings.ACADEMIA_TELEFONE,
            "modalidades": modalidades,
        },
    )


def grade_turmas(request):
    turmas = Turma.objects.select_related("modalidade").all()
    return render(request, "catalogo/turmas.html", {"turmas": turmas})
