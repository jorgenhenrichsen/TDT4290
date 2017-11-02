

$(function () {
    $(".lifter-input-field").children().first().autocomplete({
        source: "/search/lifter",
        minLength: 2,
        select: function (event, ui) {
            console.log(event);
            console.log(ui);
            $("#" + $(this).attr("id")).val(ui.id);
            // TODO: Need to set value to id here...
        }
  });
})


function cloneMore(selector, type) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + type + '-TOTAL_FORMS').val();
    newElement.find(':input').each(function() {
        var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
    newElement.find('label').each(function() {
        var newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
        $(this).attr('for', newFor);
    });
    total++;
    $('#id_' + type + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
}