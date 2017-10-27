
$(document).ready(function () {
    $("#competitions-table").tablesorter({
        cancelSelection:true,
    });

    fetchCompetitions();
});

var selectedCategory = "all";

function openCompetition(id) {
    alert("Open" + id);
}

function didSelectCategory() {
    selectedCategory = $("#category-selector").val();
    fetchCompetitions();
}

function fetchCompetitions() {
    $.ajax({
        type: "GET",
        url: "/search/competitions",
        dataType: "html",
        data: {
                "category": selectedCategory,
        },
        success: function(html) {
            /* Replace the html of the result table's tbody with the new entries. */
            $("table tbody").html(html);
            $("#competitions-table").trigger("update");
        },
        error: function() {
          console.log("ERROR");
        },
        complete: function() {
            console.log("COMPLETE");
        }
    });
}