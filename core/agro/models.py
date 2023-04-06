from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from .choices import *

# Create your models here.

class Moneda(models.Model):
    def __str__(self):
        return self.nombre
    nombre = models.CharField(max_length=50)
    corto = models.CharField(max_length=3)

class Cotizacion(models.Model):
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE, null=True, blank=True)
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    cotizacion = models.DecimalField(max_digits=12, decimal_places=3)

class Cotizacion_general(models.Model):
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    cotizacion = models.DecimalField(max_digits=12, decimal_places=3)

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
    def __str__(self):
        return self.nombre
    nombre = models.CharField(max_length=100)

class Provincia(models.Model):
    def __str__(self):
        return self.nombre
    nombre = models.CharField(max_length=100)
    pais = models.ForeignKey("Pais", verbose_name=("Pais"), on_delete=models.CASCADE)

class Ciudad(models.Model):
    def __str__(self):
        return self.nombre
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
    moneda = models.ForeignKey(Moneda, null=True, blank=True, on_delete=models.CASCADE)
    


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
    telefono = models.CharField(max_length=30, default='', null=True, blank=True)
    celular = models.CharField(max_length=30, default='', null=True, blank=True)
    nacionalidad = models.ForeignKey("Nacionalidad", verbose_name=("Nacionalidad"), on_delete=models.CASCADE, null=True, blank=True)
    genero = models.ForeignKey("Genero", verbose_name=("Genero"), on_delete=models.CASCADE, null=True, blank=True)
    tipodoc = models.ForeignKey("Tipodoc", verbose_name=("Tipo documento"), on_delete=models.CASCADE, null=True, blank=True)
    documento = models.CharField(max_length=50, default='')
    fecha_nacimiento = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=[('N', 'Ingresado'), ('A', 'Aprobado'), ('S', 'Suspendido'), ], default='N')
    observaciones = models.CharField(null=True, blank=True, max_length=1000)
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
    def __str__(self):
        return self.nombre
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    image = models.ImageField(default='default.jpg', upload_to='campos')
    observaciones = models.TextField(null=True, blank=True)

class Lote(models.Model):
    class Meta:
        pass
    def __str__(self):
        return self.nombre

    campo = models.ForeignKey("Campo", verbose_name=("Campo"), on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    image = models.ImageField(default='default.jpg', upload_to='lotes')
    ha_totales = models.DecimalField(max_digits=6, decimal_places=2)
    ha_productivas = models.DecimalField(max_digits=6, decimal_places=2)

class Actividad(models.Model):
    class Meta:
        pass
    def __str__(self):
        return self.nombre
    nombre = models.CharField(max_length=50)

class UM(models.Model):
    class Meta:
        pass
    def __str__(self):
        return self.nombre
    nombre = models.CharField(max_length=50)
    abreviado = models.CharField(max_length=5)

class Trazabilidad(models.Model):
    class Meta:
        pass
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    lote = models.ForeignKey("Lote", on_delete=models.CASCADE)
    actividad = models.ForeignKey("Actividad", on_delete=models.CASCADE) 
    fecha = models.DateField(null=True, blank=True)
    origen_prod = models.CharField(max_length=1, choices=[('S', 'Sisitema'), ('U', 'Usuario'),], default='U')
    producto_id = models.IntegerField(null=True, blank=True)
    cantidad = models.DecimalField(max_digits=6, decimal_places=2)
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE, null=True, blank=True) 
    cotizacion = models.DecimalField(max_digits=12, decimal_places=3, default=1)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)

    unidad_medida = models.ForeignKey("UM", on_delete=models.CASCADE) 
    id_mov = models.ForeignKey("Mov", verbose_name=("Movimiento stock"), on_delete=models.CASCADE)
    perfil = models.ForeignKey("Profile", on_delete=models.CASCADE)

class agro_Producto(models.Model):
    def __str__(self):
        return self.descripcion
    codigo = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=100)
    tipo = models.ForeignKey("Tipo", on_delete=models.CASCADE) 
    rubro = models.ForeignKey("Rubro", on_delete=models.CASCADE) 
    image = models.ImageField(default='default.jpg', upload_to='lotes')
    status = models.CharField(max_length=1, choices=[('O', 'Ok'), ('B', 'Baja'), ], default='O')
    add_date = models.DateTimeField(default=timezone.now)

class Producto(agro_Producto):
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)

class Tipo(models.Model):
    class Meta:
        pass
    def __str__(self):
        return self.nombre
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)

class Rubro(models.Model):
    class Meta:
        pass
    def __str__(self):
        return self.nombre
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)

class Deposito (models.Model):
    class Meta:
        pass
    def __str__(self):
        return self.nombre
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
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE, null=True, blank=True) 
    cotizacion = models.DecimalField(max_digits=12, decimal_places=3, default=1)

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
    def __str__(self):
        return self.nombre
    nombre = models.CharField(max_length=100)
    producto_semilla = models.ForeignKey("Producto", on_delete=models.CASCADE, null=True, blank=True)
    producto_cultivo = models.ForeignKey("Producto", related_name='cultivo_producto_cultivo', on_delete=models.CASCADE, null=True, blank=True)


class Calendario (models.Model):
    class Meta:
        pass
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    lote = models.ForeignKey("Lote", on_delete=models.CASCADE)
    planificacion = models.ForeignKey("Planificacion", on_delete=models.CASCADE)
    fecha_ini = models.DateField()
    fecha_final = models.DateField()

class SistemaCultivo(models.Model):
    def __str__(self):
        return self.descripcion
    descripcion = models.CharField(max_length=80)

class Especificacion(models.Model):
    def __str__(self):
        return self.descripcion
    descripcion = models.CharField(max_length=100)

class agro_CostoProd(models.Model):
    cultivo = models.ForeignKey("Cultivo", on_delete=models.CASCADE)  
    sistema_cultivo = models.ForeignKey("SistemaCultivo", on_delete=models.CASCADE) 

class agro_CostoProdo(models.Model):
    orden = models.IntegerField()
    costo_prod = models.ForeignKey("CostoProd", on_delete=models.CASCADE) 
    agro_producto = models.ForeignKey("agro_Producto", on_delete=models.CASCADE) 
    especificacion = models.ForeignKey("Especificacion", on_delete=models.CASCADE) 
    um = models.ForeignKey(UM, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=6, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE, null=True, blank=True) 
    cotizacion = models.DecimalField(max_digits=12, decimal_places=3, default=1)

class CostoProd(agro_CostoProd):
    fecha = models.DateField(default=timezone.now)
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)

class CostoProdo(agro_CostoProdo):
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
