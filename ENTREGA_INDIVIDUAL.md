# AVA2 – Recordar
Integrante: Gabrielle Mendes
Tela: Dashboard do paciente

## Funcionalidade
A tela inicial permite consultar próximas consultas agendadas e a agenda de medicamentos de um paciente de demonstração. É possível selecionar outro dia para consultar a agenda.

## Implementação e banco de dados
A rota inicial direciona à view dashboard. A view utiliza o Django ORM para consultar os models Paciente, Consulta e Medicamento no SQLite. As consultas agendadas são filtradas pela data atual e pelo paciente. Os medicamentos são filtrados pelo período de utilização e ordenados pelo horário. O template dashboard.html apresenta os resultados e utiliza o template base e o CSS próprio, criado para esta atividade.

## Evidências a inserir após executar
1. Captura do dashboard com consulta e medicamento cadastrados.
2. Captura da consulta de outro dia na agenda.
3. Opcional: terminal com resultado dos testes.

Dados exclusivamente fictícios. As demais telas são reservadas aos integrantes responsáveis. Os testes desta versão precisam ser executados localmente.
