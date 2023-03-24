from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from .choices import *

# Create your models here.
class Tipodoc(models.Model):
    def __str__(self):
        return self.descripcion
    descripcion = models.CharField(max_length=50)

class Nacionalidad(models.Model):
    def __str__(self):
        return self.descripcion
    descripcion = models.CharField(max_length=50)
    pais = models.ForeignKey("Pais", verbose_name=("Pais"), on_delete=models.CASCADE)

class Genero(models.Model):
    def __str__(self):
        return self.descripcion
    descripcion = models.CharField(max_length=50)

class Pais(models.Model):
    nombre = models.CharField(max_length=100)

class Provincia(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.ForeignKey("Pais", verbose_name=("Pais"), on_delete=models.CASCADE)

class Ciudad(models.Model):
    nombre = models.CharField(max_length=100)
    provincia = models.ForeignKey("Provincia", verbose_name=("Provincia"), on_delete=models.CASCADE)

class Empresa(models.Model):
    class Meta:
        pass
    nombre = models.CharField(max_length=100)
    razon_social = models.CharField(max_length=100)
    cuit = models.CharField(max_length=50)
    status = models.CharField(max_length=1, choices=[('O', 'Ok'), ('B', 'Baja'), ('S', 'Suspendido'), ], default='O')
    add_date = models.DateTimeField(default=timezone.now)
    


class Profile(models.Model):
    class Meta:
        pass
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    tipo = models.CharField(max_length=1, default='A') 
    direccion = models.CharField(max_length=100, default='')
    direccion2 = models.CharField(max_length=100, default='')
    pais = models.ForeignKey("Pais", on_delete=models.CASCADE, null=True, blank=True)
    provincia = models.ForeignKey("Provincia", verbose_name=("Provincia"), on_delete=models.CASCADE, null=True, blank=True)
    ciudad = models.ForeignKey("Ciudad", verbose_name=("Ciudad"), on_delete=models.CASCADE, null=True, blank=True)
    cp = models.CharField(max_length=10, default='')
    telefono = models.CharField(max_length=30, default='')
    celular = models.CharField(max_length=30, default='')
    nacionalidad = models.ForeignKey("Nacionalidad", verbose_name=("Nacionalidad"), on_delete=models.CASCADE, null=True, blank=True)
    genero = models.ForeignKey("Genero", verbose_name=("Genero"), on_delete=models.CASCADE, null=True, blank=True)
    tipodoc = models.ForeignKey("Tipodoc", verbose_name=("Tipo documento"), on_delete=models.CASCADE, null=True, blank=True)
    documento = models.CharField(max_length=50, default='')
    fecha_nacimiento = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=[('N', 'Ingresado'), ('A', 'Aprobado'), ('S', 'Suspendido'), ], default='N')
    add_date = models.DateTimeField(default=timezone.now)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Campo(models.Model):
    class Meta:
        pass
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100)

class Lote(models.Model):
    class Meta:
        pass
    campo = models.ForeignKey("Campo", verbose_name=("Campo"), on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    ha_totales = models.DecimalField(max_digits=6, decimal_places=2)
    ha_productivas = models.DecimalField(max_digits=6, decimal_places=2)

class Actividad(models.Model):
    class Meta:
        pass
    nombre = models.CharField(max_length=50)

class UM(models.Model):
    class Meta:
        pass
    nombre = models.CharField(max_length=50)
    abreviado = models.CharField(max_length=5)

class Trazabilidad(models.Model):
    class Meta:
        pass
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    lote = models.ForeignKey("Lote", on_delete=models.CASCADE)
    actividad = models.ForeignKey("Actividad", on_delete=models.CASCADE) 
    fecha = models.DateField(null=True, blank=True)
    producto = models.ForeignKey("Producto", on_delete=models.CASCADE) #armar tabla producto
    cantidad = models.DecimalField(max_digits=6, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    unidad_medida = models.ForeignKey("UM", on_delete=models.CASCADE) 
    id_mov = models.ForeignKey("Mov", verbose_name=("Movimiento stock"), on_delete=models.CASCADE)
    perfil = models.ForeignKey("Profile", on_delete=models.CASCADE)

class Producto(models.Model):
    class Meta:
        pass
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    codigo = models.CharField(max_length=30)
    nombre = models.CharField(max_length=100)
    tipo = models.ForeignKey("Tipo", on_delete=models.CASCADE) 
    rubro = models.ForeignKey("Rubro", on_delete=models.CASCADE) 

class Tipo(models.Model):
    class Meta:
        pass
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)

class Rubro(models.Model):
    class Meta:
        pass
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)

class Deposito (models.Model):
    class Meta:
        pass
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=30, default='')

class Num(models.Model):
    def __str__(self):
        return self.descrpcion
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    descrpcion = models.CharField(max_length=50)
    numero = models.IntegerField()

class Com(models.Model):
    def __str__(self):
        return self.descrpcion
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=50)
    abreviada = models.CharField(max_length=10)
    automatico = models.BooleanField(default=False)
    num = models.ForeignKey("Num", on_delete=models.CASCADE)
    tipo = models.CharField(max_length=1, choices=[('S', 'Stock'), ('V', 'Facturacion ventas'), ('P', 'Proveedores')])
    signo = models.CharField(max_length=1, choices=[('D', 'Debe'), ('H', 'Haber'), ('T', 'Transferencia')])


class Mov (models.Model):
    class Meta:
        pass
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    com = models.ForeignKey("COM", on_delete=models.CASCADE)
    n_suc = models.IntegerField()
    n_com = models.IntegerField()
    fecha = models.DateField()
    telefono = models.CharField(max_length=30, default='')    
    tipo = models.ForeignKey( "Producto", on_delete=models.CASCADE)#chequear
    deposito1=models.ForeignKey("Deposito", on_delete=models.CASCADE)
    deposito2=models.ForeignKey("Deposito", related_name="deposito2", on_delete=models.CASCADE)

class Movo (models.Model):
    class Meta:
        pass
    mov = models.ForeignKey("Mov", on_delete=models.CASCADE)
    o = models.IntegerField()
    producto= models;models.ForeignKey("Producto", verbose_name=("Producto"), on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=4, decimal_places=1)
    precio_u = models.DecimalField(max_digits=12, decimal_places=2)

class Planificacion (models.Model):
    class Meta:
        pass
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    cultivo = models.ForeignKey("Cultivo", on_delete=models.CASCADE)  
    desnsidad = models.CharField(max_length=1, choices = CH_DENSIDAD, default='1')
    profundidad = models.IntegerField()

class Plnificacion_Insumos (models.Model):
    class Meta:
        pass
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    Insumo = models.CharField(max_length=100)
    Cantidad = models.DecimalField(max_digits=4, decimal_places=1)

class Cultivo (models.Model):
    class Meta:
        pass
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    producto_semilla = models.ForeignKey("Producto", on_delete=models.CASCADE)
    producto_cultivo = models.ForeignKey("Producto", related_name='cultivo_producto_cultivo', on_delete=models.CASCADE)


class Calendario (models.Model):
    class Meta:
        pass
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    lote = models.ForeignKey("Lote", on_delete=models.CASCADE)
    planificacion = models.ForeignKey("Planificacion", on_delete=models.CASCADE)
    fecha_ini = models.DateField()
    fecha_final = models.DateField()



        
    