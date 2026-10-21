from django.urls import path

from . import views

app_name = "catalogo"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("turmas/", views.grade_turmas, name="turmas"),
]
