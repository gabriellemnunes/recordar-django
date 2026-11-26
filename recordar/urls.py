from django.urls import path
from . import views
urlpatterns = [path('',views.dashboard,name='dashboard'),path('consultas/',views.modulo,{'modulo':'Consultas'},name='consultas'),path('medicamentos/',views.modulo,{'modulo':'Medicamentos'},name='medicamentos'),path('anamnese/',views.modulo,{'modulo':'Anamnese'},name='anamnese'),path('pacientes/',views.modulo,{'modulo':'Pacientes'},name='pacientes')]
