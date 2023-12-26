from django.contrib import admin
from .models import ReempadComercioFisica, Estado

# Register your models here.

class ReempadComercioFisicaAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'apellido', 'nombreFantasia', 'cuit'),
    ordering = ['fecha']

class EstadoAdmin(admin.ModelAdmin):
    search_fields = ('nombre'),
    ordering = ['nombre']

admin.site.register(ReempadComercioFisica, ReempadComercioFisicaAdmin)
admin.site.register(Estado, EstadoAdmin)