from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [('recordar', '0001_initial')]
    operations = [migrations.AddConstraint(model_name='consulta', constraint=models.UniqueConstraint(fields=['paciente', 'data', 'horario'], condition=models.Q(status='agendada'), name='horario_paciente_unico'))]
