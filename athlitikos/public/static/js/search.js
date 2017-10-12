
$(document).ready(function () {
   $("#result-table").tablesorter({
       cancelSelection:true,
   });
});

var selectedLifter;
var selectedLifters = [];
var selectedClub;

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
          selectedLifter = id;

          console.log(selectedLifters);
          if ($.inArray(id, selectedLifters) == -1) {
              selectedLifters.push(id);

              /* Create a button with id=lifter_id and text=lifet_label */
              var html = "<button id='" + id +"' onclick='removeLifter(this.id)'> "+ ui.item.label +"</button>";
              var lifters = document.getElementById("lifters-container");
              lifters.innerHTML += html;
          }
          else {
              console.log("Was in the array");
          }



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
            selectedClub = id;
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

    console.log(selectedLifters);
    /* Fetching search results and reloading the table with the new values */
    var serializedLifters = JSON.stringify(selectedLifters);
    console.log(serializedLifters);
    $.ajax({
        type: "GET",
        url: "/search/",
        dataType: "html",
        data: {
                "lifter_id": selectedLifter,
                "lifters": serializedLifters,
                "club_id": selectedClub,
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
    console.log(id);

    selectedLifters.splice( selectedLifters.indexOf(id), 1 );
    console.log(selectedLifters);

    var container = document.getElementById("lifters-container");
    var button = document.getElementById(id);

    container.removeChild(button);



}

function clearThis(target){
        target.value= "";
}