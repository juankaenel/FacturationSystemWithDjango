let tblSale;

$(function () {

    tblSale = $('#data').DataTable({
        //responsive: true, -> comentamos esto asi nos funciona el responsive de la tabla de detalle
        scrollX:true, //aplicamos el scroll para que se adapte ya que no tiene diseño responsivo
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {
                "className": 'details-control',
                "orderable": false,
                "data": null,
                "defaultContent": ''
            },
            {"data": "client.names"},
            {"data": "date_joined"},
            {"data": "subtotal"},
            {"data": "iva"},
            {"data": "total"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-2, -3, -4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/erp/sale/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';
                    buttons += '<a rel="details" class="btn btn-success btn-xs btn-flat"><i class="fas fa-search"></i></a> ';
                    //var buttons = '<a href="/erp/sale/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });

    //método format
    function format(d) {
        console.log(d);
        let html = '<table class="table">';
        //cabecera
        html += '<thead class="thead-dark">';
        html += '<tr><th scope="col">Productos</th>';
        html += '<th scope="col">Categoría</th>';
        html += '<th scope="col">Precio de venta</th>';
        html += '<th scope="col">Cantidad</th>';
        html += '<th scope="col">Subtotal</th></tr>';
        html += '</thead>';
        //info de la tabla
        $.each(d.det, function(key,value){
            html += '<tr>';
            html += '<td>'+value.prod.name+'</td>';
            html += '<td>'+value.prod.cat.name+'</td>';
            html += '<td>'+value.price+'</td>';
            html += '<td>'+value.cant+'</td>';
            html += '<td>'+value.subtotal+'</td>';
            html += '</tr>';
        });//itero los detalles de venta
        html += '</tbody>';
        return html;
    }


    $('#data tbody')
        //Botón para traer el detalle de la venta
        .on('click', 'a[rel="details"]', function () {
            let tr = tblSale.cell($(this).closest('td, li')).index();
            let data = tblSale.row(tr.row).data();
            //console.log(data);

            $('#tblDet').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                deferRender: true,
                //data: data.det,
                ajax: {
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'action': 'search_details_prod',
                        'id': data.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {"data": "prod.name"},
                    {"data": "prod.cat.name"},
                    {"data": "price"},
                    {"data": "cant"},
                    {"data": "subtotal"},
                ],
                columnDefs: [
                    {
                        targets: [-1, -3],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '$' + parseFloat(data).toFixed(2);
                        }
                    },
                    {
                        targets: [-2],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return data;
                        }
                    },
                ],
                initComplete: function (settings, json) {

                }
            });

            //muestro el modal de detalle cuando se hace click
            $('#myModelDet').modal('show');
            })

            //botón del datatable verde para acceder a mayor información de la venta -> https://datatables.net/examples/api/row_details.html
            .on('click', 'td.details-control', function () {
                var tr = $(this).closest('tr');
                var row = tblSale.row(tr);

                if (row.child.isShown()) {
                    // This row is already open - close it
                    row.child.hide();
                    tr.removeClass('shown');
                } else {
                    // Open this row
                    row.child(format(row.data())).show();
                    tr.addClass('shown');
                }
            });

});