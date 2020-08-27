//esta funcion me permite trabajar con muchos datos en mis datatables
$(function () {
    $('#data').DataTable({
        responsive:true,
        autoWidth:false,
        destroy:true,
        deferRender:true, //se pone cuando hay datos q superen los 50000
        ajax:{
            url: window.location.pathname,
            type:'POST',
            data:{
                'action':'datasearch' //esto se lee en el views de category list view como identificador
            },
            dataSrc:''
        },
        columns:[
            {"data":"id"}, //0
            {"data":"names"}, //1
            {"data":"surnames"}, //2
            {"data":"dni"},  //3
            {"data":"date_birthday"}, //4
            {"data":"gender"}, //5
        ],
        columnDefs:[ //personalizacion de las columnas
            {
                targets: [-1], //de atrás para adelante
                class: 'text-center',
                orderable:false,
                //columna 6 -> botones
               render: function (data,type,row) { //desde acá le mandamos los botones y las rutas
                   let buttons = '<a href="/erp/category/update/'+row.id+'" type="button" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                   buttons += '<a href="/erp/category/delete/'+row.id+'" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                   return buttons;
               }
            },
        ],
        initComplete:function (settings,json) { //se ejecuta cuando se carga la tabla
            //alert('se cargó la tabla crack');
        }

    })

})