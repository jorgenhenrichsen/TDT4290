
// Autocompletion
$(function () {
    $(".lifter-input-field").autocomplete({
        source: "/search/lifter",
        minLength: 2,
        select: function (event, ui) {
            var elementId = "#" + $(this).attr("id") + "_id";
            $(elementId).val(ui.id);
        }
    });

    $(".club-input-field").autocomplete({
        source: "/search/club/",
        minLength: 2,
    });
});


// Add a new lifter row to the form
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

// Display validation errors on load.
function displayErrors(errors) {
    console.log(errors);
    var errors = errors.replace(/&#39;/g, '"');
    console.log(errors);
    var errorArray = $.parseJSON(errors);
    console.log(errorArray);


    const fieldNames = new Array(["lifter"]);

    for (i = 0; i < errorArray.length; i++) {

        for (y = 0; y < fieldNames.length; y++) {
            const fieldName = fieldNames[y];
            const id = "#id_form-" + i + "-" + fieldName;
            const fieldErrors = errorArray[i][fieldName];


            if (fieldErrors != undefined) {
                console.log(id, fieldErrors);

                for (e = 0; e < fieldErrors.length; e++) {
                    const error = fieldErrors[e];
                    console.log(error)
                    $(id).before("<label>" + error + "</label>")
                }
                    //
            }
        }
    }

}
