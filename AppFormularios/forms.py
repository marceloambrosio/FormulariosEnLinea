from django import forms
from .models import ReempadComercioFisica, ReempadComercioJuridica
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

class ReempadComercioJuridicaForm(forms.ModelForm):
    class Meta:
        model = ReempadComercioJuridica
        fields = ['razonSocial', 'nombreFantasia', 'caracter', 'cuit', 'ingresosBrutos', 'convenioMultilateral', 'irpc_numero', 'irpc_folio', 'irpc_libro', 'irpc_tema', 'irpc_anio', 'domicilioFiscal', 'localidad', 'codigoPostal', 'provincia', 'domicilioComercial', 'email', 'telefonoComercial', 'telefonoTitular', 'superficieLocal', 'superficieDeposito', 'actividadPrincipal', 'rubro2', 'rubro3', 'rubro4', 'sucursal', 'domicilioSucursal', 'socio1_nombre', 'socio1_apellido', 'socio1_dni', 'socio1_domicilio', 'socio1_caracter', 'socio2_nombre', 'socio2_apellido', 'socio2_dni', 'socio2_domicilio', 'socio2_caracter', 'inscripcionAFIP']
        exclude = ['fecha', 'estado']
        widgets = {
            'razonSocial': TextInput(attrs={'class': 'form-control'}),
            'nombreFantasia': TextInput(attrs={'class': 'form-control'}),
            'cuit': NumberInput(attrs={'class': 'form-control'}),
            'ingresosBrutos': NumberInput(attrs={'class': 'form-control'}),
            'convenioMultilateral': NumberInput(attrs={'class': 'form-control'}),
            'irpc_numero': NumberInput(attrs={'class': 'form-control'}),
            'irpc_folio': NumberInput(attrs={'class': 'form-control'}),
            'irpc_libro': NumberInput(attrs={'class': 'form-control'}),
            'irpc_tema': NumberInput(attrs={'class': 'form-control'}),
            'irpc_anio': NumberInput(attrs={'class': 'form-control'}),
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
            'caracter': TextInput(attrs={'class': 'form-control'}),
            'socio1_nombre': TextInput(attrs={'class': 'form-control'}),
            'socio1_apellido': TextInput(attrs={'class': 'form-control'}),
            'socio1_dni': NumberInput(attrs={'class': 'form-control'}),
            'socio1_domicilio': TextInput(attrs={'class': 'form-control'}),
            'socio1_caracter': Select(choices=[('Socio Gerente', 'Socio Gerente'), ('Responsable', 'Responsable'), ('Administrador', 'Administrador'), ('Apoderado', 'Apoderado')], attrs={'class': 'form-control'}),
            'socio2_nombre': TextInput(attrs={'class': 'form-control'}),
            'socio2_apellido': TextInput(attrs={'class': 'form-control'}),
            'socio2_dni': NumberInput(attrs={'class': 'form-control'}),
            'socio2_domicilio': TextInput(attrs={'class': 'form-control'}),
            'socio2_caracter': Select(choices=[('Socio Gerente', 'Socio Gerente'), ('Responsable', 'Responsable'), ('Administrador', 'Administrador'), ('Otro', 'Otro')], attrs={'class': 'form-control'}),
            'inscripcionAFIP': FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
        }