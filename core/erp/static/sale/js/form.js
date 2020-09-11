$(function () {
    $('.select2').select({
        theme:"bootstrap4",
        lengauage:"es"
    });
    $('#sale_date').datetimepicker({
        format:'YYYY-MM-DD',
        data:moment().format('YYYY-MM-DD'),
        locale:"es",
    });
});