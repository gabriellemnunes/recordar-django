from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms_medicamentos import MedicamentoForm
from .models import Medicamento, Paciente


def medicamentos_lista(request):
    pacientes = Paciente.objects.order_by('nome')
    selecionado = request.GET.get('paciente', '').strip()
    paciente = get_object_or_404(Paciente, pk=selecionado) if selecionado.isdigit() else None
    medicamentos = Medicamento.objects.select_related('paciente').order_by('horario', 'nome')
    if paciente:
        medicamentos = medicamentos.filter(paciente=paciente)
    busca = request.GET.get('busca', '').strip()
    if busca:
        medicamentos = medicamentos.filter(Q(nome__icontains=busca) | Q(dosagem__icontains=busca))
    return render(request, 'medicamentos.html', {
        'medicamentos': medicamentos, 'pacientes': pacientes,
        'paciente': paciente, 'busca': busca,
    })


def medicamento_criar(request):
    form = MedicamentoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Medicamento cadastrado com sucesso.')
        return redirect('medicamentos')
    return render(request, 'medicamento_form.html', {'form': form, 'edicao': False})


def medicamento_editar(request, pk):
    medicamento = get_object_or_404(Medicamento, pk=pk)
    form = MedicamentoForm(request.POST or None, instance=medicamento)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Medicamento atualizado com sucesso.')
        return redirect('medicamentos')
    return render(request, 'medicamento_form.html', {'form': form, 'edicao': True, 'medicamento': medicamento})


@require_POST
def medicamento_excluir(request, pk):
    medicamento = get_object_or_404(Medicamento, pk=pk)
    medicamento.delete()
    messages.success(request, 'Medicamento excluído com sucesso.')
    return redirect('medicamentos')
