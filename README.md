# Academia Corpo em Movimento

Sistema web em Django para a proprietária manter modalidades e turmas, com páginas públicas que consultam os dados cadastrados.

## Equipe

Nome da equipe: a preencher pelos integrantes.

## Requisitos

- Python 3
- Dependências listadas em `requirements.txt`

## Como rodar o projeto

No Windows, no diretório do projeto:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Acesse a página inicial em `http://127.0.0.1:8000/`, a grade em `http://127.0.0.1:8000/turmas/` e o painel em `http://127.0.0.1:8000/admin/`. No painel, cadastre e edite modalidades e turmas; a lista de turmas permite filtrar por modalidade e dia e pesquisar pelo instrutor.

O banco SQLite recebe as modalidades e turmas de exemplo na primeira migração. Para iniciar com um banco vazio, aplique as migrações e exclua os registros de exemplo pelo painel.

## Decisões

- O painel administrativo nativo do Django é usado para as operações de cadastro, edição, consulta, exclusão, filtros e busca.
- A grade pública mostra todas as turmas cadastradas, inclusive as que pertencem a uma modalidade inativa; somente modalidades ativas aparecem na página inicial.
- Modalidades com turmas não podem ser excluídas. Remova ou reassocie as turmas antes de excluir a modalidade.
- Horários são armazenados como hora e exibidos no formato de 24 horas. Os dias são opções fixas de segunda a sábado; vagas começam em 10 e não aceitam valores negativos.
- O levantamento não informou o endereço completo, o telefone nem o nome da equipe. O endereço provisório e o telefone informativo estão em `config/settings.py`; atualize-os com os dados reais antes de publicar.

## Diário de IA — 21/10/2026

- A IA foi utilizada para implementar os modelos Django, personalizar o painel administrativo, montar as páginas públicas e criar testes automatizados.
- Também foi utilizada para preparar migrações e documentação e para validar as regras de negócio com os testes do Django.
- A equipe deve revisar o código e substituir os dados de contato provisórios antes da publicação.
