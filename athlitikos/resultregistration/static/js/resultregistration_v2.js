
// Autocompletion
$(function () {
    $(".lifter-input-field").autocomplete({
        source: "/search/lifter",
        minLength: 2,
        select: function (event, ui) {

            var baseElementId = $(this).attr("id").replace("lifter", "")
            console.log(baseElementId);
            var elementId = "#" + $(this).attr("id") + "_id";
            console.log(elementId);

            $(elementId).val(ui.item.id);


            $.ajax({
                type: "GET",
                dataType: "json",
                url: "/autofill/result/",
                data: {
                    "lifter_id": ui.item.id
                },
                success: function (json) {
                    console.log(json);

                    const club_field = "#" + baseElementId + "club";
                    $(club_field).val(json.club.name);

                    const club_id = club_field + "_id";
                    $(club_id).val(json.club.id);

                    const birth_date_field = "#" + baseElementId + "birth_date";
                    $(birth_date_field).val(json.birth_date);

                }
            })
            
        }
    });

    $(".club-input-field").autocomplete({
        source: "/search/club/",
        minLength: 2,
        select: function (event, ui) {
            var elementId = "#" + $(this).attr("id") + "_id";
            $(elementId).val(ui.item.id);
        }
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
    var errors = errors.replace(/&#39;/g, '"');
    var errorArray = $.parseJSON(errors);
    console.log(errorArray);

    const fieldNames = new Array("lifter", "lifter_id", "club", "club_id", "birth_date", "category", "body_weight");

    for (i = 0; i < errorArray.length; i++) {
        const errorDict = errorArray[i]
        console.log(errorDict);
        for (y = 0; y < fieldNames.length; y++) {
            const fieldName = fieldNames[y];
            const fieldErrors = errorDict[fieldName];
            const id = "#id_form-" + i + "-" + fieldName;

            if (fieldErrors != undefined) {
                for (e = 0; e < fieldErrors.length; e++) {
                    const error = fieldErrors[e];
                    $(id).before("<label>" + error + "</label>")
                }
            }
        }
    }
}
