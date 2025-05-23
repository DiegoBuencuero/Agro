from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from .choices import *
from django.core.exceptions import ValidationError
from django.db import models
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
    def __str__(self):
        return self.nombre
    class Meta:
        pass
    nombre = models.CharField(max_length=100)
    razon_social = models.CharField(max_length=100)
    cuit = models.CharField(max_length=50)
    status = models.CharField(max_length=1, choices=[('O', 'Ok'), ('B', 'Baja'), ('S', 'Suspendido'), ], default='O')
    add_date = models.DateTimeField(default=timezone.now)
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE)
    
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
    ciudad = models.CharField(max_length=100, null=True, blank=True)
    descripcion = models.CharField(max_length=100)
    image = models.ImageField(default='default.jpg', upload_to='campos')
    observaciones = models.TextField(null=True, blank=True)

class Ciudades(models.Model):
    class Meta:
        pass
    def __str__(self):
        return self.nombre
    nombre =  models.CharField(max_length=100)
    pais = models.CharField(max_length=10)
    longitud = models.DecimalField(max_digits=10, decimal_places=6)
    latitud = models.DecimalField(max_digits=10, decimal_places=6)

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
    codigo = models.CharField(max_length=2)
    agro_tipo = models.ManyToManyField("agro_TipoProd")

class UM(models.Model):
    class Meta:
        pass
    def __str__(self):
        return self.nombre
    nombre = models.CharField(max_length=50)
    abreviado = models.CharField(max_length=5)

class EstadoLote(models.Model):
    lote = models.ForeignKey("Lote", on_delete=models.CASCADE)
    planificacion = models.ForeignKey("Planificacion_cultivo", on_delete=models.CASCADE, null=True, blank=True)
    cultivo = models.ForeignKey("Cultivo", on_delete=models.CASCADE)
    fecha_desde = models.DateField(default=timezone.now) 
    fecha_hasta = models.DateField(default=timezone.now)
    estado = models.CharField(max_length=1, choices=[('A', 'Abierto'), ('C', 'Cerrado')], default='A')

class TrazaLote(models.Model):
    class Meta:
        pass
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    estado_lote = models.ForeignKey("EstadoLote", on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateField(default=timezone.now)
    actividad = models.ForeignKey("Actividad", on_delete=models.CASCADE) 
    observaciones = models.TextField()
    perfil = models.ForeignKey("Profile", on_delete=models.CASCADE)

class TrazaLoteItem(models.Model):
    class Meta:
        pass
    trazalote = models.ForeignKey(TrazaLote, on_delete=models.CASCADE)
    o = models.IntegerField()
    producto = models.ForeignKey("Prod", on_delete=models.CASCADE)
    especificacion = models.CharField(max_length=80, default='')
    cantidad = models.DecimalField(max_digits=6, decimal_places=2)
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE, null=True, blank=True) 
    cotizacion = models.DecimalField(max_digits=12, decimal_places=3, default=1)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    unidad_medida = models.ForeignKey("UM", on_delete=models.CASCADE) 

class Trazabilidad(models.Model):
    class Meta:
        pass
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    actividad = models.ForeignKey("Actividad", on_delete=models.CASCADE) 
    fecha = models.DateField(null=True, blank=True)
    origen_prod = models.CharField(max_length=1, choices=[('S', 'Sisitema'), ('U', 'Usuario'),], default='U')
    producto_id = models.IntegerField(null=True, blank=True)
    especificacion = models.ForeignKey("Especificacion_tipo", on_delete=models.CASCADE, null=True, blank=True)
    cantidad = models.DecimalField(max_digits=6, decimal_places=2)
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE, null=True, blank=True) 
    cotizacion = models.DecimalField(max_digits=12, decimal_places=3, default=1)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    unidad_medida = models.ForeignKey("UM", on_delete=models.CASCADE) 
    id_mov = models.ForeignKey("Mov", verbose_name=("Movimiento stock"), on_delete=models.CASCADE)
    perfil = models.ForeignKey("Profile", on_delete=models.CASCADE)
    estado_lote = models.ForeignKey("EstadoLote", on_delete=models.CASCADE, null=True, blank=True)

class agro_CotizacionCultivo(models.Model):
    class Meta:
        pass
    def __str__(self):
        return str(self.fecha) + "-" + self.cultivo
    fecha = models.DateField(default=timezone.now)
    cultivo = models.ForeignKey("Cultivo", on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE) 
    cotizacion = models.DecimalField(max_digits=12, decimal_places=3, default=1)

class agro_Etapa(models.Model):
    class Meta:
        ordering = ["orden"]
    def __str__(self):
        return self.nombre + " (" + self.abreviado + ")"
    nombre = models.CharField(max_length=100)
    abreviado = models.CharField(max_length=4)
    orden = models.IntegerField()

class agro_TipoProd(models.Model):
    class Meta:
        pass
    def __str__(self):
        return self.nombre
    nombre = models.CharField(max_length=100)
    etapas = models.ManyToManyField(agro_Etapa, blank=True)
    color = models.CharField(max_length=7, default = '#FFFFFF')

class agro_RubroProd(models.Model):
    class Meta:
        pass
    def __str__(self):
        return self.nombre
    orden = models.IntegerField(default=0)
    nombre = models.CharField(max_length=100)
    letra = models.CharField(max_length=1, default = 'A')
    color = models.CharField(max_length=7, default = '#FFFFFF')

class Especificacion_tipo(models.Model):
    class Meta:
        pass
    def __str__(self):
        return self.nombre
    agro_tipo = models.ForeignKey(agro_TipoProd, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100)

class agro_Producto(models.Model):
    class Meta:
        ordering = ["descripcion"]
    def __str__(self):
        return self.descripcion
    codigo = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=100)
    agro_tipo = models.ForeignKey(agro_TipoProd, on_delete=models.CASCADE, null=True, blank=True)
    agro_rubro = models.ForeignKey(agro_RubroProd, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='lotes')
    status = models.CharField(max_length=1, choices=[('O', 'Ok'), ('B', 'Baja'), ], default='O')
    um = models.ForeignKey(UM, on_delete=models.CASCADE)
    add_date = models.DateTimeField(default=timezone.now)

class Producto(models.Model):
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    codigo = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=100)
    agro_tipo = models.ForeignKey(agro_TipoProd, on_delete=models.CASCADE, null=True, blank=True)
    agro_rubro = models.ForeignKey(agro_RubroProd, on_delete=models.CASCADE, null=True, blank=True)
    tipo = models.ForeignKey("Tipo", on_delete=models.CASCADE, null=True, blank=True) 
    rubro = models.ForeignKey("Rubro", on_delete=models.CASCADE, null=True, blank=True) 
    image = models.ImageField(default='default.jpg', upload_to='lotes')
    status = models.CharField(max_length=1, choices=[('O', 'Ok'), ('B', 'Baja'), ], default='O')
    um = models.ForeignKey(UM, on_delete=models.CASCADE)
    add_date = models.DateTimeField(default=timezone.now)

class TipoProd(models.Model):
    def __str__(self):
        return self.descripcion
    descripcion = models.CharField(max_length=100)

class RubroProd(models.Model):
    def __str__(self):
        return self.descripcion
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=100)

class ClaseProd(models.Model):
    def __str__(self):
        return self.descripcion
    codigo = models.CharField(max_length=1, choices=[('I', 'Insumo'), ('P', 'Producto venta')])
    descripcion = models.CharField(max_length=100)

class Prod(models.Model):
    def __str__(self):
        return self.descripcion
    descripcion = models.CharField(max_length=100)
    observaciones = models.TextField(blank=True, default='')
    clase = models.ForeignKey(ClaseProd, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoProd, on_delete=models.CASCADE)
    especificacion = models.CharField(max_length=80, default='', null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='lotes')
    status = models.CharField(max_length=1, choices=[('O', 'Ok'), ('B', 'Baja'), ], default='O')
    um = models.ForeignKey(UM, on_delete=models.CASCADE)
    add_date = models.DateTimeField(default=timezone.now)

class Prod_Conf(models.Model):
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    producto = models.ForeignKey(Prod, on_delete=models.CASCADE)
    stock = models.CharField(max_length=1, choices=[('S', 'Si'), ('N', 'No')], default = 'N')
    rubro = models.ForeignKey(RubroProd, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=100, default='', blank=True)
    especificacion = models.CharField(max_length=80, default='', blank=True)
    tipo = models.ForeignKey(TipoProd, on_delete=models.CASCADE, null=True, blank=True)
    um = models.ForeignKey(UM, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='lotes', null=True, blank=True)

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
        return self.descripcion 
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
    observaciones = models.CharField(max_length=100, default='')    
    deposito1=models.ForeignKey("Deposito", on_delete=models.CASCADE)
    deposito2=models.ForeignKey("Deposito", related_name="deposito2", on_delete=models.CASCADE, null= True, blank = True )

class Movo (models.Model):
    class Meta:
        pass
    mov = models.ForeignKey("Mov", on_delete=models.CASCADE)
    o = models.IntegerField()
    producto_id = models.IntegerField(null=True, blank=True)
    origen = models.CharField(max_length=1, choices = (('A', 'Agro'), ('U', 'Usuario')), default='A')
    cantidad = models.DecimalField(max_digits=4, decimal_places=1)
    precio_u = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE, null=True, blank=True) 
    cotizacion = models.DecimalField(max_digits=12, decimal_places=3, default=1, null=True, blank=True)

class Planificacion_cultivo (models.Model):
    def __str__(self):
        return self.descripcion

    class Meta:
        pass
    def clean_end_time(self):
        if self.fecha_hasta < self.fecha_desde:
            raise ValidationError('La fecha de termino debe ser mayor a la de inicio')
        if self.fecha_desde < self.campana.fecha_desde:
            raise ValidationError('La fecha de inicio debe ser mayor o igual que la fecha de inicio de campaña')
        if self.fecha_hasta > self.campana.fecha_hasta:
            raise ValidationError('La fecha de finalización debe ser menor o igual que la fecha de finalización de campaña')

    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    fecha_plani = models.DateField(default=timezone.now)
    campana = models.ForeignKey("Campana", on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=100)
    observaciones = models.TextField()
    fecha_desde = models.DateField(default=timezone.now) 
    fecha_hasta = models.DateField(default=timezone.now)
    costo = models.ForeignKey("CostoProd", on_delete=models.CASCADE, null=True, blank=True) 
      
class Campana ( models.Model):
    def __str__(self):
        return self.nombre
    class Meta:
        pass
    def clean_end_time(self):
        if self.fecha_hasta < self.fecha_desde:
            raise ValidationError('La fecha de termino debe ser mayor a la de inicio')
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    fecha_desde = models.DateField(default=timezone.now) 
    fecha_hasta = models.DateField(default=timezone.now)
    observaciones = models.TextField(null=True, blank=True)

class Planificacion_lote( models.Model):
    class Meta:
        pass
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    planificacion = models.ForeignKey("Planificacion_cultivo",  on_delete=models.CASCADE)
    lote = models.ForeignKey("Lote", on_delete=models.CASCADE)

class Planificacion_etapas(models.Model):
    def __str__(self):
        return self.planificacion.descripcion + '-' + str(self.producto_id) + '-' + str(self.cantidad)
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    planificacion = models.ForeignKey("Planificacion_cultivo",  on_delete=models.CASCADE)
    etapa = models.ForeignKey("agro_Etapa", on_delete=models.CASCADE)
    costoo = models.ForeignKey("CostoProdo", models.CASCADE, null=True, blank=True)
    cant_aplicada = models.DecimalField(max_digits=10, decimal_places=4)  

class Cultivo(models.Model):
    class Meta:
        pass
    def __str__(self):
        return self.nombre
    nombre = models.CharField(max_length=100)

class SistemaCultivo(models.Model):
    def __str__(self):
        return self.descripcion
    descripcion = models.CharField(max_length=80)

class Especificacion(models.Model):
    def __str__(self):
        return self.descripcion
    descripcion = models.CharField(max_length=100)

class agro_CostoProd(models.Model):
    def __str__(self):
        return self.nombre
    nombre = models.CharField(max_length=50, default = '')
    cultivo = models.ForeignKey("Cultivo", on_delete=models.CASCADE)  
    sistema_cultivo = models.ForeignKey("SistemaCultivo", on_delete=models.CASCADE) 

class agro_CostoProdo(models.Model):
    class Meta:
        ordering = ["costo_prod", "orden"]
    def __str__(self):
        return str(self.orden) + "-" + str(self.costo_prod) + "-" + str(self.agro_producto)
    orden = models.IntegerField()
    costo_prod = models.ForeignKey("agro_CostoProd", on_delete=models.CASCADE) 
    agro_producto = models.ForeignKey("agro_Producto", on_delete=models.CASCADE) 
    um = models.ForeignKey(UM, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=4)   #si la um es porcentaje aca va el porcentaje
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2) #si la um es porcentaje aca va un codigo (1:comp+manoobra+servmecanico)
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE, null=True, blank=True) 
    cotizacion = models.DecimalField(max_digits=12, decimal_places=3, default=1)
    especificacion = models.ForeignKey(Especificacion_tipo, on_delete=models.CASCADE, null=True, blank=True)

class CostoProd(models.Model):
    def __str__(self):
        return self.nombre
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)
    nombre = models.CharField(max_length=50, default = '')
    cultivo = models.ForeignKey("Cultivo", on_delete=models.CASCADE)
    sistema_cultivo = models.ForeignKey("SistemaCultivo", on_delete=models.CASCADE) 

class CostoProdo(models.Model):
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    orden = models.IntegerField()
    costo_prod = models.ForeignKey("CostoProd", on_delete=models.CASCADE) 
    producto_id = models.IntegerField(null=True, blank=True)
    origen = models.CharField(max_length=1, choices = (('A', 'Agro'), ('U', 'Usuario')), default='A')
    um = models.ForeignKey(UM, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=4)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE, null=True, blank=True) 
    cotizacion = models.DecimalField(max_digits=12, decimal_places=3, default=1)
    especificacion = models.ForeignKey(Especificacion_tipo, on_delete=models.CASCADE, null=True, blank=True)

class RegistroLluvia(models.Model):
    def __str__(self):
        return f"{self.campo} - {self.fecha} - {self.cantidad}" 
    empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    campo = models.ForeignKey("Campo", verbose_name=("Campo"), on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)
    cantidad = models.IntegerField(default=0)

class agro_CategoriaContacto(models.Model):
    def __str__(self):
        return self.descripcion
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

class Proveedor(models.Model):
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



#TABLAS NUEVAS

class ArchivoDato(models.Model):
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=50)  # rendimiento, P, K, pH, etc.
    archivo = models.FileField(upload_to='archivos/')
    formato = models.CharField(max_length=10)  # shp, csv, geojson
    fecha_carga = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

class DatoGeo(models.Model):
    archivo = models.ForeignKey(ArchivoDato, on_delete=models.CASCADE)
    latitud = models.FloatField()
    longitud = models.FloatField()
    valor = models.FloatField()
    unidad = models.CharField(max_length=20)
    tipo = models.CharField(max_length=50)  # duplicado a propósito para fácil acceso
    fecha = models.DateField(null=True, blank=True)  # fecha de toma del dato (opcional)


class ArchivoLote(models.Model):
    nombre = models.CharField(max_length=255)
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE, related_name='archivos')
    
    archivo = models.FileField(upload_to='lotes/')
    extension = models.CharField(max_length=20)
    tipo = models.CharField(max_length=20,choices=TIPO_CHOICES,verbose_name="Tipo de dado")
    fecha_carga = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre