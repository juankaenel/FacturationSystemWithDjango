$(function () {
    $('.select2').select({
        theme:"bootstrap4",
        lengauage:"es"
    });
   $('#date_joined').datetimepicker({ //datetimepicker para el la fecha de la factura
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"), //fecha actual
        locale: 'es',
        maxDate: moment().format("YYYY-MM-DD") //fecha límite
    });

   $("input[name='iva']").TouchSpin({ //Touchspin para el iva
        default:21,
        min: 0,
        max: 100,
        step: 0.1,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%'
    });
});l