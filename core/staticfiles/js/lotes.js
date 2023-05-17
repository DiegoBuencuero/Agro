function load_lotes(parametro) { 
    $.ajax({
      url : "{% url 'ajax_get_lote' %}",
      data : {
        'campo' : id_campo.value,
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

