from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from ..models import ReempadComercioFisica, ReempadComercioJuridica
from ..forms import ReempadComercioFisicaForm, ReempadComercioJuridicaForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from django.conf import settings


# Create your views here.

class FormularioCompletadoView(View):
    def get(self, request):
        return render(request, 'formulario_completado.html')

class ReempadComercioFisicaCreateView(CreateView):
    model = ReempadComercioFisica
    form_class = ReempadComercioFisicaForm
    template_name = 'reempadronamiento/reempad_comercio_fisica_create.html'

    def form_valid(self, form):
        # Guarda el objeto sin confirmar para obtener el id
        self.object = form.save()

        # Configura el servidor de correo electrónico (SMTP)
        smtp_server = settings.EMAIL_HOST
        smtp_port = settings.EMAIL_PORT
        smtp_user = settings.EMAIL_HOST_USER
        smtp_password = settings.EMAIL_HOST_PASSWORD

        # Crea el objeto de mensaje con formato HTML
        subject = "[Reempadronamiento] Confirmación de carga de archivo"
        message = f"""
¡Hola {self.object.nombre} {self.object.apellido}!
                
La carga del archivo se generó correctamente. Se adjunta el archivo PDF con los datos generados. 

En los próximos días le llegará otro email confirmando la carga del reempadronamiento en sistema.

Por favor, tenga en cuenta que este correo electrónico se genera automáticamente. Por lo tanto, le pedimos que no responda a este correo electrónico. 
Si tiene alguna pregunta o necesita ayuda, por favor, póngase en contacto con al correo rentas@villanueva.gob.ar

Su código de seguimiento es {self.object.codigo_identificacion}.

Ante cualquier inquietud, no dudes en comunicarte.
Saludos.

Municipalidad de Villa Nueva
"""

        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = smtp_user
        msg["To"] = self.object.email

        msg.attach(MIMEText(message, 'plain'))

        # Adjunta el archivo PDF
        with open(self.object.pdf.path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename= {}'.format(self.object.pdf.name))
            msg.attach(part)

        # Conéctate al servidor SMTP y envía el correo electrónico
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, [self.object.email], msg.as_string())
        server.quit()

        # Redirige a la página de éxito y pasa el objeto
        return render(self.request, 'formulario_completado.html', {'object': self.object})

class ReempadComercioFisicaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ReempadComercioFisica
    fields = ['estado', 'observaciones']
    permission_required = 'AppFormularios.change_ReempadComercioFisica'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            self.object.estado = form.cleaned_data.get('estado')
            self.object.observaciones = form.cleaned_data.get('observaciones')
            self.object.finalizado = True
            self.object.save()

            # Configura el servidor de correo electrónico (SMTP)
            smtp_server = settings.EMAIL_HOST
            smtp_port = settings.EMAIL_PORT
            smtp_user = settings.EMAIL_HOST_USER
            smtp_password = settings.EMAIL_HOST_PASSWORD

            # Crea el objeto de mensaje con formato HTML
            subject = "[Reempadronamiento] Actualización de estado"
            message = f"""
¡Hola {self.object.nombre} {self.object.apellido}! 

Tu formulario con codigo: {self.object.codigo_identificacion} se ha actualizado:

El estado de su reempadronamiento es {self.object.estado.nombre}. 
Observaciones: {self.object.observaciones}

Por favor, tenga en cuenta que este correo electrónico se genera automáticamente. Por lo tanto, le pedimos que no responda a este correo electrónico. 
Si tiene alguna pregunta o necesita ayuda, por favor, póngase en contacto con al correo rentas@villanueva.gob.ar.

Ante cualquier inquietud, no dudes en comunicarte.
Saludos.

Municipalidad de Villa Nueva
"""

            msg = MIMEMultipart()
            msg["Subject"] = subject
            msg["From"] = smtp_user
            msg["To"] = self.object.email

            msg.attach(MIMEText(message, 'plain'))

            # Conéctate al servidor SMTP y envía el correo electrónico
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, [self.object.email], msg.as_string())
            server.quit()

            return redirect('reempad_comercio_fisica_list')
        return redirect('reempad_comercio_fisica_list')

class ReempadComercioFisicaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ReempadComercioFisica
    template_name = 'reempadronamiento/reempad_comercio_fisica_list.html'
    permission_required = 'AppFormularios.view_ReempadComercioFisica'

class ReempadComercioJuridicaCreateView(CreateView):
    model = ReempadComercioJuridica
    form_class = ReempadComercioJuridicaForm
    template_name = 'reempadronamiento/reempad_comercio_juridica_create.html'
    
    def form_valid(self, form):
        # Guarda el objeto sin confirmar para obtener el id
        self.object = form.save()

        # Configura el servidor de correo electrónico (SMTP)
        smtp_server = settings.EMAIL_HOST
        smtp_port = settings.EMAIL_PORT
        smtp_user = settings.EMAIL_HOST_USER
        smtp_password = settings.EMAIL_HOST_PASSWORD

        # Crea el objeto de mensaje con formato HTML
        subject = "[Reempadronamiento] Confirmación de carga de archivo"
        message = f"""
¡Hola {self.object.razonSocial}!
                
La carga del archivo se generó correctamente. Se adjunta el archivo PDF con los datos generados. 

En los próximos días le llegará otro email confirmando la carga del reempadronamiento en sistema.

Por favor, tenga en cuenta que este correo electrónico se genera automáticamente. Por lo tanto, le pedimos que no responda a este correo electrónico. 
Si tiene alguna pregunta o necesita ayuda, por favor, póngase en contacto con al correo rentas@villanueva.gob.ar

Su código de seguimiento es {self.object.codigo_identificacion}.

Ante cualquier inquietud, no dudes en comunicarte.
Saludos.

Municipalidad de Villa Nueva
"""

        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = smtp_user
        msg["To"] = self.object.email

        msg.attach(MIMEText(message, 'plain'))

        # Adjunta el archivo PDF
        with open(self.object.pdf.path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename= {}'.format(self.object.pdf.name))
            msg.attach(part)

        # Conéctate al servidor SMTP y envía el correo electrónico
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, [self.object.email], msg.as_string())
        server.quit()

        # Redirige a la página de éxito y pasa el objeto
        return render(self.request, 'formulario_completado.html', {'object': self.object})
    
class ReempadComercioJuridicaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ReempadComercioJuridica
    fields = ['estado', 'observaciones']
    permission_required = 'AppFormularios.change_ReempadComercioJuridica'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            self.object.estado = form.cleaned_data.get('estado')
            self.object.observaciones = form.cleaned_data.get('observaciones')
            self.object.finalizado = True
            self.object.save()

                    # Configura el servidor de correo electrónico (SMTP)
            smtp_server = settings.EMAIL_HOST
            smtp_port = settings.EMAIL_PORT
            smtp_user = settings.EMAIL_HOST_USER
            smtp_password = settings.EMAIL_HOST_PASSWORD

            # Crea el objeto de mensaje con formato HTML
            subject = "[Reempadronamiento] Actualización de estado"
            message = f"""
¡Hola {self.object.nombre} {self.object.apellido}! 

Tu formulario con codigo {self.object.codigo_identificacion} se ha actualizado:

El estado de su reempadronamiento es {self.object.estado.nombre}. 
Observaciones: {self.object.observaciones}

Por favor, tenga en cuenta que este correo electrónico se genera automáticamente. Por lo tanto, le pedimos que no responda a este correo electrónico. 
Si tiene alguna pregunta o necesita ayuda, por favor, póngase en contacto con al correo rentas@villanueva.gob.ar.

Ante cualquier inquietud, no dudes en comunicarte.
Saludos.

Municipalidad de Villa Nueva
"""

            msg = MIMEMultipart()
            msg["Subject"] = subject
            msg["From"] = smtp_user
            msg["To"] = self.object.email

            msg.attach(MIMEText(message, 'plain'))

            # Conéctate al servidor SMTP y envía el correo electrónico
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, [self.object.email], msg.as_string())
            server.quit()

            return redirect('reempad_comercio_juridica_list')
        return redirect('reempad_comercio_juridica_list')
    
class ReempadComercioJuridicaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ReempadComercioJuridica
    template_name = 'reempadronamiento/reempad_comercio_juridica_list.html'
    permission_required = 'AppFormularios.view_ReempadComercioJuridica'