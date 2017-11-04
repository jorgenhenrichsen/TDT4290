
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
var numberOfRows = 0
function addRow(elem) {
    var $myDiv = $(elem)
    $.ajax({
        method: "POST",
        url: 'resultform/',
        data:{
            'rowId': numberOfRows,
        },
        dataType: 'html',
        success: function(data){
            // console.log($myDiv)
            $myDiv.append(data)
            data.trigger()
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
    var $table = $(div)
    for( i=0; i<10; i++){
        addRow($table)
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

    var $competition_form = $('.competition_form')
    $competition_form.submit(function (event){
        console.log('submitting competition')
        event.preventDefault()
        var $formData = $($competition_form).serialize()
        var $thisURL = $competition_form.attr('data-url')
        $.ajax({
            method: "POST",
            url: $thisURL,
            dataType: 'html',
            data: $formData,
            success: function(json){
                    var jsonObj = JSON.parse(json)
                    console.log('id:', jsonObj.competition_id)
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
    })

    var $group_form = $('.group_form')
    $group_form.submit(function (event) {
        console.log('submitting group')
        event.preventDefault()
        var $formData = $($group_form).serialize()
        var $thisURL = $group_form.attr('data-url')
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

    var $result_form = $('.result_form')
    console.log($result_form)
    $result_form.submit(function (event) {
        // console.log(document.getElementsByClassName('result_form').length)
        event.preventDefault()
        var rawElements = $('.result_form')
        var elements = rawElements.length
        // console.log(rawElements,elements)
        console.log('submitting result')
        var $form
        var $thisURL
        var id
        var pushstring = {name:"group_id", value:$('#group_id').val()}
        // var pushstring = $('#group_id_p')
        console.log('pushstring: ', pushstring)
        // for(var j=0, j<2, j++)
        for (var i=1; i<=elements; i++) {
        // for(var $$form in rawElements){
            // console.log($$form)
            id = "#pending_result"+i.toString()
            $form = $(id)
            // $form = $$form
            $thisURL = $form.attr('data-url')
            console.log($form)
            // var $formData = $($form).serialize()
            var $formData = $form.serializeArray()
            console.log($formData)
            $formData.push(pushstring)
            $.ajax({
                method: "POST",
                url: $thisURL,
                dataType: 'html',
                data: $formData,
                success: function (json) {
                    var jsonObj = JSON.parse(json)
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
