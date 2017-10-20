
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

// Redirect to resultregistration on click.
$(function () {
    document.getElementById("add-result-button").onclick = function () {
        location.href = "/resultregistration/";
    }
});

function editPendingGroup(id) {
    alert("Edit" + id);
}

function deletePendingGroup(id) {
    alert("Delete"+ id);
}
