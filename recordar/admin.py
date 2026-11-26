from django.contrib import admin
from .models import Paciente, Consulta, Medicamento, Anamnese
admin.site.register([Paciente, Consulta, Medicamento, Anamnese])
