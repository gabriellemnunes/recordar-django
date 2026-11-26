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
