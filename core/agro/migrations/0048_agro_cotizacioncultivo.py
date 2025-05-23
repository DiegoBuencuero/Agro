# Generated by Django 4.1.7 on 2023-04-18 19:27

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('agro', '0047_planificacion_etapas_alter_agro_etapa_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='agro_CotizacionCultivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(default=django.utils.timezone.now)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=12)),
                ('cotizacion', models.DecimalField(decimal_places=3, default=1, max_digits=12)),
                ('cultivo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agro.cultivo')),
                ('moneda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agro.moneda')),
            ],
        ),
    ]
