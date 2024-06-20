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

class Person(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        abstract = True  # Define esta clase como abstracta

    def __str__(self):
        return self.username


class User(Person):
    uid = models.CharField(max_length=255, unique=True, primary_key=True)
    programa = models.CharField(max_length=255)
    codigo_estudiantil = models.PositiveIntegerField(default=0, unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)  # Campo nuevo opcional
    photo_url = models.URLField(max_length=500, null=True, blank=True)

    # Campos para rastrear si han sido editados
    codigo_estudiantil_editado = models.BooleanField(default=False)
    programa_editado = models.BooleanField(default=False)
    telefono_editado = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    

class Admin(Person):
    
    def __str__(self):
        return self.username

class Reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, to_field='uid')
    fecha = models.DateField()
    hora = models.TimeField()
    cantidad_horas = models.PositiveIntegerField(default=1)
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
    cantidad_horas = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.usuario.nombre} - {self.cantidad_horas} hora(s) el {self.fecha} a las {self.hora}'
    
class Membresia(models.Model):
    id_membresia = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, to_field='uid')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return f'{self.usuario.nombre} - {self.fecha_inicio} a {self.fecha_fin}'
    

