let asGuest = false;

function changeCheckboxState() {
    asGuest = asGuest === false;
    document.getElementById("username").disabled = asGuest;
    document.getElementById("password").disabled = asGuest;
}

function getUserID() {
    const username = document.getElementById('username').value;
    console.log(username);
    sessionStorage.setItem('username', username);
}