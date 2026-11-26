from datetime import date, time
from django.test import TestCase
from django.urls import reverse
from .models import Paciente, Medicamento


class MedicamentosTests(TestCase):
    def setUp(self):
        self.paciente = Paciente.objects.create(nome='Ana Teste', email='ana@example.com')
        self.outro = Paciente.objects.create(nome='Bruno Teste', email='bruno@example.com')
        self.dados = {
            'paciente': str(self.paciente.pk), 'nome': 'Remédio fictício',
            'dosagem': '1 comprimido', 'horario': '08:30',
            'data_inicio': '2026-11-26', 'data_fim': '2026-12-26',
        }

    def test_listagem_inicial(self):
        self.assertEqual(self.client.get(reverse('medicamentos')).status_code, 200)

    def test_cadastrar_no_sqlite(self):
        resposta = self.client.post(reverse('medicamento_novo'), self.dados)
        self.assertRedirects(resposta, reverse('medicamentos'))
        self.assertEqual(Medicamento.objects.count(), 1)
        self.assertEqual(Medicamento.objects.first().paciente, self.paciente)

    def test_editar(self):
        med = Medicamento.objects.create(paciente=self.paciente, nome='Antes', dosagem='10mg', horario=time(8), data_inicio=date(2026,11,26))
        self.client.post(reverse('medicamento_editar', args=[med.pk]), {**self.dados, 'nome': 'Depois'})
        med.refresh_from_db()
        self.assertEqual(med.nome, 'Depois')

    def test_excluir_apenas_por_post(self):
        med = Medicamento.objects.create(paciente=self.paciente, nome='Antes', dosagem='10mg', horario=time(8), data_inicio=date(2026,11,26))
        url = reverse('medicamento_excluir', args=[med.pk])
        self.assertEqual(self.client.get(url).status_code, 405)
        self.assertEqual(Medicamento.objects.count(), 1)
        self.assertRedirects(self.client.post(url), reverse('medicamentos'))
        self.assertEqual(Medicamento.objects.count(), 0)

    def test_validacao_periodo(self):
        resposta = self.client.post(reverse('medicamento_novo'), {**self.dados, 'data_fim': '2026-11-20'})
        self.assertContains(resposta, 'A data final não pode ser anterior')
        self.assertEqual(Medicamento.objects.count(), 0)

    def test_campos_obrigatorios(self):
        resposta = self.client.post(reverse('medicamento_novo'), {})
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(Medicamento.objects.count(), 0)

    def test_filtro_paciente(self):
        for paciente in (self.paciente, self.outro):
            Medicamento.objects.create(paciente=paciente, nome=paciente.nome, dosagem='1 comprimido', horario=time(9), data_inicio=date(2026,11,26))
        resposta = self.client.get(reverse('medicamentos'), {'paciente': self.paciente.pk})
        self.assertContains(resposta, 'Ana Teste')
        self.assertEqual(list(resposta.context['medicamentos'].values_list('paciente_id', flat=True)), [self.paciente.pk])

    def test_integracao_dashboard(self):
        Medicamento.objects.create(paciente=self.paciente, nome='Meu medicamento', dosagem='10 mg', horario=time(10), data_inicio=date(2020,1,1))
        self.assertContains(self.client.get(reverse('dashboard'), {'paciente': self.paciente.pk}), 'Meu medicamento')
