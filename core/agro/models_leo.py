from django.db import models
from django.utils import timezone
from .choices import *


class agro_CategoriaContacto(models.Model):
    descripcion = models.CharField(max_length=80)

class Contactos(models.Model):
    def __str__(self):
        return self.nombre
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    email = models.EmailField()
    telefono = models.CharField(max_length=60)
    categorias = models.ManyToManyField(agro_CategoriaContacto, blank=True)

class agro_Ivapos(models.Model):
    def __str__(self):
        return self.descripcion
    descripcion = models.CharField(max_length=50)
    comprobante = models.ForeignKey(Com, on_delete=models.CASCADE)


class Proveedores(models.Model):
    def __str__(self):
        return self.razon_social
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    codigo_interno = models.CharField(max_length=20)
    razon_social = models.CharField(max_length=50)
    nombre_fantasia = models.CharField(max_length=50)
    direccion = models.CharField(max_length = 50)
    telefono = models.CharField(max_length = 30)
    email = models.EmailField(max_length = 250)
    cuit = models.CharField(max_length = 30)
    ivapos = models.ForeignKey(agro_Ivapos, on_delete=models.CASCADE)
    contactos = models.ManyToManyField(Contactos, blank=True)
    class Meta:
        ordering = ["razon_social"]
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"



