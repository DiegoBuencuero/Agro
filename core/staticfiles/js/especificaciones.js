function load_especificaciones(url_ajax, clave, um, objeto_detino, parametro) { 
  if (clave === '') {
    objeto_detino.innerHTML = "<option value '' selected>---------</option>";
  }
  else {
    $.ajax({
      url : url_ajax,
      data : {
        'producto' : clave,
      },
      method : 'GET',
      success : function(response) {
        um.value = response.um.id;
        var opciones = "";
        response.data.forEach(function(item, index) {
          opciones += '<option value="' + item.id + '">' + item.nombre + '</option>';
        });
        objeto_detino.innerHTML = opciones;
        if (parametro != undefined) id_espec.value = parametro;

      } 
    });

  }

  }