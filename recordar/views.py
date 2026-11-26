from django.utils.dateparse import parse_date
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Q
from .models import Paciente, Consulta, Medicamento

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

from django.shortcuts import redirect
from django.db import IntegrityError, transaction
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import ConsultaForm

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
