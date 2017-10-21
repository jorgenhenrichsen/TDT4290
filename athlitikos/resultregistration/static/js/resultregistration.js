
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
// });
function newRow(id){
    var $table = $(id)
    console.log($table.children.length)
    console.log($table.append('<div>urgh</div>'))
}

function ajaxSubmit(id) {
    var $myForm = $(id)
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
