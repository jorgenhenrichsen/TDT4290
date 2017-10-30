
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

var selectedClubs =[];
var selectedCategory = "all";

/* On load */
$(function () {
    $("#from-date-picker").datepicker();
    $("#to-date-picker").datepicker();
    fetchCompetitions();
});


/*
 * Autocomplete function for the club text-input-field.
 */
$(function () {
    $("#host-query-field").autocomplete({
        source: "/search/club/",
        minLength: 1,
        select: function (event, ui) {
            var id = ui.item.label;
            console.log("Selected " + ui.item.label, "ID: " + id);

            if ($.inArray(id, selectedClubs) == -1) {
              selectedClubs.push(id);

              /* Create a button with id=lifter_id and text=lifet_label */
              var html = "<button id='" + id +"' onclick='removeClub(this.id)' class='filter-button'> "+ ui.item.label +"</button>";
              var clubs = document.getElementById("clubs-container");
              clubs.innerHTML += html;
          }

          ui.item.value = "";
        }
    });
});


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

    var serializedClubs = JSON.stringify(selectedClubs);


    $.ajax({
        type: "GET",
        url: "/search/competitions",
        dataType: "html",
        data: {
            "category": selectedCategory,
            "from_date": fromDate,
            "to_date": toDate,
            "hosts": serializedClubs
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

/* Remove a club from the filter list */
function removeClub(id) {

    selectedClubs.splice( selectedClubs.indexOf(id), 1 );

    var container = document.getElementById("clubs-container");
    var button = document.getElementById(id);

    container.removeChild(button);
}
