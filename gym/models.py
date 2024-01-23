from django.db import models
from datetime import datetime, timedelta, date

class Gym(models.Model):
    gym_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    aforo_max = models.PositiveIntegerField(default=0)

class HorarioDia(models.Model):
    DIA_CHOICES = [ ('Lunes', 'Lunes'),
                    ('Martes', 'Martes'),
                    ('Miércoles', 'Miércoles'),  
                    ('Jueves', 'Jueves'), 
                    ('Viernes', 'Viernes'),
                    ('Sábado', 'Sábado'),
                    ('Domingo','Domingo')]

    dia = models.CharField(max_length=10, choices=DIA_CHOICES, unique=True)
    closed = models.BooleanField(default=True)
    openTime = models.TimeField(null=True, blank=True)
    closeTime = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.dia} - {"Cerrado" if self.closed else f"{self.openTime} a {self.closeTime}"}'
    
class User(models.Model):
    uid = models.CharField(max_length=255, unique=True, primary_key=True)
    nombre = models.CharField(max_length=255)
    programa = models.CharField(max_length=255)
    codigo_estudiantil = models.IntegerField(default=0)
    email = models.EmailField(max_length=255)
    
    def __str__(self):
        return self.nombre

class Reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, to_field='uid')
    fecha = models.DateField()
    hora = models.TimeField()
    cantidad_horas = models.IntegerField(default=1)
    hora_fin = models.TimeField(blank=True, null=True)  # Nuevo campo

    def save(self, *args, **kwargs):
        # Calcular la hora de finalización al guardar la reserva
        if self.hora and self.cantidad_horas:
            hora_fin = (datetime.combine(date(1, 1, 1), self.hora) +
                        timedelta(hours=self.cantidad_horas)).time()
            self.hora_fin = hora_fin

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.usuario.nombre} - {self.cantidad_horas} hora(s) el {self.fecha} a las {self.hora}'

class Penalizacion(models.Model):
    id_penalizacion = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, to_field='uid')
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()

    def __str__(self):
        return f'{self.usuario.nombre} - {self.fecha_inicio} a {self.fecha_fin}'

class Asistencia(models.Model):
    id_asistencia = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, to_field='uid')
    fecha = models.DateField()
    hora = models.TimeField()
    cantidad_horas = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.usuario.nombre} - {self.cantidad_horas} hora(s) el {self.fecha} a las {self.hora}'