# Generated by Django 5.0.1 on 2024-01-22 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0008_alter_horariodia_dia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horariodia',
            name='dia',
            field=models.CharField(choices=[('Lunes', 'Lunes'), ('Martes', 'Martes'), ('Miércoles', 'Miércoles'), ('Jueves', 'Jueves'), ('Viernes', 'Viernes'), ('Sábado', 'Sábado'), ('Domingo', 'Domingo')], max_length=10, unique=True),
        ),
    ]
