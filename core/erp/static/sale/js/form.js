let verts = {
    items: { //diccionario con tod o lo que tiene mi cabacera y mi detalle
        client: '',
        date_joined: '',
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        products: [],
    },
    add: function () {

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

    $("input[name='iva']").TouchSpin({ //Touchspin para el iva
        default: 21,
        min: 0,
        max: 100,
        step: 0.1,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%'
    });

    //busqueda de productos lo hacemos mediante la libreria jqueryui para usar el autocomplete
    $('input'[name = "search"]).autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products', //esto se lee en el views de sale como identificador
                    'term': request.term, //en la variable term viaja lo que se está buscando
                },
                datatype:'json',
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
            evemt.preventDefault();
            console.clear();
            //console.log(ui.item);
            verts.items.products.push(ui.item);//agregamos al array de products los items encontrados
            $(this).val(''); //vaciamos el valor del input
        }

    });

});
l