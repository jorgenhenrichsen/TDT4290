$(function(){

    $('#search').keyup(function() {

        $.ajax({
            type: "POST",
            url: "/autocomplete/search/",
            data: {
                'search_text' : $('#search').val(),
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchSuccess,
            dataType: 'html'
        });

    });

});

function searchSuccess(data, textStatus, jqXHR)
{
    $('#autocomplete-results').html(data);
}
