
$(document).ready(function () {
    $("#competitions-table").tablesorter({
        cancelSelection:true,
    });
});

/*
 * Set up datepicker fields.
 */

$.datepicker.setDefaults({
    dateFormat: "dd/mm/yy",
});

/* On load */
$(function () {
    $("#from-date-picker").datepicker();
    $("#to-date-picker").datepicker();
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

    var fromDate = document.getElementById("from-date-picker").value;
    var toDate = document.getElementById("to-date-picker").value;

    $.ajax({
        type: "GET",
        url: "/search/competitions",
        dataType: "html",
        data: {
            "category": selectedCategory,
            "from_date": fromDate,
            "to_date": toDate
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


