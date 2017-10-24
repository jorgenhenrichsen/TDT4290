// Redirect to resultregistration on click.
$(function () {
    document.getElementById("add-result-button").onclick = function () {
        location.href = "/resultregistration/";
    }
});

function editPendingGroup(id) {
    window.location.href = "/resultregistration/";
}