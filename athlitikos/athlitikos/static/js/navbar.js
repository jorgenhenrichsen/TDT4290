
function logoutCurrentUser() {
    window.location.href = "/logout/";
    //$.ajax({
        //type: "GET",
        //url: "/logout/",
        //dataType: "html",
        //success: function () {

            //console.log("Logged out");
            //document.getElementById("user-status-container").innerHTML = "<button onclick='login()'>Login</button>"

        //},
        //error: function () {
          //console.log("ERROR");
        //},
        //complete: function () {
            //console.log("COMPLETE");
        //},
    //})

}

function login() {
    window.location.href = "/login/";
}

function redirectToResults() {
    window.location.href = "/search/";
}

function redirectToCompetitions() {
    window.location.href = "/search/competitions/";
}

function redirectToHome() {
    window.location.href = "/home/";
}

function collapseNavbar() {
    var x = document.getElementById("top-navbar");
    if (x.className === "navbar") {
        x.className += " responsive";
    } else {
        x.className = "navbar";
    }
}

function redirectToHomeAdmin() {
    window.location.href = "/home/admin/";
}

function redirectToHomeClubof() {
    window.location.href = "/home/clubofc/";
}