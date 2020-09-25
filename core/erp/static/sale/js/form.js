let tblProducts; //le asigno a mi tabla del list
let vents = {
    items: { //diccionario con tod o lo que tiene mi cabacera y mi detalle
        client: '',
        date_joined: '',
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        products: [],
    },
    calculate_invoice: function () { //calcular factura
        let subtotal = 0.00;
        let iva = $('input[name="iva"]').val(); //lo definí en create.html, un iva calculado
        $.each(this.items.products, function (pos, dict) {
            dict.pos = pos; //obtengo la posicion a medida que voy iterando
            dict.subtotal = dict.cant * parseFloat(dict.pvp);
            subtotal += dict.subtotal;
        });
        //valores de los inputs
        this.items.subtotal = subtotal;
        this.items.iva = this.items.subtotal * iva;
        this.items.total = this.items.iva + this.items.subtotal;
        //inputs de la factura
        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2)); //agrego al input el subtotal
        $('input[name="ivacalc"]').val(this.items.iva.toFixed(2)); //el iva calculado que defini en el create html, es igual al iva
        $('input[name="total"]').val(this.items.total.toFixed(2)); //el iva calculado que defini en el create html, es igual al iva
    },
    add: function (item) {
        this.items.products.push(item);
        this.list();
    },
    list: function () {
        this.calculate_invoice();
        tblProducts = $('#tablaProductos').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true, //se pone cuando hay datos q superen los 50000
            data: this.items.products,
            columns: [
                {"data": "id"}, //0
                {"data": "name"}, //1
                {"data": "cat.name"}, //2
                {"data": "pvp"},  //3
                {"data": "cant"},  //3
                {"data": "subtotal"},  //3
            ],
            columnDefs: [ //personalizacion de las columnas
                {
                    targets: [0], //en la posición 1 está el botón eliminar, ese es el que quiero editar
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) { //desde acá le mandamos los botones y las rutas
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat" style="color:white"> <i class="fas fa-trash-alt"></i></a>';
                    },

                },
                {
                    targets: [-3, -1], //en la posición -3 precio unitario y -1, ese es el que quiero editar
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) { //desde acá le mandamos los botones y las rutas
                        return '$' + parseFloat(data).toFixed(2); //retorna un signo de dolar con dos digitos
                    },

                },
                {
                    targets: [-2], //en la posición -2
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) { //desde acá le mandamos los botones y las rutas
                        //row.cant hace referencia a la cantidad q definí de productos
                        return '<input type="text" name="cant" class="form-control form-control-sm input-sm" value="' + row.cant + '" autocomplete="off">';
                    },

                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                //con rowcallback puedo acceder a los datos del datatable
                //busco en la fila el input cant
                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    max: 100,
                    step: 1,
                });
            },
            initComplete: function (settings, json) { //se ejecuta cuando se carga la tabla
                //alert('se cargó la tabla crack');
            }

        });
    }
};


$(function () {
    $('.select2').select({
        theme: "bootstrap4",
        lengauage: "es"
    });
    $('#date_joined').datetimepicker({ //datetimepicker para el la fecha de la factura
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"), //fecha actual
        locale: 'es',
        maxDate: moment().format("YYYY-MM-DD") //fecha límite
    });
    //------------------------------------------ IVA ------------------------------
    $("input[name='iva']").TouchSpin({ //Touchspin para el iva
        min: 0,
        max: 100,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%'
    }).on('change', function () {
        vents.calculate_invoice(); //cuando se cambie el iva con los botones arriba o abajo, o le demos un valor nuevo que me calcule de nuevo la factura
    })

        .val(0.21); //defino el iva en 21% por defecto

    //busqueda de productos lo hacemos mediante la libreria jqueryui para usar el autocomplete
    $('input[name="search"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products', //esto se lee en el views de sale como identificador
                    'term': request.term, //en la variable term viaja lo que se está buscando
                },
                dataType: 'json',
            }).done(function (data) {
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                //alert(textStatus+ ':' + errorThrown)
            }).always(function (data) {

            });
        },
        delay: 500,
        minLength: 1,
        select: function (event, ui) {
            event.preventDefault();
            //console.clear();
            ui.item.cant = 1; //defino la cantidad de productos como 1 debido a que no se solicita la cantidad pero se debe mostrar en la tabla
            ui.item.subtotal = 0.00; //defino el subtotal
            //console.log(ui.item); //imprimo lo que me llega por la búsqueda
            //vents.items.products.push(ui.item);//agregamos al array de products los items encontrados en el input del search
            vents.add(ui.item); // es equivalente a ->  vents.items.products.push(ui.item);
            vents.list();//listamos los productos en la tabla
            //console.log(vents.items); //controlamos los items del array y vemos que se van agregando los productos buscados
            $(this).val(''); //vaciamos el valor del input
        }

    });

    //botón eliminar todos los items
    $('.btnRemoveAll').on('click', function () {
        //llamo al alert_action de functions.js
        if (vents.items.products.length === 0) return false; //si no hay productos no puedo usar el botón
        alert_action('Notificación', '¿Estás seguro de eliminar todos los items de tu detalle?', function () {
            vents.items.products = []; //vacio los productos
            vents.list();
        });
    })

    $('#tablaProductos tbody')
        //botón eliminar
        .on('click', 'a[rel="remove"]', function () {
            let tr = tblProducts.cell($(this).closest('td,li')).index();
            //llamo al alert_action
            alert_action('Notificación', '¿Estás seguro de eliminar el producto de tu detalle?', function () {
                vents.items.products.splice(tr.row, 1) //tr.row pos actual
                vents.list();
            });
        })

        //evento cantidad
        .on('change', 'input[name="cant"]', function () {
            let cant = parseInt($(this).val());
            // ----- primera forma de obtener la posición y la cantidad -----
            let tr = tblProducts.cell($(this).closest('td,li')).index(); //hace referencia a la fila que necesito manejar
            //console.log(tr);
            //let data = tblProducts.row(tr.row).data(); //accedo al objeto de la fila
            vents.items.products[tr.row].cant = cant; //con el tr ya controlado actualizo la cantidad de productos
            //console.log(vents.items.products);

            //---- segunda forma ----
            //vents.items.products[data.pos].cant = cant; //es lo mismo que obtenerlo como lo hice con el tr, pos se controla en el $.each del calculate invoice, por cada iteración obtengo la posición de la fila
            //console.log(vents.items.products);

            //tanto data.pos como tr.row obtienen la posición de la fila que necesito actualizar la cantidad

            vents.calculate_invoice();
            $('td:eq(5)', tblProducts.row(tr.row).node()).html('$' + vents.items.products[tr.row].subtotal.toFixed(2)); //accedo a la posicion 5 de mi row, que en este caso va a el subtotal
        })

    //botón limpiar input
    $('.btnClearSearch').on('click',function () {
        $('input[name="search"]').val('').focus();
    });
    //evento submit
    $('form').on('submit', function (e) {
        e.preventDefault();

        //controlar que no se envíe form vacío
        if (vents.items.products.length === 0) {
            message_error('Debe al menos tener un item en su detalle de venta');
            return false;
        }


        vents.items.date_joined = $('input[name="date_joined"]').val();
        vents.items.client = $('select[name="client"]').val();

        let parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val()); //mando por parametros el action que se lee desde el create html
        parameters.append('vents', JSON.stringify(vents.items)); //JSON.stringify convierte un objeto o valor de JavaScript en una cadena de texto JSON
        submitWithajax(window.location.pathname, 'Notificación', '¿Estás seguro que desea realizar la siguiente acción?', parameters, function () {
            location.href = '/erp/dashboard';
        });
    })

    //listamos el datatable
    vents.list();

});
