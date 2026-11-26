from django import forms
from .models import Medicamento, Paciente


class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ['paciente', 'nome', 'dosagem', 'horario', 'data_inicio', 'data_fim']
        labels = {
            'paciente': 'Paciente', 'nome': 'Nome do medicamento',
            'dosagem': 'Dosagem', 'horario': 'Horário de uso',
            'data_inicio': 'Início do tratamento', 'data_fim': 'Fim do tratamento (opcional)',
        }
        widgets = {
            'paciente': forms.Select(attrs={'class': 'med-input'}),
            'nome': forms.TextInput(attrs={'class': 'med-input', 'placeholder': 'Ex.: Medicamento de demonstração'}),
            'dosagem': forms.TextInput(attrs={'class': 'med-input', 'placeholder': 'Ex.: 1 comprimido'}),
            'horario': forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'class': 'med-input'}),
            'data_inicio': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'med-input'}),
            'data_fim': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'med-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paciente'].queryset = Paciente.objects.order_by('nome')
        self.fields['horario'].input_formats = ['%H:%M', '%H:%M:%S']
        for field in ['data_inicio', 'data_fim']:
            self.fields[field].input_formats = ['%Y-%m-%d', '%d/%m/%Y']

    def clean(self):
        cleaned = super().clean()
        inicio, fim = cleaned.get('data_inicio'), cleaned.get('data_fim')
        if inicio and fim and fim < inicio:
            self.add_error('data_fim', 'A data final não pode ser anterior à data inicial.')
        return cleaned
