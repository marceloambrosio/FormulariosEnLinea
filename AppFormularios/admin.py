from django.contrib import admin
from .models import ReempadComercioFisica, ReempadComercioJuridica, Estado

# Register your models here.

class ReempadComercioFisicaAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'apellido', 'nombreFantasia', 'cuit'),
    ordering = ['fecha']

class ReempadComercioJuridicaAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'apellido', 'nombreFantasia', 'cuit'),
    ordering = ['fecha']

class EstadoAdmin(admin.ModelAdmin):
    search_fields = ('nombre'),
    ordering = ['nombre']

admin.site.register(ReempadComercioFisica, ReempadComercioFisicaAdmin)
admin.site.register(ReempadComercioJuridica, ReempadComercioJuridicaAdmin)
admin.site.register(Estado, EstadoAdmin)