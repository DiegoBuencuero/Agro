# Generated by Django 4.1.7 on 2023-04-06 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agro', '0024_rename_nomnbre_moneda_nombre'),
    ]

    operations = [
        migrations.AddField(
            model_name='agro_costoprod',
            name='nombre',
            field=models.CharField(default='', max_length=50),
        ),
    ]
