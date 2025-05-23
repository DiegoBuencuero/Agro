# Generated by Django 4.1.7 on 2023-04-17 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agro', '0044_agro_rubroprod_letra'),
    ]

    operations = [
        migrations.CreateModel(
            name='agro_Etapa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterModelOptions(
            name='agro_producto',
            options={'ordering': ['descripcion']},
        ),
        migrations.AddField(
            model_name='agro_tipoprod',
            name='etapas',
            field=models.ManyToManyField(to='agro.agro_etapa'),
        ),
    ]
