from django import forms
from django.utils import timezone
from .models import Consulta

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['paciente', 'medico', 'especialidade', 'clinica', 'data', 'horario']
        labels = {'medico': 'Médico', 'clinica': 'Clínica', 'horario': 'Horário'}
        widgets = {'data': forms.DateInput(attrs={'type': 'date'}), 'horario': forms.TimeInput(attrs={'type': 'time'})}

    def clean(self):
        dados = super().clean()
        data, horario, medico = (dados.get(k) for k in ('data', 'horario', 'medico'))
        agora = timezone.localtime()
        if data and horario and (data, horario) <= (agora.date(), agora.time()):
            self.add_error('data', 'Escolha uma data e um horário futuros.')
        if data and horario and medico and Consulta.objects.filter(medico__iexact=medico, data=data, horario=horario, status='agendada').exists():
            self.add_error('horario', 'Este médico já possui uma consulta neste horário.')
        paciente = dados.get("paciente")
        if data and horario and paciente and Consulta.objects.filter(paciente=paciente, data=data, horario=horario, status="agendada").exists():
            self.add_error("horario", "Este paciente já possui uma consulta neste horário.")
        return dados
