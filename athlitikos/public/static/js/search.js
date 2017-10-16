
$(document).ready(function () {
   $("#result-table").tablesorter({
       cancelSelection:true,
   });
});

var selectedLifters = [];
var selectedClubs = [];

/*
 * Autocomplete function for the name text-input-field.
 */
$(function() {
  $("#query-lifter").autocomplete({
      source: "/search/lifter/",
      minLength: 2,
      select: function (event, ui) {
          var id = ui.item.id;
          console.log("Selected " + ui.item.label, "ID: " + id);

          if ($.inArray(id, selectedLifters) == -1) {
              selectedLifters.push(id);

              /* Create a button with id=lifter_id and text=lifet_label */
              var html = "<button id='" + id +"' onclick='removeLifter(this.id)' class='filter-button'> "+ ui.item.label +"</button>";
              var lifters = document.getElementById("lifters-container");
              lifters.innerHTML += html;
          }

          ui.item.value = "";
      }
  });
});

/*
 * Autocomplete function for the club text-input-field.
 */
$(function () {
    $("#query-club").autocomplete({
        source: "/search/club/",
        minLength: 1,
        select: function (event, ui) {
            var id = ui.item.id;
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

/*
 * Set up datepicker fields.
 */

$.datepicker.setDefaults({
    dateFormat: "dd/mm/yy",
});

$(function () {
    $("#from-date-picker").datepicker();
    $("#to-date-picker").datepicker()
});

/*
 * Custom form-submit function to supply ids for selected items.
 */
function submitForm() {
    var form = document.getElementById("search-form");

    var fromDate = document.getElementById("from-date-picker").value;
    var toDate = document.getElementById("to-date-picker").value;

    /* Fetching search results and reloading the table with the new values */
    var serializedLifters = JSON.stringify(selectedLifters);
    var serializedClubs = JSON.stringify(selectedClubs);
    $.ajax({
        type: "GET",
        url: "/search/",
        dataType: "html",
        data: {
                "lifters": serializedLifters,
                "clubs": serializedClubs,
                "from_date": fromDate,
                "to_date": toDate
        },
        success: function (html) {

            /* Replace the html of the result table with the new one. */
            $('#result-table').html(html);

            /* Add tablesorter behavior to the result table */
            document.getElementById('result-table').classList.add('tablesorter');

           $("#result-table").tablesorter({
               cancelSelection:true,
            });

        },
        error: function () {
          console.log("ERROR");  
        },
        complete: function () {
            console.log("COMPLETE");
        }
    });
}


/* Remove a lifter from the filter list */
function removeLifter(id) {

    selectedLifters.splice( selectedLifters.indexOf(id), 1 );

    var container = document.getElementById("lifters-container");
    var button = document.getElementById(id);

    container.removeChild(button);
}

/* Remove a club from the filter list */
function removeClub(id) {

    selectedClubs.splice( selectedClubs.indexOf(id), 1 );

    var container = document.getElementById("clubs-container");
    var button = document.getElementById(id);

    container.removeChild(button);
}

function didSelectAgeGroup(element) {
    var selectedIndex = $('option:selected',element).index() - 1; /* -1 because of the placeholder option */



}