from django.db import models
class Paciente(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=30, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    def __str__(self): return self.nome
class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='consultas')
    medico = models.CharField(max_length=150)
    especialidade = models.CharField(max_length=100)
    clinica = models.CharField(max_length=150)
    data = models.DateField()
    horario = models.TimeField()
    status = models.CharField(max_length=15, choices=[('agendada','Agendada'),('cancelada','Cancelada')], default='agendada')
    class Meta:
        constraints = [models.UniqueConstraint(fields=['medico','data','horario'], condition=models.Q(status='agendada'), name='horario_medico_unico'), models.UniqueConstraint(fields=['paciente','data','horario'], condition=models.Q(status='agendada'), name='horario_paciente_unico')]
class Medicamento(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='medicamentos')
    nome = models.CharField(max_length=150)
    dosagem = models.CharField(max_length=100)
    horario = models.TimeField()
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
class Anamnese(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
    queixa_principal = models.TextField(blank=True)
    sintomas = models.TextField(blank=True)
    alergias = models.TextField(blank=True)
    condicoes_saude = models.TextField(blank=True)
    medicamentos_em_uso = models.TextField(blank=True)
