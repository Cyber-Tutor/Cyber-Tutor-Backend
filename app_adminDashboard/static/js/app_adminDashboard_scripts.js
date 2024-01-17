$(document).ready(function () {
    let formIndex = parseInt($('#forms-container').data('form-index'), 10);

    $('#add-module-button').click(function () {
        let newForm = $('#form-template').html().replace(/__prefix__/g, formIndex);
        $('#forms-container').append(newForm);
        formIndex++;
        $('input[name$="TOTAL_FORMS"]').val(formIndex);
        $('#forms-container').data('form-index', formIndex);
    });
});
