
    // using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
//
// $(document).ready(function(){
//     var $myForm = $('#competition_form')
//     $myForm.submit(function(event){
//         event.preventDefault()
//         var $formData = $(this).serialize()
//         var $thisURL = $myForm.attr('data-url') || window.location.href // or set your own url
//         $.ajax({
//             method: "POST",
//             url: $thisURL,
//             data: $formData,
//             success: handleFormSuccess,
//             error: handleFormError,
//         })
//     })
//
//     function handleFormSuccess(data, textStatus, jqXHR){
//         console.log('youhooo')
//         console.log(data)
//         console.log(textStatus)
//         console.log(jqXHR)
//         // $myForm.reset(); // reset form data
//     }
//
//     function handleFormError(jqXHR, textStatus, errorThrown){
//         console.log('fuckthis')
//         console.log(jqXHR)
//         console.log(textStatus)
//         console.log(errorThrown)
//     }
// // });
// function newRow(div){
//     // var $table = $(id)
//     // // console.log($table.append('<div>urgh</div>'))
//     // var rownumber = $table.childNodes.length
//     // console.log($table.children.length, rownumber)
//     // var row = '<div>this is a row <br></div>'
//     var $row =
//
//     return $row
//
// }
var numberOfRows = 0;
function addRow(elem) {
    var $myDiv = $(elem);
    $.ajax({
        method: "POST",
        url: 'resultform/',
        data:{
            'rowId': numberOfRows
        },
        dataType: 'html',
        success: function(data){
            // console.log($myDiv)
            $myDiv.append(data);
            data.trigger();
            // $(data).trigger('create')
            // $myDiv.page()
            // console.log($myDiv, $myDiv.children.length.toString())
            // console.log('id: ',$myDiv,' length: '+$myDiv.children.length.toString())
            // console.log('success')

            numberOfRows ++
        },
        error: function () {
            $myDiv.append('<div>error<br></div>')
        }
    })
}

// function getCompetitionId(div){
//     var competitionId = $('#competition_id')
//     competitionId.value = $('#competition_form').getAttribute('')
// }

function initiateResultRows(div){
    var $table = $(div);
    for( var i=0; i<10; i++){
        addRow($table);
        // $table.append(newRow('result_registration_table'))
        // $table.append('<div>this is a row <br></div>')
        $('#initiate').hide()
    }
}
$(document).ready(function() {
    // var $myForm = $('.ajax_form')
    // $myForm.submit(function (event) {
    //     console.log('submitting')
    //     event.preventDefault();
    //     var $formData = $($myForm).serialize()
    //     var $thisURL = $myForm.attr('data-url') || window.location.href // or set your own url
    //     console.log($formData, JSON.stringify($thisURL))
    //     console.log($myForm)
    //     if ($myForm.hasClass('.group_form')) {
    //         $.ajax({
    //             method: "POST",
    //             url: $thisURL,
    //             data: $formData,
    //             success: function () {
    //             },
    //             error: function () {
    //             },
    //             complete: function () {
    //                 console.log('complete')
    //             }
    //         })
    //     } else if ($myForm.hasClass('competition_form')) {
    //         $.ajax({
    //             method: "POST",
    //             url: $thisURL,
    //             dataType: 'html',
    //             data: $formData,
    //             success: function (json) {
    //
    //             },
    //             error: function () {
    //             },
    //             complete: function () {
    //                 console.log('complete')
    //             }
    //         })
    //     }
    //
    //
    // })

    var $competition_form = $('.competition_form');
    $competition_form.submit(function (event){
        console.log('submitting competition');
        event.preventDefault();
        var $formData = $($competition_form).serialize();
        var $thisURL = $competition_form.attr('data-url');
        $.ajax({
            method: "POST",
            url: $thisURL,
            dataType: 'html',
            data: $formData,
            success: function(json){
                    var jsonObj = JSON.parse(json);
                    console.log('id:', jsonObj.competition_id);
                    if (jsonObj.competition_id !== 0) {
                        // console.log('id:', jsonObj.competition_id)
                        $('#competition_id').val(jsonObj.competition_id)//json.getAttribute('competition_id')
                        // console.log($('#competition_id').)
                    }
            },
            error: function(){},
            complete: function () {
                console.log('complete')
            }
        })
    });

    var $group_form = $('.group_form');
    $group_form.submit(function (event) {
        console.log('submitting group');
        event.preventDefault();
        var pushstring = {name:"competition_id", value:$('#competition_id').val()};
        var $formData = $($group_form).serializeArray();
        $formData.push(pushstring);
        var $thisURL = $group_form.attr('data-url');
        $.ajax({
            method: "POST",
            url: $thisURL,
            dataType: 'html',
            data: $formData,
            success: function(json){
                    var jsonObj = JSON.parse(json)
                    console.log('id:', jsonObj.group_id)
                    if (jsonObj.group_id !== -1) {
                        // console.log('id:', jsonObj.competition_id)
                        $('#group_id').val(jsonObj.group_id)//json.getAttribute('competition_id')
                        // console.log($('#competition_id').)
                    }
            },
            error: function(){},
            complete: function () {
                console.log('complete')
            }
        })
    })

    var $result_form = $('.result_form');
    console.log($result_form);
    $result_form.submit(function (event) {
        // console.log(document.getElementsByClassName('result_form').length)
        event.preventDefault();
        var rawElements = $('.result_form');
        var elements = rawElements.length;
        // console.log(rawElements,elements)
        console.log('submitting result');
        var $form;
        var $thisURL;
        var id;
        var pushstring = {name:"group_id", value:$('#group_id').val()};
        // var pushstring = $('#group_id_p')
        console.log('pushstring: ', pushstring);
        // for(var j=0, j<2, j++)
        for (var i=1; i<=elements; i++) {
        // for(var $$form in rawElements){
            // console.log($$form)
            id = "#pending_result"+i.toString();
            $form = $(id);
            // $form = $$form
            $thisURL = $form.attr('data-url');
            console.log($form);
            // var $formData = $($form).serialize()
            var $formData = $form.serializeArray();
            console.log($formData);
            $formData.push(pushstring);
            $.ajax({
                method: "POST",
                url: $thisURL,
                dataType: 'html',
                data: $formData,
                success: function (json) {
                    var jsonObj = JSON.parse(json);
                    console.log(jsonObj.successful)
                },
                error: function () {
                },
                complete: function () {
                    console.log('complete')
                }
            })
        }
    })
});

function importExcel(){
    $.ajax({
        method: "POST",
        url: "fromexcel/",
        dataType: 'json',

        success: function(json){
            // console.log(json)
            // var jsonObj = JSON.parse(json)
            console.log(json.success, json.result_details);
            var competition = json.competition_details;
            var results = json.result_details;
            var group = json.group_details;
            fillCompetition(competition);
            fillResults(results);
            fillGroup(group);
            // $('#id_host').val(competition.host)
        },
        error: function (error) {
            console.log(error)
        },
        complete: function () {
            console.log('complete excel')
        }
    })
}

function fillCompetition(competition){
    $('#id_competition_category').val(competition.category)
    $('#id_host').val(competition.host)
    $('#id_location').val(competition.location)
    $('#id_start_date').val(competition.start_date)
}

function fillResults(results){
    // TODO: BETTER ARGUMENTS FOR FOR-LOOP
    for(var i = 0; i<results.length; i++){
        fillResultRow(results[i], i)
    }
}

function fillResultRow(resultRow, i){
    // id_form-i-field
    var $formId = '#pending_result'+i.toString()+' '
    console.log($formId, resultRow)
    // TODO: APPLY THIS TO NEW RESULTFORM
    // $('#id_form-'+i.toString()+'weight_class').val(resultRow.weight_class)
    // $('#id_form-'+i.toString()+'body_weight').val(resultRow.body_weight)
    // $('#id_form-'+i.toString()+'category').val(resultRow.category)
    // $('#id_form-'+i.toString()+'lifter').val(resultRow.lifter)
    // $('#id_form-'+i.toString()+'birth_date').val(resultRow.birth_date)
    // $('#id_form-'+i.toString()+'club').val(resultRow.club)
    // $('#id_form-'+i.toString()+'snatch1').val(resultRow.snatch1)
    // $('#id_form-'+i.toString()+'snatch2').val(resultRow.snatch3)
    // $('#id_form-'+i.toString()+'snatch3').val(resultRow.snatch2)
    // $('#id_form-'+i.toString()+'clean_and_jerk1').val(resultRow.clean_and_jerk1)
    // $('#id_form-'+i.toString()+'clean_and_jerk2').val(resultRow.clean_and_jerk2)
    // $('#id_form-'+i.toString()+'clean_and_jerk3').val(resultRow.clean_and_jerk3)

    $($formId+'#id_weight_class').val(resultRow.weight_class)
    $($formId+'#id_body_weight').val(resultRow.body_weight)
    $($formId+'#id_category').val(resultRow.age_group)
    $($formId+'#id_lifter_first_name').val(resultRow.lifter)
    $($formId+'#id_birth_date').val(resultRow.birth_date)
    $($formId+'#id_club').val(resultRow.club)
    $($formId+'#id_snatch1').val(resultRow.snatch1)
    $($formId+'#id_snatch2').val(resultRow.snatch3)
    $($formId+'#id_snatch3').val(resultRow.snatch2)
    $($formId+'#id_clean_and_jerk1').val(resultRow.clean_and_jerk1)
    $($formId+'#id_clean_and_jerk2').val(resultRow.clean_and_jerk2)
    $($formId+'#id_clean_and_jerk3').val(resultRow.clean_and_jerk3)


}

function fillGroup(group){
    $('#id_competition_leader').val(group.competition_leader)
    $('#id_jury').val(group.jury)
    $('#id_secretary').val(group.secretary)
    $('#id_speaker').val(group.speaker)

    $('#id_judges').val(group.judges)
    $('#id_technical_controller').val(group.technical_controller)
    $('#id_chief_marshall').val(group.chief_marshall)
    $('#id_time_keeper').val(group.time_keeper)

    $('#id_notes').val(group.notes)
    $('#id_records_description').val(group.records_description)


}
// function submitResult(form_id){
//     // var $result_form = document.getElementById(from_id)
//     var $result_form =$(form_id)
//     console.log(form_id, $result_form)
//     // console.log('submitting result')
//     $result_form.event.preventDefault()
//     // var $formData = $($result_form).serialize()
//     // // var $formData = $($result_form).serializeArray()
//     // // $formData.push({group_id: $('#group_id').toString()})
//     // var $thisURL = $result_form.attr('data-url')
//     // console.log($thisURL)
//     // $.ajax({
//     //     method: "POST",
//     //     url: $thisURL,
//     //     dataType: 'html',
//     //     data: $formData,
//     //     success: function(){},
//     //     error: function(){},
//     //     complete: function () {
//     //         console.log('complete')
//     //     }
//     // })
// }

// function group_success(data) {
//
// }
//
// function competition_success(json){
//     var jsonObj = JSON.parse(json)
//     console.log('id:',jsonObj.competition_id)
//     if(jsonObj.competition_id !== 0){
//         $('#competition_id').value = jsonObj.competition_id//json.getAttribute('competition_id')
//     }
// }
// function handleFormSuccess(data, textStatus, jqXHR){
//     console.log('youhooo')
//     // console.log(data)
//     // console.log(textStatus)
//     // console.log(jqXHR)
//     // $myForm.reset(); // reset form data
// }
//
// function handleFormError(jqXHR, textStatus, errorThrown){
//     console.log(jqXHR)
//     // console.log(textStatus)
//     // console.log(errorThrown)
// }
// function ajaxSubmit(node) {
//     console.log('ahaajsubmit')
// // $(document).ready(function(){
// //     var $myForm = $(node)
// //     var node = $(node)
//     var $myForm = $(node)
//     // console.log(node)
// };
