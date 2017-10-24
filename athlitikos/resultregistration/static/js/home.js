
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

function editPendingGroup(id) {
    window.location.href = "/result/edit/" + id;
}

function deletePendingGroup(id) {
    alert("Delete"+ id);
}

