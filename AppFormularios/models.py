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
from reportlab.lib.pagesizes import A4
from PIL import Image as PilImage
from PyPDF2 import PdfReader, PdfWriter
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

        # Establecer el título del PDF
        titulo = "Reempadronamiento-" + self.nombreFantasia + "-" + self.cuit
        p.setTitle(titulo)

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
        p.drawString(50, 640, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        p.drawString(73 + length, 640, self.nombreFantasia)
        
        # Dibuja "CUIT:" en negrita y luego el valor en texto normal
        label = "CUIT: "
        p.setFont('Helvetica-Bold', 12)
        p.drawString(50, 610, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        p.drawString(70 + length, 610, self.cuit)

        # Calcula la nueva posición x para "Insc. Ingresos Brutos:"
        x = 70 + length + p.stringWidth(self.cuit, "Helvetica", 12) + 50

        # Dibuja "Insc. Ingresos Brutos:" en negrita y luego el valor en texto normal
        label = "Insc. Ingresos Brutos: "
        p.setFont('Helvetica-Bold', 12)
        p.drawString(x, 610, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        p.drawString(x + length + 20, 610, self.ingresosBrutos)
        
        if self.convenioMultilateral is not None:
            label = "Convenio Multilateral: "
            p.setFont('Helvetica-Bold', 12)
            p.drawString(50, 580, label)
            p.setFont('Helvetica', 12)
            length = p.stringWidth(label, "Helvetica-Bold", 12)
            p.drawString(61 + length, 580, self.convenioMultilateral)

        # Dibuja una línea horizontal que divida la hoja
        p.line(50, 550, A4[0] - 50, 550)
        
        label = "Domicilio Fiscal: "
        p.setFont('Helvetica-Bold', 12)
        p.drawString(50, 510, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        p.drawString(61 + length, 510, self.domicilioFiscal)
        
        # Dibuja "Localidad:" en negrita y luego el valor en texto normal
        label = "Localidad: "
        p.setFont('Helvetica-Bold', 12)
        p.drawString(50, 480, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        p.drawString(50 + length, 480, self.localidad)

        # Calcula la nueva posición x para "Cod. Postal:"
        x = 70 + length + p.stringWidth(self.localidad, "Helvetica", 12) + 50

        # Dibuja "Cod. Postal:" en negrita y luego el valor en texto normal
        label = "Cod. Postal: "
        p.setFont('Helvetica-Bold', 12)
        p.drawString(x, 480, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        p.drawString(x + length + 10, 480, str(self.codigoPostal))

        # Calcula la nueva posición x para "Provincia:"
        x = x + length + p.stringWidth(str(self.codigoPostal), "Helvetica", 12) + 50

        # Dibuja "Provincia:" en negrita y luego el valor en texto normal
        label = "Provincia: "
        p.setFont('Helvetica-Bold', 12)
        p.drawString(x, 480, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        p.drawString(x + length + 10, 480, self.provincia)
        
        label = "Domicilio Comercial: "
        p.setFont('Helvetica-Bold', 12)
        p.drawString(50, 450, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        p.drawString(61 + length, 450, self.domicilioComercial)
        
        label = "E-mail: "
        p.setFont('Helvetica-Bold', 12)
        p.drawString(50, 420, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        p.drawString(61 + length, 420, self.email)
        
        # Dibuja "Teléfono Comercial:" en negrita y luego el valor en texto normal
        label = "Teléfono Comercial: "
        p.setFont('Helvetica-Bold', 12)
        p.drawString(50, 390, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        p.drawString(60 + length, 390, self.telefonoComercial)

        # Calcula la nueva posición x para "Teléfono del Titular:"
        x = 40 + length + p.stringWidth(self.telefonoComercial, "Helvetica", 12) + 50

        # Dibuja "Teléfono del Titular:" en negrita y luego el valor en texto normal
        label = "Teléfono del Titular: "
        p.setFont('Helvetica-Bold', 12)
        p.drawString(x, 390, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        p.drawString(x + length + 10, 390, self.telefonoTitular)
        
        label = "Superficie del local en m2: "
        p.setFont('Helvetica-Bold', 12)
        p.drawString(50, 360, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        p.drawString(61 + length, 360, str(self.superficieLocal))
        
        if self.superficieDeposito is not None:
            label = "Superficie del depósito en m2: "
            p.setFont('Helvetica-Bold', 12)
            p.drawString(50, 360, label)
            p.setFont('Helvetica', 12)
            length = p.stringWidth(label, "Helvetica-Bold", 12)
            p.drawString(61 + length, 360, str(self.superficieDeposito))

        # Dibuja "Posee sucursal/es:" en negrita y luego el valor en texto normal
        label = "Posee sucursal/es: "
        p.setFont('Helvetica-Bold', 12)
        p.drawString(50, 330, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        if self.sucursal:
            p.drawString(55 + length, 330, "Sí")
        else:
            p.drawString(55 + length, 330, "No")

        # Calcula la nueva posición x para "Domicilio Sucursal:"
        x = 40 + length + p.stringWidth("Sí" if self.sucursal else "No", "Helvetica", 12) + 50

        # Dibuja "Domicilio Sucursal:" en negrita y luego el valor en texto normal
        if self.domicilioSucursal is not None:
            label = "Domicilio Sucursal: "
            p.setFont('Helvetica-Bold', 12)
            p.drawString(x, 330, label)
            p.setFont('Helvetica', 12)
            length = p.stringWidth(label, "Helvetica-Bold", 12)
            p.drawString(x + length + 20, 330, self.domicilioSucursal)
        
        # Dibuja una línea horizontal que divida la hoja
        p.line(50, 300, A4[0] - 50, 300)

        label = "Actividad Principal: "
        p.setFont('Helvetica-Bold', 12)
        p.drawString(50, 270, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        p.drawString(61 + length, 270, self.actividadPrincipal)
        
        if self.rubro2 is not None:
            label = "Otros rubros de actividad: "
            p.setFont('Helvetica-Bold', 12)
            p.drawString(50, 240, label)
            p.setFont('Helvetica', 12)
            length = p.stringWidth(label, "Helvetica-Bold", 12)
            p.drawString(61 + length, 240,"- " + self.rubro2)
        
        if self.rubro3 is not None:
            p.setFont('Helvetica', 12)
            length = p.stringWidth(label, "Helvetica-Bold", 12)
            p.drawString(61 + length, 210,"- " + self.rubro3)
        
        if self.rubro4 is not None:
            p.setFont('Helvetica', 12)
            length = p.stringWidth(label, "Helvetica-Bold", 12)
            p.drawString(61 + length, 180,"- " + self.rubro4)
        
    # Cierra el objeto PDF limpiamente.
        p.showPage()
        p.save()

        # Obtiene el valor del archivo PDF que acaba de generar.
        pdf = buffer.getvalue()
        buffer.close()

        # Crea un objeto PdfWriter para escribir el PDF final
        output = PdfWriter()

        # Añade el PDF que acabas de generar
        output.add_page(PdfReader(io.BytesIO(pdf)).pages[0])

        # Añade el PDF existente
        output.add_page(PdfReader(open(self.inscripcionAFIP.path, 'rb')).pages[0])

        # Escribe el PDF final
        with open('output.pdf', 'wb') as f:
            output.write(f)

        # Lee el contenido del nuevo archivo PDF
        with open('output.pdf', 'rb') as f:
            new_pdf = f.read()

        # Guarda el PDF en el campo 'pdf' del modelo.
        self.pdf.save('output.pdf', ContentFile(new_pdf), save=False)

        # Actualiza el estado
        estado = Estado.objects.get(nombre='Pendiente')
        self.estado = estado

        super().save(*args, **kwargs)