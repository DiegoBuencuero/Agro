# Generated by Django 4.1.7 on 2023-04-18 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agro', '0046_rename_desnsidad_planificacion_densidad_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Planificacion_etapas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=4, max_digits=10)),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=12)),
                ('cotizacion', models.DecimalField(decimal_places=3, default=1, max_digits=12)),
                ('agro_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agro.agro_producto')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agro.empresa')),
                ('especificacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='agro.especificacion_tipo')),
            ],
        ),
        migrations.AlterModelOptions(
            name='agro_etapa',
            options={'ordering': ['orden']},
        ),
        migrations.AddField(
            model_name='agro_etapa',
            name='abreviado',
            field=models.CharField(default='', max_length=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agro_etapa',
            name='orden',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Plnificacion_Insumos',
        ),
        migrations.AddField(
            model_name='planificacion_etapas',
            name='etapa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agro.agro_etapa'),
        ),
        migrations.AddField(
            model_name='planificacion_etapas',
            name='moneda',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='agro.moneda'),
        ),
        migrations.AddField(
            model_name='planificacion_etapas',
            name='planificacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agro.planificacion'),
        ),
        migrations.AddField(
            model_name='planificacion_etapas',
            name='um',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agro.um'),
        ),
    ]
