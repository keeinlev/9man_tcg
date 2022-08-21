var axios = require("axios");

async function searchUsers() {

    axios.get('http://127.0.0.1:5000/search?query_string=' + $("#search").val()).then(resp => {

        $("#search_results").html("");
        let s = "";
        let users = resp.data['users'];
        users.forEach(function(u) {
            let id = u["id"];
            let username = u["username"];
            let date_joined = u["date_created"];
            console.log(id, username, date_joined);

            s += "<div class='field'><a href='/profile?user=" + id.toString() + "'>" + username + "</a><br>Joined: " + date_joined + "</div>";
            $("#search_results").html(s);
        });
        console.log(resp.data);
    });
    
}

$('#search').on("keyup", function(e) {
    e.preventDefault();
    if (e.key === "Enter") {
        searchUsers();
    }
})