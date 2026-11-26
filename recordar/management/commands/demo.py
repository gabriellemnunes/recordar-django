from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta,time
from recordar.models import Paciente, Consulta, Medicamento
class Command(BaseCommand):
    help = 'Cria dados fictícios para demonstração local.'
    def handle(self,*args,**options):
        p,_=Paciente.objects.get_or_create(email='maria@example.com',defaults={'nome':'Maria (demonstração)'})
        hoje=timezone.localdate()
        Consulta.objects.get_or_create(paciente=p,medico='Dr. Exemplo',data=hoje+timedelta(days=2),horario=time(10),defaults={'especialidade':'Clínica geral','clinica':'Clínica Exemplo'})
        Medicamento.objects.get_or_create(paciente=p,nome='Medicamento demonstrativo',defaults={'dosagem':'Dose fictícia','horario':time(8),'data_inicio':hoje})
        self.stdout.write(self.style.SUCCESS('Dados fictícios cadastrados.'))
