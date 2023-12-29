from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from .models import ReempadComercioFisica, ReempadComercioJuridica
from .forms import ReempadComercioFisicaForm, ReempadComercioJuridicaForm

# Create your views here.

class FormularioCompletadoView(View):
    def get(self, request):
        return render(request, 'formulario_completado.html')

class ReempadComercioFisicaCreateView(CreateView):
    model = ReempadComercioFisica
    form_class = ReempadComercioFisicaForm
    template_name = 'reempad_comercio_fisica_create.html'

    def form_valid(self, form):
        # Guarda el objeto sin confirmar para obtener el id
        self.object = form.save()

        # Redirige a la página de éxito y pasa el objeto
        return render(self.request, 'formulario_completado.html', {'object': self.object})

class ReempadComercioFisicaUpdateView(UpdateView):
    model = ReempadComercioFisica
    fields = ['estado', 'observaciones']
    success_url = reverse_lazy('reempad_comercio_fisica_list')

    def form_valid(self, form):
        form.instance.finalizado = True
        return redirect('reempad_comercio_fisica_list')

class ReempadComercioFisicaListView(ListView):
    model = ReempadComercioFisica
    template_name = 'reempad_comercio_fisica_list.html'

class ReempadComercioJuridicaCreateView(CreateView):
    model = ReempadComercioJuridica
    form_class = ReempadComercioJuridicaForm
    template_name = 'reempad_comercio_juridica_create.html'
    
    def form_valid(self, form):
        # Guarda el objeto sin confirmar para obtener el id
        self.object = form.save()

        # Redirige a la página de éxito y pasa el objeto
        return render(self.request, 'formulario_completado.html', {'object': self.object})