
$(function(){

    // Disable sorting for the actions column.
    $("#result-table").tablesorter({
        headers: {
            '.actions' : {
                sorter: false
            }
        }
    });

    $("#add-competition-button").click(function () {
        window.location.href = "/resultregistration/competition/new";
    })
});

function addNewJudge() {
    window.location.href = "/judge/new";
}

function addNewLifter() {
    window.location.href = "/lifter/new";
}

function addNewClub() {
    window.location.href = "/club/new";
}

function deletePendingGroup(id) {
    window.location.href = "/result/delete/" + id;
}

function denyDeletePendingGroupClubofc() {
    window.alert("Kan bare slette resultater som venter på godkjenning");
}

function editPendingGroup(id) {
    window.location.href = "/result/edit/" + id;
}

function importExcel() {
    window.location.href = "/resultregistration/fromexcel/";
}

// Redirect to resultregistration on click.
$(function () {
    document.getElementById("add-result-button").onclick = function () {
        location.href = "/resultregistration/";
    }
});
