import os
from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from reportlab.lib.pagesizes import A4
from PIL import Image as PilImage
from PyPDF2 import PdfReader, PdfWriter
from .models import Estado
from .uploaders import upload_to_inscripcionAFIP_fisica, upload_to_reempadronamiento_fisica
import io

# Create your models here.
class ReempadComercioFisica(models.Model):
    codigo_identificacion = models.CharField(max_length=20, blank=True, null=True)
    fecha = models.DateField(default=timezone.now, blank=True, null=True)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
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
    inscripcionAFIP = models.FileField(upload_to=upload_to_inscripcionAFIP_fisica, validators=[FileExtensionValidator(['pdf'], message="ERROR, el archivo tiene que estar en formato PDF.")])
    pdf = models.FileField(upload_to=upload_to_reempadronamiento_fisica, blank=True, null=True)
    finalizado = models.BooleanField(default=False)

    def __str__(self):
        return self.apellido + ", " + self.nombre + " - " + self.nombreFantasia + " - " + str(self.cuit)
    
    def save(self, *args, **kwargs):
        # Actualiza el estado
        if self.id is None:
            estado = Estado.objects.get(nombre='Pendiente')
            self.estado = estado

        # Genera el codigo_identificacion después de guardar el objeto
        if self.codigo_identificacion is None:
            self.codigo_identificacion = 'RMF' + str(self.id).zfill(6)

        # Guarda el objeto, lo que debería almacenar el archivo inscripcionAFIP
        super().save(*args, **kwargs)

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
        
        subtitle = "PERSONAS FISICAS"
        p.drawString(235, 688, subtitle)
        subtitle_width = p.stringWidth(subtitle, "Helvetica-Bold", 12)
        p.line(235, 683, 235 + subtitle_width, 683)

        # Registra una fuente TTF y úsala para el texto en negrita
        pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
        p.setFont('VeraBd', 12)

        # Dibuja "Apellido y nombre:" en negrita y luego el valor en texto normal
        label = "Apellido y nombre: "
        p.setFont('Helvetica-Bold', 12)
        p.drawString(50, 650, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        p.drawString(80 + length, 650, self.apellido + " " + self.nombre)

        # Dibuja "Nombre de fantasía:" en negrita y luego el valor en texto normal
        label = "Nombre de fantasía: "
        p.setFont('Helvetica-Bold', 12)
        p.drawString(50, 620, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        p.drawString(73 + length, 620, self.nombreFantasia)
        
        # Dibuja "CUIT:" en negrita y luego el valor en texto normal
        label = "CUIT: "
        p.setFont('Helvetica-Bold', 12)
        p.drawString(50, 590, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        p.drawString(70 + length, 590, self.cuit)

        # Calcula la nueva posición x para "Insc. Ingresos Brutos:"
        x = 70 + length + p.stringWidth(self.cuit, "Helvetica", 12) + 50

        # Dibuja "Insc. Ingresos Brutos:" en negrita y luego el valor en texto normal
        label = "Insc. Ingresos Brutos: "
        p.setFont('Helvetica-Bold', 12)
        p.drawString(x, 590, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        p.drawString(x + length + 20, 590, self.ingresosBrutos)
        
        if self.convenioMultilateral is not None:
            label = "Convenio Multilateral: "
            p.setFont('Helvetica-Bold', 12)
            p.drawString(50, 560, label)
            p.setFont('Helvetica', 12)
            length = p.stringWidth(label, "Helvetica-Bold", 12)
            p.drawString(61 + length, 560, self.convenioMultilateral)

        # Dibuja una línea horizontal que divida la hoja
        p.line(50, 535, A4[0] - 50, 535)
        
        label = "Domicilio Fiscal: "
        p.setFont('Helvetica-Bold', 12)
        p.drawString(50, 500, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        p.drawString(61 + length, 500, self.domicilioFiscal)
        
        # Dibuja "Localidad:" en negrita y luego el valor en texto normal
        label = "Localidad: "
        p.setFont('Helvetica-Bold', 12)
        p.drawString(50, 470, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        p.drawString(50 + length, 470, self.localidad)

        # Calcula la nueva posición x para "Cod. Postal:"
        x = 70 + length + p.stringWidth(self.localidad, "Helvetica", 12) + 50

        # Dibuja "Cod. Postal:" en negrita y luego el valor en texto normal
        label = "Cod. Postal: "
        p.setFont('Helvetica-Bold', 12)
        p.drawString(x, 470, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        p.drawString(x + length + 10, 470, str(self.codigoPostal))

        # Calcula la nueva posición x para "Provincia:"
        x = x + length + p.stringWidth(str(self.codigoPostal), "Helvetica", 12) + 50

        # Dibuja "Provincia:" en negrita y luego el valor en texto normal
        label = "Provincia: "
        p.setFont('Helvetica-Bold', 12)
        p.drawString(x, 470, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        p.drawString(x + length + 10, 470, self.provincia)
        
        label = "Domicilio Comercial: "
        p.setFont('Helvetica-Bold', 12)
        p.drawString(50, 440, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        p.drawString(61 + length, 440, self.domicilioComercial)
        
        label = "E-mail: "
        p.setFont('Helvetica-Bold', 12)
        p.drawString(50, 410, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        p.drawString(61 + length, 410, self.email)
        
        # Dibuja "Teléfono Comercial:" en negrita y luego el valor en texto normal
        label = "Teléfono Comercial: "
        p.setFont('Helvetica-Bold', 12)
        p.drawString(50, 380, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        p.drawString(60 + length, 380, self.telefonoComercial)

        # Calcula la nueva posición x para "Teléfono del Titular:"
        x = 40 + length + p.stringWidth(self.telefonoComercial, "Helvetica", 12) + 50

        # Dibuja "Teléfono del Titular:" en negrita y luego el valor en texto normal
        label = "Teléfono del Titular: "
        p.setFont('Helvetica-Bold', 12)
        p.drawString(x, 380, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        p.drawString(x + length + 10, 380, self.telefonoTitular)
        
        label = "Superficie del local en m2: "
        p.setFont('Helvetica-Bold', 12)
        p.drawString(50, 350, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        p.drawString(61 + length, 350, str(self.superficieLocal))
        
        if self.superficieDeposito is not None:
            label = "Superficie del depósito en m2: "
            p.setFont('Helvetica-Bold', 12)
            p.drawString(270, 350, label)
            p.setFont('Helvetica', 12)
            length = p.stringWidth(label, "Helvetica-Bold", 12)
            p.drawString(275 + length, 350, str(self.superficieDeposito))

        # Dibuja "Posee sucursal/es:" en negrita y luego el valor en texto normal
        label = "Posee sucursal/es: "
        p.setFont('Helvetica-Bold', 12)
        p.drawString(50, 320, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        if self.sucursal:
            p.drawString(55 + length, 320, "Sí")
        else:
            p.drawString(55 + length, 320, "No")

        # Calcula la nueva posición x para "Domicilio Sucursal:"
        x = 40 + length + p.stringWidth("Sí" if self.sucursal else "No", "Helvetica", 12) + 50

        # Dibuja "Domicilio Sucursal:" en negrita y luego el valor en texto normal
        if self.domicilioSucursal is not None:
            label = "Domicilio Sucursal: "
            p.setFont('Helvetica-Bold', 12)
            p.drawString(x, 320, label)
            p.setFont('Helvetica', 12)
            length = p.stringWidth(label, "Helvetica-Bold", 12)
            p.drawString(x + length + 20, 320, self.domicilioSucursal)
        
        # Dibuja una línea horizontal que divida la hoja
        p.line(50, 290, A4[0] - 50, 290)

        label = "Actividad Principal: "
        p.setFont('Helvetica-Bold', 12)
        p.drawString(50, 260, label)
        p.setFont('Helvetica', 12)
        length = p.stringWidth(label, "Helvetica-Bold", 12)
        p.drawString(61 + length, 260, self.actividadPrincipal)
        
        if self.rubro2 is not None:
            label = "Otros rubros de actividad: "
            p.setFont('Helvetica-Bold', 12)
            p.drawString(50, 230, label)
            p.setFont('Helvetica', 12)
            length = p.stringWidth(label, "Helvetica-Bold", 12)
            p.drawString(61 + length, 230,"- " + self.rubro2)
        
        if self.rubro3 is not None:
            p.setFont('Helvetica', 12)
            length = p.stringWidth(label, "Helvetica-Bold", 12)
            p.drawString(61 + length, 210,"- " + self.rubro3)
        
        if self.rubro4 is not None:
            p.setFont('Helvetica', 12)
            length = p.stringWidth(label, "Helvetica-Bold", 12)
            p.drawString(61 + length, 170,"- " + self.rubro4)
        
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

        # Asegúrate de que el archivo inscripcionAFIP exista y se pueda leer
        if os.path.isfile(self.inscripcionAFIP.path):
            # Añade el archivo inscripcionAFIP como una hoja adicional
            with open(self.inscripcionAFIP.path, 'rb') as f:
                output.add_page(PdfReader(f).pages[0])

        # Lee el contenido del nuevo archivo PDF
        with open('output.pdf', 'rb') as f:
            new_pdf = f.read()

        # Guarda el PDF en el campo 'pdf' del modelo.
        self.pdf.save('output.pdf', ContentFile(new_pdf), save=False)

        # Borra el archivo 'output.pdf'
        os.remove('output.pdf')

        super().save(update_fields=['codigo_identificacion', 'pdf'])