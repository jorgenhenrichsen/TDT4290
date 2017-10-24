
$(function(){

    // Disable sorting for the actions column.
    $("#result-table").tablesorter({
        headers: {
            '.actions' : {
                sorter: false
            }
        }
    });
});


function deletePendingGroup(id) {
    alert("Delete"+ id);
}

