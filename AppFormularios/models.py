import os
from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from reportlab.platypus import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from PIL import Image as PilImage
import io

# Create your models here.
def upload_to_inscripcionAFIP(instance, filename):
    base, extension = os.path.splitext(filename)
    return 'ReempadronamientoFisica/{0}{1}-{2}-{3}-InscripcionAFIP{4}'.format(instance.apellido, instance.nombre, instance.nombreFantasia, instance.cuit, extension)

def upload_to_reempadronamiento_fisica(instance, filename):
    base, extension = os.path.splitext(filename)
    return 'ReempadronamientoFisica/{0}{1}-{2}-{3}-Final{4}'.format(instance.apellido, instance.nombre, instance.nombreFantasia, instance.cuit, extension)

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
    cuit = models.CharField(max_length=20)
    ingresosBrutos = models.CharField(max_length=20)
    convenioMultilateral = models.CharField(max_length=20, blank=True, null=True)
    domicilioFiscal = models.CharField(max_length=50)
    localidad = models.CharField(max_length=50)
    codigoPostal = models.IntegerField()
    provincia = models.CharField(max_length=50)
    domicilioComercial = models.CharField(max_length=50)
    email = models.EmailField()
    telefonoComercial = models.CharField(max_length=20)
    telefonoTitular = models.CharField(max_length=20)
    superficieLocal = models.IntegerField()
    superficieDeposito = models.IntegerField(blank=True, null=True)
    actividadPrincipal = models.CharField(max_length=100)
    rubro2 = models.CharField(max_length=100, blank=True, null=True)
    rubro3 = models.CharField(max_length=100, blank=True, null=True)
    rubro4 = models.CharField(max_length=100, blank=True, null=True)
    sucursal = models.BooleanField(default=False)
    domicilioSucursal = models.CharField(max_length=50, blank=True, null=True)
    inscripcionAFIP = models.FileField(upload_to=upload_to_inscripcionAFIP, validators=[FileExtensionValidator(['pdf'], message="ERROR, el archivo tiene que estar en formato PDF.")])
    pdf = models.FileField(upload_to=upload_to_reempadronamiento_fisica, blank=True, null=True)

    def __str__(self):
        return self.apellido + ", " + self.nombre + " - " + self.nombreFantasia + " - " + str(self.cuit)
    
    def save(self, *args, **kwargs):
        # Si el objeto ya tiene un PDF, lo elimina
        if self.pdf and os.path.isfile(self.pdf.path):
            default_storage.delete(self.pdf.path)

        # Crea un objeto de archivo en memoria
        buffer = io.BytesIO()

        # Crea el archivo PDF, usando el objeto como su "archivo"
        p = canvas.Canvas(buffer)

        # --- Dibuja la imagen de la portada ---
        # Carga la imagen de la portada
        portada = PilImage.open('img/formulario_encabezado.png')
        # Ajusta el tamaño de la imagen para que ocupe todo el ancho de la hoja
        portada_width = A4[0]
        portada_height = portada.size[1] * portada_width / portada.size[0]  # Calcula la altura proporcional
        # Dibuja la imagen de la portada
        p.drawImage('img/formulario_encabezado.png', 0, 740, width=portada_width, height=portada_height)

        # --- Dibuja el texto del formulario ---
        # Dibuja el título del formulario y lo subraya
        title = "FORMULARIO DE REEMPADRONAMIENTO DE COMERCIOS - INDUSTRIAS - SERVICIOS"
        p.drawString(50, 710, title)
        title_width = p.stringWidth(title, "Helvetica", 12)
        p.line(50, 705, 50 + title_width, 705)

        # Registra una fuente TTF y úsala para el texto en negrita
        pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
        p.setFont('VeraBd', 12)

        # Dibuja "Apellido y nombre:" en negrita y luego el valor en texto normal
        label = "Apellido y nombre: "
        p.setFont('Helvetica-Bold', 12)
        p.drawString(50, 670, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        p.drawString(80 + length, 670, self.apellido + " " + self.nombre)

        # Dibuja "Nombre de fantasía:" en negrita y luego el valor en texto normal
        label = "Nombre de fantasía: "
        p.setFont('Helvetica-Bold', 12)
        p.drawString(50, 650, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        p.drawString(82 + length, 650, self.nombreFantasia)
        
        label = "CUIT: "
        p.setFont('Helvetica-Bold', 12)
        p.drawString(50, 630, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        p.drawString(100 + length, 630, self.cuit)
        
        label = "Insc. Ingresos Brutos: "
        p.setFont('Helvetica-Bold', 12)
        p.drawString(50, 610, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        p.drawString(61 + length, 610, self.ingresosBrutos)
        
        label = "Convenio Multilateral: "
        p.setFont('Helvetica-Bold', 12)
        p.drawString(50, 590, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        p.drawString(61 + length, 590, self.convenioMultilateral)

        # Agrega más campos aquí...

        # Cierra el objeto PDF limpiamente.
        p.showPage()
        p.save()

        # Obtiene el valor del archivo PDF que acaba de generar.
        pdf = buffer.getvalue()
        buffer.close()

        # Guarda el PDF en el campo 'pdf' del modelo.
        self.pdf.save('output.pdf', ContentFile(pdf), save=False)

        # Actualiza el estado
        estado = Estado.objects.get(nombre='Pendiente')
        self.estado = estado

        super().save(*args, **kwargs)
