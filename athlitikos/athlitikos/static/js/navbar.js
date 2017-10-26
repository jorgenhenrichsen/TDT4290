
function logoutCurrentUser() {

    $.ajax({
        type: "GET",
        url: "/logout/",
        dataType: "html",
        success: function () {

            console.log("Logged out");
            document.getElementById("user-status-container").innerHTML = "<button onclick='login()'>Login</button>";

        },
        error: function () {
          console.log("ERROR");
        },
        complete: function () {
            console.log("COMPLETE");
        },
    })

}

function login() {
    window.location.href = "/login/";
}