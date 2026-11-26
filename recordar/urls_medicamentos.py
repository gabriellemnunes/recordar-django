from django.urls import path
from .views_medicamentos import (
    medicamentos_lista, medicamento_criar, medicamento_editar, medicamento_excluir,
)

urlpatterns = [
    path('', medicamentos_lista, name='medicamentos'),
    path('novo/', medicamento_criar, name='medicamento_novo'),
    path('<int:pk>/editar/', medicamento_editar, name='medicamento_editar'),
    path('<int:pk>/excluir/', medicamento_excluir, name='medicamento_excluir'),
]
