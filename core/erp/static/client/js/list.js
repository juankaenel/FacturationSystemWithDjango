var tblClient;

function getData() {
    //Función para cargar el datatable
    tblClient = $('#data').DataTable({
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
            {"data": "gender.name"}, //.name pq en el toJson le puse que sea un diccionario con id y name, en este caso el name me retorna el nombre del género
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></a> '; //btn editar
                    buttons += '<a href="#" type="button" class="btn btn-danger btn-xs btn-flat btnDelete"><i class="fas fa-trash-alt"></i></a>'; //btn borrar
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

    //ACCIÓN AGREGAR
    $('.btnAdd').on('click', function () { //cuando presione el botón me abra el modal
        $('input[name="action"]').val('add'); //cuando presione el botón tome el valor del action como add para poder procesaorlo en el view
        modal_title.find('span').html('Creación de un cliente');
        console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass('fas fa-plus');
        $('form')[0].reset();
        $('#myModalClient').modal('show'); //me permite visualizar el modal
    })


    //llamo a la tabla data, tbody. cuando haga click en el boton de clase btnEdit...

    $('#data tbody')
        //ACCION EDITAR
        .on('click', '.btnEdit', function () {
            modal_title.find('span').html('Edición de un cliente');
            modal_title.find('i').removeClass().addClass('fas fa-edit');

            //var data = tblClient.row( $(this).parents('tr') ).data() ; //trae los valores del componente de la tabla cuando pongo editar. Esto solo no nos serviría pq cuando pasa a diseño resposnivo cambia los parents
            //con diseño responsivo incluido
            var tr = tblClient.cell($(this).closest('td', 'li')).index();
            var data = tblClient.row(tr.row).data();

            //ahora paso los datos obtenidos de mi tabla a mis inputs. T-odo esto sucede cuando damos click en editar
            $('input[name="action"]').val('edit'); //cambio el tipo de acción para que se controle en el view de client
            $('input[name="id"]').val(data.id); //para esto tengo que mandarle desde el list.html de client un campo de tipo id hidden
            $('input[name="names"]').val(data.names);
            $('input[name="surnames"]').val(data.surnames);
            $('input[name="dni"]').val(data.dni);
            $('input[name="date_birthday"]').val(data.date_birthday);
            $('input[name="address"]').val(data.address);
            $('input[name="gender"]').val(data.gender.id); //retorno el id que hace referencia a ese género. Recordar q en el método ToJson retorna un diccionario
            //abrimos el modal
            $('#myModalClient').modal('show');
        })
        //ACCION BORRAR
        .on('click', '.btnDelete', function () {
            //var data = tblClient.row( $(this).parents('tr') ).data() ; //trae los valores del componente de la tabla cuando pongo editar. Esto solo no nos serviría pq cuando pasa a diseño resposnivo cambia los parents
            //con diseño responsivo incluido
            var tr = tblClient.cell($(this).closest('td', 'li')).index();
            var data = tblClient.row(tr.row).data();
            let parameters = new FormData();
            parameters.append('action','delete')
            parameters.append('id',data.id)
            submitWithajax(window.location.pathname, 'Notificación', '¿Estás seguro que desea eliminar el siguiente registro?', parameters, function () {
                tblClient.ajax.reload();//refresco el datatable

            });
            //$('#myModalClient').modal('show');
        })

    //cuando le de click al botón de type submit
    //let parameters = $(this).serializeArray(); //esto me permite obtener en un array todos los datos que hay en nuestro formulario. Con this hago referencia al formulario
    $('form').on('submit', function (e) {
        let parameters = new FormData(this); //con esto hago una instancia de FormData y le mando el formulario actual a través de this, eso viaja al parameters q se le pasa al ajax
        e.preventDefault();

        submitWithajax(window.location.pathname, 'Notificación', '¿Estás seguro que desea realizar la siguiente acción?', parameters, function () {
            //Una vez que se ejecute todoo el submit
            console.log('enviado');
            tblClient.ajax.reload();//refresco el datatable
            //getData();
            $('#myModalClient').modal('hide'); //oculto el modal
        });
    });
});


