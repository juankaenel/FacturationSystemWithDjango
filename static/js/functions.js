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

function submitWithajax(url, title, content, parameters, callback) {
    $.confirm({
        theme: 'material',
        title: title,
        icon: 'fa fa-info',
        content: content,
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
                        processData: false, //no procese la data ni el tipo de dato, yo te lo mando por la vista
                        contentType: false,
                    }).done(function (data) {//si tod0 sale bien
                        if (!data.hasOwnProperty('error')) {//si no detecta error
                            callback();
                            return false; //para salir del proceso
                        }
                        //else

                        message_error(data.error);

                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        alert(textStatus + ': ' + errorThrown)
                    }).always(function (data) {
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

//Acción para preguntar si desea eliminar todos los productos del detalle de la factura
function alert_action(title, content, callback) {
    $.confirm({
        theme: 'material',
        title: title,
        icon: 'fa fa-info',
        content: content,
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
                    callback(); //el callback viene a ser la acción para vaciar la tabla
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