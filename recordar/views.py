from django.utils.dateparse import parse_date
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db import IntegrityError, transaction

from .models import Paciente, Consulta, Medicamento
from .forms import ConsultaForm, PacienteForm

def dashboard(request):
    pacientes = Paciente.objects.order_by('nome')
    paciente = get_object_or_404(Paciente, pk=request.GET['paciente']) if request.GET.get('paciente','').isdigit() else pacientes.first()
    hoje = timezone.localdate()
    try:
        dia = parse_date(request.GET.get("dia", "")) or hoje
    except ValueError:
        dia = hoje
    consultas = Consulta.objects.none()
    medicamentos = Medicamento.objects.none()
    if paciente:
        consultas = paciente.consultas.filter(status='agendada', data__gte=hoje).order_by('data','horario')
        medicamentos = paciente.medicamentos.filter(data_inicio__lte=dia).filter(Q(data_fim__isnull=True)|Q(data_fim__gte=dia)).order_by('horario')
    return render(request,'dashboard.html',{'pacientes':pacientes,'paciente':paciente,'consultas':consultas,'medicamentos':medicamentos,'hoje':hoje,'dia':dia})

def modulo(request, modulo):
    return render(request,'pendente.html',{'modulo':modulo})

def consultas(request):
    form = ConsultaForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        try:
            with transaction.atomic():
                form.save()
        except IntegrityError:
            form.add_error('horario', 'Horário indisponível. Escolha outro.')
        else:
            messages.success(request, 'Consulta agendada com sucesso.')
            return redirect('consultas')
    lista = Consulta.objects.select_related('paciente').order_by('-data', '-horario')
    return render(request, 'consultas.html', {'form': form, 'consultas': lista})

@require_POST
def cancelar_consulta(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    Consulta.objects.filter(pk=consulta.pk, status='agendada').update(status='cancelada')
    messages.success(request, 'Consulta cancelada.')
    return redirect('consultas')

def pacientes(request):
    form = PacienteForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        paciente = form.save()
        messages.success(request, f'Paciente {paciente.nome} cadastrado com sucesso.')
        return redirect('pacientes')
    busca = request.GET.get('busca', '').strip()
    lista = Paciente.objects.all().order_by('nome')
    if busca:
        lista = lista.filter(Q(nome__icontains=busca) | Q(email__icontains=busca))
    return render(request, 'pacientes.html', {'form': form, 'pacientes': lista, 'busca': busca})

def editar_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    form = PacienteForm(request.POST or None, instance=paciente)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Paciente {paciente.nome} atualizado com sucesso.')
        return redirect('pacientes')
    return render(request, 'editar_paciente.html', {'form': form, 'paciente': paciente})

@require_POST
def excluir_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    nome_paciente = paciente.nome
    paciente.delete()
    messages.success(request, f'Paciente {nome_paciente} excluído com sucesso.')
    return redirect('pacientes')
