# Generated by Django 4.1.7 on 2023-04-02 19:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agro', '0017_producto_add_date_producto_image_producto_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producto',
            old_name='nombre',
            new_name='descripcion',
        ),
    ]
