from django import forms
from .models import ReempadComercioFisica
from django.forms import TextInput, NumberInput, EmailInput, FileInput, Select

class ReempadComercioFisicaForm(forms.ModelForm):
    class Meta:
        model = ReempadComercioFisica
        fields = ['nombre', 'apellido', 'nombreFantasia', 'cuit', 'ingresosBrutos', 'convenioMultilateral', 'domicilioFiscal', 'localidad', 'codigoPostal', 'provincia', 'domicilioComercial', 'email', 'telefonoComercial', 'telefonoTitular', 'superficieLocal', 'superficieDeposito', 'actividadPrincipal', 'rubro2', 'rubro3', 'rubro4', 'sucursal', 'domicilioSucursal', 'inscripcionAFIP']
        exclude = ['fecha', 'estado']
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control'}),
            'apellido': TextInput(attrs={'class': 'form-control'}),
            'nombreFantasia': TextInput(attrs={'class': 'form-control'}),
            'cuit': NumberInput(attrs={'class': 'form-control'}),
            'ingresosBrutos': NumberInput(attrs={'class': 'form-control'}),
            'convenioMultilateral': NumberInput(attrs={'class': 'form-control'}),
            'domicilioFiscal': TextInput(attrs={'class': 'form-control'}),
            'localidad': TextInput(attrs={'class': 'form-control'}),
            'codigoPostal': NumberInput(attrs={'class': 'form-control'}),
            'provincia': TextInput(attrs={'class': 'form-control'}),
            'domicilioComercial': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'telefonoComercial': NumberInput(attrs={'class': 'form-control'}),
            'telefonoTitular': NumberInput(attrs={'class': 'form-control'}),
            'superficieLocal': NumberInput(attrs={'class': 'form-control'}),
            'superficieDeposito': NumberInput(attrs={'class': 'form-control'}),
            'actividadPrincipal': TextInput(attrs={'class': 'form-control'}),
            'rubro2': TextInput(attrs={'class': 'form-control'}),
            'rubro3': TextInput(attrs={'class': 'form-control'}),
            'rubro4': TextInput(attrs={'class': 'form-control'}),
            'sucursal': Select(choices=[(False, 'No'), (True, 'Sí')], attrs={'class': 'form-control'}),
            'domicilioSucursal': TextInput(attrs={'class': 'form-control'}),
            'inscripcionAFIP': FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
        }