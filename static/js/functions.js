function message_error(obj) {
    let html = '';
    if (typeof (obj) == 'object') { //si el tipo de error capturado es un objeto..
        html = '<ul style="text-align: left;">';
        $.each(obj, function (key, value) {
            html += '<li>' + key + ': ' + value + '</li>';
        });
        html += '</ul>';
        Swal.fire({ //Sweet Alert
            title: 'Error!',
            html: html, //le paso el error atrapado en el form
            icon: 'error',
        })
    } else {
        html = '<p>' + obj + '</p>'
    }

}

function submitWithajax(url,parameters) {
    $.confirm({
        theme: 'material',
        title: 'Confirmación',
        icon: 'fa fa-info',
        content: '¿Estás seguro que desea realizar la acción?',
        columnClass: 'medium',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    $.ajax({
                //url: '{% url 'erp:category_create' %}',
                url: url,//,window.location.pathname,
                type: 'POST',
                data: parameters, //le mando los parametros del formulario
                dataType: 'json',
            }).done(function (data) {//si tod0 sale bien
                if (!data.hasOwnProperty('error')) {//si no detecta error
                    location.href = '{{ list_url }}';
                    return false; //para salir del proceso
                }
                //else

                message_error(data.error);

            }).fail(function (jqXHR, textStatus, errorThrown) {
                alert(textStatus + ': ' + errorThrown)
            }).always(function () {
                //console.log('complete') //se imprime siempre
            });
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {

                }
            },
        }
    })
}