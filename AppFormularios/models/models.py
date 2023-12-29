from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class Estado(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre + ' (ID: ' + str(self.id) + ')'

@receiver(post_migrate)
def add_initial_data(sender, **kwargs):
    Estado.objects.get_or_create(nombre='Pendiente')
    Estado.objects.get_or_create(nombre='Cargado')
    Estado.objects.get_or_create(nombre='Rechazado')
    Estado.objects.get_or_create(nombre='Eliminado')