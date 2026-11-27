from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Paciente


class PacienteTests(TestCase):
    def setUp(self):
        self.dados = {
            'nome': 'Ana da Silva',
            'email': 'ana@example.com',
            'telefone': '(11) 99999-0000',
            'data_nascimento': '2000-05-10',
        }

    def test_pagina_inicial_e_listagem(self):
        Paciente.objects.create(nome='Ana', email='ana@example.com')
        resposta = self.client.get(reverse('pacientes'))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'Gerenciamento de pacientes')
        self.assertContains(resposta, 'Ana')

    def test_cadastrar_paciente(self):
        resposta = self.client.post(reverse('pacientes'), self.dados)
        self.assertRedirects(resposta, reverse('pacientes'))
        self.assertEqual(Paciente.objects.count(), 1)

    def test_campos_obrigatorios(self):
        resposta = self.client.post(reverse('pacientes'), {})
        self.assertEqual(resposta.status_code, 200)
        self.assertTrue(resposta.context['form'].errors)
        self.assertEqual(Paciente.objects.count(), 0)

    def test_email_duplicado(self):
        Paciente.objects.create(nome='Outro', email='ana@example.com')
        resposta = self.client.post(reverse('pacientes'), self.dados)
        self.assertContains(resposta, 'Este e-mail já está cadastrado')
        self.assertEqual(Paciente.objects.count(), 1)

    def test_email_duplicado_na_edicao(self):
        Paciente.objects.create(nome='Ana', email='ana@example.com')
        outro = Paciente.objects.create(nome='Bruno', email='bruno@example.com')
        resposta = self.client.post(reverse('editar_paciente', args=[outro.pk]), {**self.dados, 'nome': 'Bruno'})
        self.assertContains(resposta, 'Este e-mail já está cadastrado')

    def test_editar_paciente(self):
        paciente = Paciente.objects.create(nome='Antes', email='antes@example.com')
        resposta = self.client.post(reverse('editar_paciente', args=[paciente.pk]), {**self.dados, 'nome': 'Depois'})
        self.assertRedirects(resposta, reverse('pacientes'))
        paciente.refresh_from_db()
        self.assertEqual(paciente.nome, 'Depois')

    def test_excluir_apenas_por_post(self):
        paciente = Paciente.objects.create(nome='Excluir', email='excluir@example.com')
        url = reverse('excluir_paciente', args=[paciente.pk])
        self.assertEqual(self.client.get(url).status_code, 405)
        self.assertRedirects(self.client.post(url), reverse('pacientes'))
        self.assertFalse(Paciente.objects.filter(pk=paciente.pk).exists())

    def test_busca(self):
        Paciente.objects.create(nome='Maria Souza', email='maria@example.com')
        Paciente.objects.create(nome='João Lima', email='joao@example.com')
        resposta = self.client.get(reverse('pacientes'), {'busca': 'maria'})
        self.assertContains(resposta, 'Maria Souza')
        self.assertNotContains(resposta, 'João Lima')

    def test_data_nascimento_nao_pode_ser_futura(self):
        dados = {**self.dados, 'data_nascimento': (timezone.localdate().replace(year=timezone.localdate().year + 1)).isoformat()}
        resposta = self.client.post(reverse('pacientes'), dados)
        self.assertContains(resposta, 'não pode ser futura')
        self.assertEqual(Paciente.objects.count(), 0)
