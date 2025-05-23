# Generated by Django 4.1.7 on 2023-03-23 16:10

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agro', '0002_xnacionalidad_remove_profile_nacionalidad_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nacionalidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=50)),
                ('pais', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agro.pais', verbose_name='Pais')),
            ],
        ),
        migrations.AlterField(
            model_name='empresa',
            name='add_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 23, 16, 10, 39, 524741, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='add_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 23, 16, 10, 39, 525291, tzinfo=datetime.timezone.utc)),
        ),
        migrations.DeleteModel(
            name='xNacionalidad',
        ),
        migrations.AddField(
            model_name='profile',
            name='nacionalidad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='agro.nacionalidad', verbose_name='Nacionalidad'),
        ),
    ]
