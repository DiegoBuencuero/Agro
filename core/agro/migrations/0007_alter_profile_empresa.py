# Generated by Django 4.1.7 on 2023-03-23 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agro', '0006_alter_profile_ciudad_alter_profile_pais_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='empresa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='agro.empresa'),
        ),
    ]
