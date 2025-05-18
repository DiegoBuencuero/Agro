
from django.contrib import admin
from django.urls import path, include
from agro.views import ( home, login_page, signup, activate, personal_details, ChangePassword, vista_campos, editar_campos, vista_lotes, editar_lote,
 vista_producto,  editar_producto, vista_rubro_producto, editar_rubro_producto, vista_costo_prod, editar_costo_prod, ajax_get_costo, load_costo_agro, ajax_get_espec, editar_costo_prod_linea,
 vista_campana, editar_campana, vista_planificacion, editar_planificacion, vista_planificacion_lote,  ajax_get_lote, vista_lote_eliminar, vista_planificacion_etapas, vista_planificacion_etapas_reset,
 vista_comprobantes, editar_comprobante, vista_numerador, editar_numerador, vista_deposito, editar_deposito,  ajax_get_lote, vista_lote_eliminar, vista_planificacion_etapas, vista_lluvia, ajax_load_lluvias, vista_meteorologia,
)
from agro.views_diego import(
    upload_archivos, carga_archivos, mapa_shapefile, ajax_lotes_por_campo,get_capas_lote,
    get_capa_tipo, analizar_mapas, analizar_mapas_cocecha, api_mapa_lote, get_capas_selecc
)

from django.conf import settings
from django.conf.urls.static import static
from .urls_leo import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('i18n/', include('django.conf.urls.i18n')), 
    path('login', login_page),
    path('signup/', signup),
    path('activate/<uidb64>/<token>', activate, name='activate'),  
    path("accounts/", include("django.contrib.auth.urls")),
    path("personal-info/", personal_details, name='personal_details'),
    path('password-reset/', ChangePassword, name='password-reset'),
    path('06/', vista_numerador, name='vista_numerador'),
    path('06/<int:id_num>', editar_numerador, name='editar_numerador'),
    path('07/<int:id_com>', editar_comprobante, name='editar_comprobante'),
    path('08/',vista_deposito, name='vista_deposito'),
    path('08/<int:id_depo>', editar_deposito, name='editar_deposito'),
    path('regLluvias/', vista_lluvia, name='vista_lluvia'),
    path('ajax-load-lluvias/', ajax_load_lluvias, name='ajax_load_lluvias'),
    path('meteorologia/', vista_meteorologia, name='vista_meteorologia'),



    path('upload-arch', upload_archivos, name='upload_archivos'),
    path('carga_archivos', carga_archivos, name='carga_archivos'),
    path('mapa-shapefile/', mapa_shapefile, name='mapa_shapefile'),


    path("ajax/lotes/",ajax_lotes_por_campo, name="ajax_lotes_por_campo"),
    path("get_capas_lote/", get_capas_lote, name="get_capas_lote"),
    path("get_capa_tipo/", get_capa_tipo, name="get_capa_tipo"),
    path('anali-dif-maps', analizar_mapas, name='analizar_mapas'),

    path('anali-maps-coc', analizar_mapas_cocecha, name='analizar_mapas_cocecha'),
    path('api/mapa_lote/', api_mapa_lote, name='api_mapa_lote'),
    path('get_capas_selecc/', get_capas_selecc, name='get_capas_selecc'),
 


    
]
urlpatterns += url_leo
# Only add this when we are in debug mode.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    