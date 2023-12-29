import os

def upload_to_inscripcionAFIP_fisica(instance, filename):
    base, extension = os.path.splitext(filename)
    return 'ReempadronamientoFisica/{0}{1}-{2}-{3}-InscripcionAFIP{4}'.format(instance.apellido, instance.nombre, instance.nombreFantasia, instance.cuit, extension)

def upload_to_reempadronamiento_fisica(instance, filename):
    base, extension = os.path.splitext(filename)
    return 'ReempadronamientoFisica/{0}{1}-{2}-{3}-Final{4}'.format(instance.apellido, instance.nombre, instance.nombreFantasia, instance.cuit, extension)

def upload_to_inscripcionAFIP_juridica(instance, filename):
    base, extension = os.path.splitext(filename)
    return 'ReempadronamientoJuridica/{0}-{1}-{2}-InscripcionAFIP{3}'.format(instance.razonSocial, instance.nombreFantasia, instance.cuit, extension)

def upload_to_reempadronamiento_juridica(instance, filename):
    base, extension = os.path.splitext(filename)
    return 'ReempadronamientoJuridica/{0}-{1}-{2}-Final{3}'.format(instance.razonSocial, instance.nombreFantasia, instance.cuit, extension)