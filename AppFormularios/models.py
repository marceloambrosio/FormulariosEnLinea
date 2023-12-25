import os
from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone

# Create your models here.
def upload_to_inscripcionAFIP(instance, filename):
    base, extension = os.path.splitext(filename)
    return 'ReempadronamientoFisica/{0}{1}-{2}-{3}-InscripcionAFIP{4}'.format(instance.apellido, instance.nombre, instance.nombreFantasia, instance.cuit, extension)

class ReempadronamientoComercioFisica(models.Model):
    fecha = models.DateField(default=timezone.now)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    nombreFantasia = models.CharField(max_length=50)
    cuit = models.IntegerField()
    ingresosBrutos = models.IntegerField()
    convenioMultilateral = models.IntegerField(Blank=True, null=True)
    numero = models.IntegerField(Blank=True, null=True)
    folio = models.IntegerField(Blank=True, null=True)
    libro = models.IntegerField(Blank=True, null=True)
    tema = models.CharField(max_length=50, Blank=True, null=True)
    anio = models.IntegerField(Blank=True, null=True)
    domicilioFiscal = models.CharField(max_length=50)
    localidad = models.CharField(max_length=50)
    codigoPostal = models.IntegerField()
    provincia = models.CharField(max_length=50)
    domicilioComercial = models.CharField(max_length=50)
    email = models.EmailField()
    telefonoComercial = models.IntegerField()
    telefonoTitular = models.IntegerField()
    superficieLocal = models.IntegerField()
    superficieDeposito = models.IntegerField(Blank=True, null=True)
    actividadPrincipal = models.CharField(max_length=100)
    rubro2 = models.CharField(max_length=100, Blank=True, null=True)
    rubro3 = models.CharField(max_length=100, Blank=True, null=True)
    rubro4 = models.CharField(max_length=100, Blank=True, null=True)
    sucursal = models.BooleanField()
    domicilioSucursal = models.CharField(max_length=50, Blank=True, null=True)
    inscripcionAFIP = models.FileField(upload_to=upload_to_inscripcionAFIP, validators=[FileExtensionValidator(['pdf'], message="ERROR, el archivo tiene que estar en formato PDF.")], blank=True, null=True)

    def __str__(self):
        return self.apellido + ", " + self.nombre + " - " + self.nombreFantasia + " - " + str(self.cuit)