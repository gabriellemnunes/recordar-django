from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('consultas/', views.consultas, name='consultas'),
    path('consultas/<int:pk>/cancelar/', views.cancelar_consulta, name='cancelar_consulta'),
    path('medicamentos/', include('recordar.urls_medicamentos')),
    path('anamnese/', views.modulo, {'modulo': 'Anamnese'}, name='anamnese'),
    path('pacientes/', views.modulo, {'modulo': 'Pacientes'}, name='pacientes'),
]
