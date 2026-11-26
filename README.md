# Recordar | Django

## Sobre o projeto

O Recordar é um sistema desenvolvido para auxiliar pacientes na organização de sua rotina de saúde, facilitando o acompanhamento de consultas, medicamentos e informações clínicas.

Esta versão foi desenvolvida utilizando Django para a atividade AVA2 — Implementação das telas do Projeto Integrador, com foco na integração entre interfaces, funcionalidades e banco de dados.

## Tecnologias utilizadas

- Python
- Django
- SQLite
- HTML5
- CSS3
- Django ORM
- Git e GitHub

## Divisão de responsabilidades

| Integrante | Tela | Responsabilidade |
|---|---|---|
| Gabrielle | Dashboard | Visualização das próximas consultas, agenda de medicamentos e filtros. |
| Beatriz | Consultas | Agendamento, listagem, cancelamento e validação de horários. |
| Andreza | Anamnese | Registro e consulta das informações clínicas do paciente. |
| Louise | Medicamentos | Cadastro, gerenciamento e visualização dos medicamentos. |
| Diógenes | Pacientes | Cadastro, consulta e gerenciamento dos pacientes. |

## Estrutura do projeto

- `config/` — Configurações gerais do Django.
- `recordar/` — Models, views, rotas e regras de negócio.
- `templates/` — Interfaces HTML.
- `static/` — Recursos visuais e arquivos estáticos.
- `manage.py` — Gerenciamento do projeto Django.
- `requirements.txt` — Dependências do projeto.
- `iniciar.bat` — Inicialização automatizada no Windows.
- `db.sqlite3` — Banco de dados local, gerado durante a configuração.

## Como executar o projeto

### 1. Clonar o repositório

`git clone https://github.com/gabriellemnunes/recordar-django.git`

### 2. Acessar a pasta

`cd recordar-django`

### 3. Executar o instalador

`.\iniciar.bat`

### 4. Acessar o sistema

http://127.0.0.1:8001/

## Banco de dados

O projeto utiliza SQLite integrado ao Django ORM para armazenamento e consulta das informações.

As entidades previstas são:

- Pacientes;
- Consultas;
- Medicamentos;
- Anamnese.

As informações são manipuladas por meio dos models e views do Django e apresentadas nas interfaces através dos templates.

Os dados utilizados para demonstração são fictícios e destinados exclusivamente a fins acadêmicos.

## Organização das branches

Cada integrante deverá desenvolver sua funcionalidade em uma branch individual.

- `gabi/dashboard`
- `bia/consultas`
- `andreza/anamnese`
- `louise/medicamentos`
- `diogenes/pacientes`

Após a implementação e validação das funcionalidades, as alterações deverão ser integradas à branch principal, preservando a estrutura compartilhada.

## Testes

Para executar os testes automatizados:

`python manage.py test`

Para verificar a configuração do Django:

`python manage.py check`

Cada integrante deverá validar sua funcionalidade antes de integrar suas alterações ao projeto principal.

## Entrega individual — AVA2

Cada integrante deverá enviar individualmente no Teams:

- Identificação da tela desenvolvida;
- Descrição da funcionalidade;
- Explicação da implementação e integração com o banco de dados;
- Capturas de tela demonstrando o funcionamento e os resultados.

**Prazo:** 28/11/2026, às 23h59.

## Status do projeto

Projeto acadêmico em desenvolvimento colaborativo. O dashboard foi demonstrado em execução, e as demais funcionalidades deverão ser integradas conforme a conclusão das tarefas individuais.

## Equipe

- Gabrielle
- Beatriz
- Andreza
- Louise
- Diógenes

Projeto Integrador — Análise e Desenvolvimento de Sistemas — 2026.
