
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
    window.location.href = "/result/edit/" + id;
}

function deletePendingGroup(id) {
    window.location.href = "/result/delete/" + id;
}

