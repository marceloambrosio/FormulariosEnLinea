# Generated by Django 4.2.7 on 2023-12-29 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppFormularios', '0004_reempadcomerciofisica_finalizado'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reempadcomerciojuridica',
            old_name='apellido',
            new_name='razonSocial',
        ),
        migrations.RemoveField(
            model_name='reempadcomerciojuridica',
            name='nombre',
        ),
        migrations.AlterField(
            model_name='reempadcomerciojuridica',
            name='caracter',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
