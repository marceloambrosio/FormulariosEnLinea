from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from .models import ReempadComercioFisica, ReempadComercioJuridica
from .forms import ReempadComercioFisicaForm, ReempadComercioJuridicaForm

# Create your views here.

class ReempadComercioFisicaCreateView(CreateView):
    model = ReempadComercioFisica
    form_class = ReempadComercioFisicaForm
    template_name = 'reempad_comercio_fisica_create.html'
    success_url = reverse_lazy('home')

class ReempadComercioFisicaUpdateView(UpdateView):
    model = ReempadComercioFisica
    fields = ['estado', 'observaciones']

class ReempadComercioFisicaListView(ListView):
    model = ReempadComercioFisica
    template_name = 'reempad_comercio_fisica_list.html'

class ReempadComercioJuridicaCreateView(CreateView):
    model = ReempadComercioJuridica
    form_class = ReempadComercioJuridicaForm
    template_name = 'reempad_comercio_juridica_create.html'
    success_url = reverse_lazy('home')