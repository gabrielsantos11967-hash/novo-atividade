from django.core.validators import MinValueValidator
from django.db import models


class Modalidade(models.Model):
    nome = models.CharField("nome", max_length=100, unique=True)
    descricao = models.TextField("descrição", blank=True)
    ativa = models.BooleanField("ativa", default=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "modalidade"
        verbose_name_plural = "modalidades"

    def __str__(self):
        return self.nome


class Turma(models.Model):
    class DiaSemana(models.IntegerChoices):
        SEGUNDA = 0, "Segunda"
        TERCA = 1, "Terça"
        QUARTA = 2, "Quarta"
        QUINTA = 3, "Quinta"
        SEXTA = 4, "Sexta"
        SABADO = 5, "Sábado"

    modalidade = models.ForeignKey(
        Modalidade,
        on_delete=models.PROTECT,
        related_name="turmas",
        verbose_name="modalidade",
    )
    dia_semana = models.PositiveSmallIntegerField(
        "dia da semana",
        choices=DiaSemana.choices,
    )
    horario = models.TimeField("horário")
    instrutor = models.CharField("instrutor", max_length=100)
    vagas = models.PositiveIntegerField(
        "vagas",
        default=10,
        validators=[MinValueValidator(0)],
    )

    class Meta:
        ordering = ["dia_semana", "horario"]
        verbose_name = "turma"
        verbose_name_plural = "turmas"

    def __str__(self):
        return f"{self.modalidade} - {self.get_dia_semana_display()} {self.horario:%H:%M}"
