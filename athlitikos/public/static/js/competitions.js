
$(document).ready(function () {
    $("#competitions-table").tablesorter({
        cancelSelection:true,
    });
});


function openCompetition(id) {
    alert("Open" + id);
}