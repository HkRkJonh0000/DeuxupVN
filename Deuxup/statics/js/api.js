const API = "/api";
fetch(`${API}/auth/me/`)
.then(response => response.json()).then(data => {
    console.log(data);
}).catch(error => {
    console.error(error);
}).finally(() => {
    console.log("API call completed");
});

const btnMe = document.getElementById("btn-me");
btnMe.addEventListener("click", () => {
    fetch(`${API}/auth/me/`)
    .then(response => response.json()).then(data => {
        console.log(data);
    }).catch(error => {
        console.log(error);
    }).finally(() => {
        console.log("API call completed");
    });
});