# Generated by Django 4.1.7 on 2023-08-24 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agro', '0074_remove_trazabilidad_planificacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='agro_producto',
            name='um',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='agro.um'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='producto',
            name='um',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='agro.um'),
            preserve_default=False,
        ),
    ]
