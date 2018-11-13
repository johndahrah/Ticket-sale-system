let asGuest = false;

function changeCheckboxState() {
    asGuest = asGuest === false;
    document.getElementById("username").disabled = asGuest;
    document.getElementById("password").disabled = asGuest;
}