function load_especificaciones(url_ajax, clave, objeto_detino, parametro) { 
    $.ajax({
      url : url_ajax,
      data : {
        'producto' : clave,
      },
      method : 'GET',
      success : function(response) {
        var opciones = "";
        response.data.forEach(function(item, index) {
          opciones += '<option value="' + item.id + '">' + item.nombre + '</option>';
        });
        objeto_detino.innerHTML = opciones;
        if (parametro != undefined) id_espec.value = parametro;

      } 
    });

  }