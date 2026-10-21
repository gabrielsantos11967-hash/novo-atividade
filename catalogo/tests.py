from django.contrib.auth import get_user_model
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.urls import reverse

from .models import Modalidade, Turma


class TestCaseSemDadosDeExemplo(TestCase):
    def setUp(self):
        super().setUp()
        Turma.objects.all().delete()
        Modalidade.objects.all().delete()


class ModalidadeModelTests(TestCaseSemDadosDeExemplo):
    def test_nome_precisa_ser_unico(self):
        Modalidade.objects.create(nome="Pilates")
        duplicada = Modalidade(nome="Pilates")

        with self.assertRaises(ValidationError):
            duplicada.full_clean()

    def test_modalidade_com_turma_nao_pode_ser_excluida(self):
        modalidade = Modalidade.objects.create(nome="Pilates")
        Turma.objects.create(
            modalidade=modalidade,
            dia_semana=Turma.DiaSemana.SEGUNDA,
            horario="07:30",
            instrutor="Rafael",
        )

        with self.assertRaises(ProtectedError):
            modalidade.delete()


class TurmaModelTests(TestCaseSemDadosDeExemplo):
    def setUp(self):
        super().setUp()
        self.modalidade = Modalidade.objects.create(nome="Pilates")

    def test_vagas_tem_padrao_dez(self):
        turma = Turma.objects.create(
            modalidade=self.modalidade,
            dia_semana=Turma.DiaSemana.SEGUNDA,
            horario="07:30",
            instrutor="Rafael",
        )

        self.assertEqual(turma.vagas, 10)

    def test_vagas_nao_podem_ser_negativas(self):
        turma = Turma(
            modalidade=self.modalidade,
            dia_semana=Turma.DiaSemana.SEGUNDA,
            horario="07:30",
            instrutor="Rafael",
            vagas=-1,
        )

        with self.assertRaises(ValidationError):
            turma.full_clean()

    def test_dia_deve_ser_da_lista_permitida(self):
        turma = Turma(
            modalidade=self.modalidade,
            dia_semana=6,
            horario="07:30",
            instrutor="Rafael",
        )

        with self.assertRaises(ValidationError):
            turma.full_clean()


class PaginasPublicasTests(TestCaseSemDadosDeExemplo):
    def setUp(self):
        super().setUp()
        self.pilates = Modalidade.objects.create(
            nome="Pilates",
            descricao="Solo e aparelhos, turmas pequenas",
        )
        self.musculacao = Modalidade.objects.create(
            nome="Musculação",
            descricao="Treino com pesos",
        )
        self.inativa = Modalidade.objects.create(
            nome="Natação",
            descricao="Piscina aquecida (em reforma)",
            ativa=False,
        )
        Turma.objects.create(
            modalidade=self.musculacao,
            dia_semana=Turma.DiaSemana.SEGUNDA,
            horario="19:00",
            instrutor="Carla",
            vagas=15,
        )
        Turma.objects.create(
            modalidade=self.pilates,
            dia_semana=Turma.DiaSemana.SEGUNDA,
            horario="07:30",
            instrutor="Rafael",
            vagas=8,
        )
        Turma.objects.create(
            modalidade=self.inativa,
            dia_semana=Turma.DiaSemana.TERCA,
            horario="08:00",
            instrutor="Ana",
            vagas=10,
        )

    def test_inicio_mostra_dados_da_academia_e_modalidades_ativas(self):
        response = self.client.get(reverse("catalogo:inicio"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Academia Corpo em Movimento")
        self.assertContains(response, "Caruaru - PE")
        self.assertContains(response, "Telefone não informado")
        self.assertContains(response, "Solo e aparelhos, turmas pequenas")
        self.assertNotContains(response, "Piscina aquecida")
        self.assertContains(response, reverse("catalogo:turmas"))

    def test_grade_mostra_todas_as_turmas_em_ordem_de_dia_e_horario(self):
        response = self.client.get(reverse("catalogo:turmas"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Modalidade")
        self.assertContains(response, "Instrutor")
        self.assertContains(response, "Vagas")
        self.assertContains(response, "Natação")
        self.assertContains(response, "07:30")
        self.assertContains(response, "19:00")
        self.assertContains(response, reverse("catalogo:inicio"))
        self.assertLess(
            response.content.index(b"Rafael"),
            response.content.index(b"Carla"),
        )


class PainelAdministrativoTests(TestCaseSemDadosDeExemplo):
    def setUp(self):
        super().setUp()
        user_model = get_user_model()
        self.admin = user_model.objects.create_superuser(
            username="proprietaria",
            email="proprietaria@example.com",
            password="senha-de-teste-segura",
        )
        self.client.force_login(self.admin)
        self.modalidade = Modalidade.objects.create(nome="Pilates")
        self.turma = Turma.objects.create(
            modalidade=self.modalidade,
            dia_semana=Turma.DiaSemana.SEGUNDA,
            horario="07:30",
            instrutor="Rafael",
            vagas=8,
        )

    def test_lista_de_turmas_tem_colunas_e_filtros(self):
        outra_modalidade = Modalidade.objects.create(nome="Natação")
        Turma.objects.create(
            modalidade=outra_modalidade,
            dia_semana=Turma.DiaSemana.TERCA,
            horario="08:00",
            instrutor="Ana",
            vagas=10,
        )
        response = self.client.get(
            reverse("admin:catalogo_turma_changelist"),
            {
                "modalidade__id__exact": self.modalidade.pk,
                "dia_semana__exact": Turma.DiaSemana.SEGUNDA,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Modalidade")
        self.assertContains(response, "Dia da semana")
        self.assertContains(response, "Horário")
        self.assertContains(response, "Instrutor")
        self.assertContains(response, "Vagas")
        self.assertEqual(
            list(response.context["cl"].result_list),
            [self.turma],
        )
        self.assertEqual(
            admin.site._registry[Turma].list_filter,
            ("modalidade", "dia_semana"),
        )

    def test_busca_turmas_pelo_instrutor(self):
        response = self.client.get(
            reverse("admin:catalogo_turma_changelist"),
            {"q": "Rafael"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rafael")
        self.assertContains(response, "07:30")

    def test_painel_de_modalidades_filtra_ativas(self):
        response = self.client.get(
            reverse("admin:catalogo_modalidade_changelist"),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ativa__exact")
