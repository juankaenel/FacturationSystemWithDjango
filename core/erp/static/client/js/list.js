$(function () {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'datasearch'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "names"},
            {"data": "surnames"},
            {"data": "dni"},
            {"data": "date_birthday"},
            {"data": "gender"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="#" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
    $('#myModalClient').modal('show'); //me permite visualizar el modal

     $('form').on('submit', function (e) {
            e.preventDefault();
            //let parameters = $(this).serializeArray(); //esto me permite obtener en un array todos los datos que hay en nuestro formulario. Con this hago referencia al formulario
            let parameters = new FormData(this); //con esto hago una instancia de FormData y le mando el formulario actual a través de this, eso viaja al parameters q se le pasa al ajax

            submitWithajax(window.location.pathname,'Notificación','¿Estás seguro que desea realizar la siguiente acción?', parameters, function () {
                location.href = '{{ list_url }}';
            });
        });
});