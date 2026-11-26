from django.test import TestCase
from django.utils import timezone
from datetime import timedelta,time
from .models import Paciente,Consulta,Medicamento
class DashboardTests(TestCase):
    def test_vazio(self):
        self.assertContains(self.client.get('/'),'Nenhuma consulta agendada.')
    def test_dados_do_paciente(self):
        p=Paciente.objects.create(nome='Maria',email='m@example.com')
        outro=Paciente.objects.create(nome='João',email='j@example.com')
        hoje=timezone.localdate()
        Consulta.objects.create(paciente=p,medico='Médico A',especialidade='Cardiologia',clinica='Clínica A',data=hoje+timedelta(days=1),horario=time(10))
        Consulta.objects.create(paciente=outro,medico='Médico B',especialidade='Outra especialidade',clinica='Clínica B',data=hoje,horario=time(11))
        Medicamento.objects.create(paciente=p,nome='Exemplo A',dosagem='Fictícia',horario=time(8),data_inicio=hoje)
        r=self.client.get('/',{'paciente':p.pk})
        self.assertContains(r,'Cardiologia')
        self.assertContains(r,'Exemplo A')
        self.assertNotContains(r,'Outra especialidade')
    def test_filtro_agenda_e_consultas(self):
        p=Paciente.objects.create(nome='Teste',email='teste@example.com')
        hoje=timezone.localdate()
        futuro=hoje+timedelta(days=3)
        Consulta.objects.create(paciente=p,medico='Cancelado',especialidade='Cancelada teste',clinica='Teste',data=futuro,horario=time(9),status='cancelada')
        Medicamento.objects.create(paciente=p,nome='Agenda futura',dosagem='Fictícia',horario=time(8),data_inicio=futuro,data_fim=futuro)
        r=self.client.get('/',{'paciente':p.pk})
        self.assertNotContains(r,'Cancelada teste')
        self.assertNotContains(r,'Agenda futura')
        self.assertContains(self.client.get('/',{'paciente':p.pk,'dia':futuro.isoformat()}),'Agenda futura')

    def test_estilo_incorporado(self):
        r=self.client.get('/')
        self.assertContains(r,'<style>')
        self.assertContains(r,'grid-template-columns')
