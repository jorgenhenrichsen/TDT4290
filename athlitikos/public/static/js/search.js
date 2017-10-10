
$(document).ready(function () {
   $("#result-table").tablesorter({
       cancelSelection:true,
   });
});

var selectedLifter;
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

    var lifterId = document.getElementById("lifter-id");
    lifterId.value = selectedLifter;

    var clubId = document.getElementById("club-id");
    clubId.value = selectedClub;

    $.ajax({
        type: "GET",
        url: "/search/results/",
        dataType: "json",
        success: function (data) {
            console.log(data);
            /* TODO: Update the table with the received json data */
        },
        error: function () {
          console.log("ERROR");  
        },
        complete: function () {
            console.log("COMPLETE");
        }
    });
}