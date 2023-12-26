import os
from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.db.models.signals import post_migrate
from django.dispatch import receiver

# Create your models here.
def upload_to_inscripcionAFIP(instance, filename):
    base, extension = os.path.splitext(filename)
    return 'ReempadronamientoFisica/{0}{1}-{2}-{3}-InscripcionAFIP{4}'.format(instance.apellido, instance.nombre, instance.nombreFantasia, instance.cuit, extension)

class Estado(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

@receiver(post_migrate)
def add_initial_data(sender, **kwargs):
    Estado.objects.get_or_create(nombre='Pendiente')
    Estado.objects.get_or_create(nombre='Cargado')

class ReempadComercioFisica(models.Model):
    fecha = models.DateField(default=timezone.now, blank=True, null=True)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT, blank=True, null=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    nombreFantasia = models.CharField(max_length=50)
    cuit = models.IntegerField()
    ingresosBrutos = models.IntegerField()
    convenioMultilateral = models.IntegerField(blank=True, null=True)
    domicilioFiscal = models.CharField(max_length=50)
    localidad = models.CharField(max_length=50)
    codigoPostal = models.IntegerField()
    provincia = models.CharField(max_length=50)
    domicilioComercial = models.CharField(max_length=50)
    email = models.EmailField()
    telefonoComercial = models.IntegerField()
    telefonoTitular = models.IntegerField()
    superficieLocal = models.IntegerField()
    superficieDeposito = models.IntegerField(blank=True, null=True)
    actividadPrincipal = models.CharField(max_length=100)
    rubro2 = models.CharField(max_length=100, blank=True, null=True)
    rubro3 = models.CharField(max_length=100, blank=True, null=True)
    rubro4 = models.CharField(max_length=100, blank=True, null=True)
    sucursal = models.BooleanField(default=False)
    domicilioSucursal = models.CharField(max_length=50, blank=True, null=True)
    inscripcionAFIP = models.FileField(upload_to=upload_to_inscripcionAFIP, validators=[FileExtensionValidator(['pdf'], message="ERROR, el archivo tiene que estar en formato PDF.")], blank=True, null=True)

    def save(self, *args, **kwargs):
        estado = Estado.objects.get(nombre='Pendiente')
        self.estado = estado
        super().save(*args, **kwargs)

    def __str__(self):
        return self.apellido + ", " + self.nombre + " - " + self.nombreFantasia + " - " + str(self.cuit)