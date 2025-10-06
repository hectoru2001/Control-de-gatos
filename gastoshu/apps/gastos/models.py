from django.db import models
from django.utils import timezone
from datetime import date

# Create your models here.
class Gasto(models.Model):
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.fecha} - {self.monto} - {self.descripcion}"

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre
