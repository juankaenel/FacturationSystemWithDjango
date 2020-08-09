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
    }
    else{
        html = '<p>'+obj+'</p>'
    }

}
