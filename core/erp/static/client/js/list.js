let tableClient;

function getData() {
    //Función para cargar el datatable
    tableClient = $('#data').DataTable({
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
}

$(function () {
    modal_title = $('.modal-title');
    getData();//llamamos al datatable


    $('.btnAdd').on('click', function () { //cuando presione el botón me abra el modal
        $('input[name="action"]').val('add'); //cuando presione el botón tome el valor del action como add para poder procesaorlo en el view
        modal_title.find('span').html('Creación de un cliente');
        console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass('fas fa-plus');
        $('form')[0].reset();
        $('#myModalClient').modal('show'); //me permite visualizar el modal
    })
    $('form').on('submit', function (e) { //cuando le de click al botón de type submit
        //let parameters = $(this).serializeArray(); //esto me permite obtener en un array todos los datos que hay en nuestro formulario. Con this hago referencia al formulario
        let parameters = new FormData(this); //con esto hago una instancia de FormData y le mando el formulario actual a través de this, eso viaja al parameters q se le pasa al ajax
        e.preventDefault();

        submitWithajax(window.location.pathname, 'Notificación', '¿Estás seguro que desea realizar la siguiente acción?', parameters, function () {
            //Una vez que se ejecute todoo el submit
            tblClient.ajax.reload();//refresco el datatable
            //getData();
            $('#myModalClient').modal('hide'); //oculto el modal
        });
    });
});


