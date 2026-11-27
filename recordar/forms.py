from django import forms
from django.utils import timezone
from .models import Consulta, Paciente

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

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'email', 'telefone', 'data_nascimento']
        labels = {
            'nome': 'Nome completo',
            'email': 'E-mail',
            'telefone': 'Telefone',
            'data_nascimento': 'Data de nascimento',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'pac-input', 'placeholder': 'Nome completo do paciente'}),
            'email': forms.EmailInput(attrs={'class': 'pac-input', 'placeholder': 'paciente@email.com'}),
            'telefone': forms.TextInput(attrs={'class': 'pac-input', 'placeholder': '(00) 00000-0000'}),
            'data_nascimento': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'pac-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_nascimento'].input_formats = ['%Y-%m-%d', '%d/%m/%Y']
        self.fields['nome'].required = True
        self.fields['email'].required = True

    def clean_nome(self):
        nome = self.cleaned_data['nome'].strip()
        if not nome:
            raise forms.ValidationError('Informe o nome do paciente.')
        return nome

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        pacientes = Paciente.objects.filter(email__iexact=email)
        if self.instance.pk:
            pacientes = pacientes.exclude(pk=self.instance.pk)
        if pacientes.exists():
            raise forms.ValidationError('Este e-mail já está cadastrado.')
        return email

    def clean_telefone(self):
        return self.cleaned_data.get('telefone', '').strip()

    def clean_data_nascimento(self):
        data_nascimento = self.cleaned_data.get('data_nascimento')
        if data_nascimento and data_nascimento > timezone.localdate():
            raise forms.ValidationError('A data de nascimento não pode ser futura.')
        return data_nascimento
