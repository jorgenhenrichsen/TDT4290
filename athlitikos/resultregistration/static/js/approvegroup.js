function approvePendingGroup(id) {
    window.location.href = "/result/approve/" + id;
}

function rejectPendingGroup(id) {
    window.location.href = "/result/reject/" + id;
}

function changePendingGroup(id) {
    window.location.href = "/resultregistration/edit/" + id;
}

function goBackToHome() {
    window.location.href = "/home/"
}

