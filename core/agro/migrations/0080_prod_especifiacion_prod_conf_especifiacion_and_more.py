# Generated by Django 4.2.4 on 2023-09-11 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agro', '0079_prod_conf_descripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='prod',
            name='especifiacion',
            field=models.CharField(default='', max_length=80),
        ),
        migrations.AddField(
            model_name='prod_conf',
            name='especifiacion',
            field=models.CharField(default='', max_length=80),
        ),
        migrations.AlterField(
            model_name='prod_conf',
            name='descripcion',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='prod_conf',
            name='stock',
            field=models.CharField(choices=[('S', 'Si'), ('N', 'No')], default='N', max_length=1),
        ),
    ]
