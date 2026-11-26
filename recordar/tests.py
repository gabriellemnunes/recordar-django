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

class ConsultaTests(TestCase):
    def setUp(self):
        self.p = Paciente.objects.create(nome='Paciente teste', email='consulta@example.com')
        self.dados = dict(paciente=self.p.pk, medico='Médico teste', especialidade='Clínica geral', clinica='Clínica teste', data=(timezone.localdate()+timedelta(days=2)).isoformat(), horario='10:00')

    def test_agendar(self):
        self.assertRedirects(self.client.post('/consultas/', self.dados), '/consultas/')
        self.assertEqual(Consulta.objects.get().paciente, self.p)
        self.assertContains(self.client.get('/consultas/'), 'Médico teste')

    def test_duplicidade(self):
        self.client.post('/consultas/', self.dados)
        self.assertContains(self.client.post('/consultas/', self.dados), 'já possui uma consulta')
        self.assertEqual(Consulta.objects.count(), 1)

    def test_cancelar_e_reagendar(self):
        self.client.post('/consultas/', self.dados)
        c = Consulta.objects.get()
        url = f'/consultas/{c.pk}/cancelar/'
        self.assertEqual(self.client.get(url).status_code, 405)
        self.assertRedirects(self.client.post(url), '/consultas/')
        c.refresh_from_db()
        self.assertEqual(c.status, 'cancelada')
        self.assertRedirects(self.client.post('/consultas/', self.dados), '/consultas/')
        self.assertEqual(Consulta.objects.filter(status='agendada').count(), 1)

    def test_data_passada(self):
        self.dados['data'] = (timezone.localdate()-timedelta(days=1)).isoformat()
        self.assertContains(self.client.post('/consultas/', self.dados), 'Escolha uma data')
        self.assertFalse(Consulta.objects.exists())

    def test_paciente_com_medicos_diferentes(self):
        self.client.post('/consultas/', self.dados)
        resposta = self.client.post('/consultas/', dict(self.dados, medico='Outro médico'))
        self.assertContains(resposta, 'Este paciente já possui uma consulta')
        self.assertEqual(Consulta.objects.count(), 1)

    def test_medico_com_pacientes_diferentes(self):
        self.client.post('/consultas/', self.dados)
        outro = Paciente.objects.create(nome='Outro', email='outro@example.com')
        self.assertContains(self.client.post('/consultas/', dict(self.dados, paciente=outro.pk)), 'Este médico já possui uma consulta')
        self.assertEqual(Consulta.objects.count(), 1)

    def test_cancelada_no_historico(self):
        self.client.post('/consultas/', self.dados)
        c = Consulta.objects.get()
        self.client.post(f'/consultas/{c.pk}/cancelar/')
        self.assertContains(self.client.get('/consultas/'), 'Cancelada')
        self.assertContains(self.client.get('/consultas/'), 'Médico teste')
