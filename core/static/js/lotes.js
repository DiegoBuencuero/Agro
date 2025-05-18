function load_lotes(url_param, clave, objeto_detino, parametro) { 
    $.ajax({
      url : url_param,
      data : {
        'campo' : clave,
      },
      method : 'GET',
      success : function(response) {
        var opciones = "";
        response.data.forEach(function(item, index) {
          opciones += '<option value="' + item.id + '">' + item.nombre + '</option>';
        });
        id_lote_campo.innerHTML = opciones;
        if (parametro != undefined) id_lote_campo.value = parametro;

      } // reference to below
    });

  }

