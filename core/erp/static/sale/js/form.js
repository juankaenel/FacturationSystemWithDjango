let vents = {
    items: { //diccionario con tod o lo que tiene mi cabacera y mi detalle
        client: '',
        date_joined: '',
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        products: [],
    },
    calculate_invoice: function(){ //calcular factura
        let subtotal = 0.00;
        let iva = $('input[name="iva"]').val(); //lo definí en create.html, un iva calculado
        $.each(this.items.products,function (pos,dict) {
           dict.subtotal = dict.cant * parseFloat(dict.pvp);
           subtotal += dict.subtotal;
        });
        //valores de los inputs
        this.items.subtotal = subtotal;
        this.items.iva = this.items.subtotal*iva;
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
         $('#tablaProductos').DataTable({
        responsive:true,
        autoWidth:false,
        destroy:true,
        deferRender:true, //se pone cuando hay datos q superen los 50000
        data:this.items.products,
        columns:[
            {"data":"id"}, //0
            {"data":"name"}, //1
            {"data":"cat.name"}, //2
            {"data":"pvp"},  //3
            {"data":"cant"},  //3
            {"data":"subtotal"},  //3
        ],
        columnDefs:[ //personalizacion de las columnas
            {
                targets: [0], //en la posición 1 está el botón eliminar, ese es el que quiero editar
                class: 'text-center',
                orderable:false,
                render: function (data,type,row) { //desde acá le mandamos los botones y las rutas
                    return '<a rel="remove" class="btn btn-danger btn-xs btn-flat"> <i class="fas fa-trash-alt"></i></a>';
                },

            },
            {
                targets: [-3, -1], //en la posición -3 precio unitario y -1, ese es el que quiero editar
                class: 'text-center',
                orderable:false,
                render: function (data,type,row) { //desde acá le mandamos los botones y las rutas
                    return '$'+parseFloat(data).toFixed(2); //retorna un signo de dolar con dos digitos
                },

            },
            {
                targets: [-2], //en la posición -2
                class: 'text-center',
                orderable:false,
                render: function (data,type,row) { //desde acá le mandamos los botones y las rutas
                    //row.cant hace referencia a la cantidad q definí de productos
                    return '<input type="text" name="cant" class="form-control form-control-sm input-sm" value="'+row.cant+'" autocomplete="off">';
                },

            },
        ],
        rowCallback(row,data,displayNum,displayIndex,dataIndex){
        //con rowcallback puedo acceder a los datos del datatable
        //busco en la fila el input cant
            $(row).find('input[name="cant"]').TouchSpin({
                min: 0,
                max: 100,
                step: 0.01,
                });
        },
        initComplete:function (settings,json) { //se ejecuta cuando se carga la tabla
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
    }).on('change',function () {
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
                dataType:'json',
            }).done(function (data) {
                response(data);
            }).fail(function (jqXHR,textStatus,errorThrown) {
                //alert(textStatus+ ':' + errorThrown)
            }).always(function (data) {

            });
        },
        delay:500,
        minLength:1,
        select: function (event,ui) {
            event.preventDefault();
            console.clear();
            ui.item.cant = 1; //defino la cantidad de productos como 1 debido a que no se solicita la cantidad pero se debe mostrar en la tabla
            ui.item.subtotal=0.00; //defino el subtotal
            //console.log(ui.item); //imprimo lo que me llega por la búsqueda
            //vents.items.products.push(ui.item);//agregamos al array de products los items encontrados en el input del search
            vents.add(ui.item); // es equivalente a ->  vents.items.products.push(ui.item);
            vents.list();//listamos los productos en la tabla
            //console.log(vents.items); //controlamos los items del array y vemos que se van agregando los productos buscados
            $(this).val(''); //vaciamos el valor del input
        }

    });

    //evento cantidad
    $('#tablaProductos tbody').on('change', 'input[name="cant"]',function () {
        console.clear();
        let cant = parseInt($(this).val());

    })

});
