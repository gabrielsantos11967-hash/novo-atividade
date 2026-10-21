from django import forms
from django.contrib import admin

from .models import Modalidade, Turma


class TurmaAdminForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = "__all__"
        widgets = {
            "horario": forms.TimeInput(format="%H:%M", attrs={"type": "time"}),
        }


@admin.register(Modalidade)
class ModalidadeAdmin(admin.ModelAdmin):
    list_display = ("nome", "ativa")
    list_filter = ("ativa",)
    search_fields = ("nome",)
    ordering = ("nome",)


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    form = TurmaAdminForm
    list_display = ("modalidade", "dia_semana", "horario", "instrutor", "vagas")
    list_filter = ("modalidade", "dia_semana")
    search_fields = ("instrutor",)
    ordering = ("dia_semana", "horario")


admin.site.site_header = "Academia Corpo em Movimento"
admin.site.site_title = "Painel administrativo"
admin.site.index_title = "Gerenciamento da academia"
