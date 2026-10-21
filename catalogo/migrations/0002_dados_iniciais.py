from datetime import time

from django.db import migrations


def criar_dados_iniciais(apps, schema_editor):
    Modalidade = apps.get_model("catalogo", "Modalidade")
    Turma = apps.get_model("catalogo", "Turma")
    banco = schema_editor.connection.alias

    modalidades = {
        "Musculação": Modalidade.objects.using(banco).create(
            nome="Musculação",
            descricao="Treino com pesos, acompanhamento individual",
        ),
        "Pilates": Modalidade.objects.using(banco).create(
            nome="Pilates",
            descricao="Solo e aparelhos, turmas pequenas",
        ),
        "Funcional": Modalidade.objects.using(banco).create(
            nome="Funcional",
            descricao="Circuito de alta intensidade",
        ),
        "Natação": Modalidade.objects.using(banco).create(
            nome="Natação",
            descricao="Piscina aquecida (em reforma)",
            ativa=False,
        ),
    }

    turmas = [
        ("Pilates", 0, time(7, 30), "Rafael", 8),
        ("Musculação", 0, time(19, 0), "Carla", 15),
        ("Funcional", 1, time(6, 30), "Diego", 12),
        ("Musculação", 1, time(18, 0), "Carla", 15),
        ("Pilates", 2, time(7, 30), "Rafael", 8),
        ("Funcional", 5, time(9, 0), "Diego", 20),
    ]
    Turma.objects.using(banco).bulk_create(
        [
            Turma(
                modalidade=modalidades[nome],
                dia_semana=dia,
                horario=horario,
                instrutor=instrutor,
                vagas=vagas,
            )
            for nome, dia, horario, instrutor, vagas in turmas
        ]
    )


class Migration(migrations.Migration):
    dependencies = [
        ("catalogo", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(criar_dados_iniciais, migrations.RunPython.noop),
    ]
