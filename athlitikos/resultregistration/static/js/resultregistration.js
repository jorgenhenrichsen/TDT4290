
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
            console.log($myDiv, $myDiv.children.length.toString())
            console.log('id: ',$myDiv,' length: '+$myDiv.children.length.toString())
            console.log('success')
            numberOfRows ++
        },
        error: function () {
            $myDiv.append('<div>error<br></div>')
        }
    })
}

function initiateResultRows(div){
    var $table = $(div)
    for( i =0; i<10; i++){
        addRow($table)
        // $table.append(newRow('result_registration_table'))
        // $table.append('<div>this is a row <br></div>')
        $('#initiate').hide()
    }
}

function ajaxSubmit(node) {
    var $myForm = $(node)
    console.log($myForm )
    $myForm.submit(function(event){
        event.preventDefault();
        var $formData = $($myForm).serialize()
    var $thisURL = $myForm.attr('data-url') || window.location.href // or set your own url
    console.log($formData, JSON.stringify($thisURL))
    $.ajax({
        method: "POST",
        url: $thisURL,
        data: $formData,
        success: handleFormSuccess,
        error: handleFormError,
    })

    })


    function handleFormSuccess(data, textStatus, jqXHR){
        console.log('youhooo')
        // console.log(data)
        // console.log(textStatus)
        // console.log(jqXHR)
        // $myForm.reset(); // reset form data
    }

    function handleFormError(jqXHR, textStatus, errorThrown){
        console.log('fuckthis')
        // console.log(jqXHR)
        // console.log(textStatus)
        // console.log(errorThrown)
    }
};
