let selected_tickets = [];

let errorBox = document.getElementById('error-box');

function validate_search_data(form) {
    const controls = form.elements;
    for (let i=0; i<controls.length; i++) {
        controls[i].disabled = controls[i].value === '';
        if (!isNaN(controls[i].value)
            && controls[i].value !== ''
            && controls[i].type === 'text') {
            showError('Введенные данные имеют неверный формат');
            return false;
        }
    }
    return true;
}

function sellTickets() {
    let xhr = new XMLHttpRequest();

    xhr.onreadystatechange = showPossibleErrorAndReloadIfSucces(xhr);

    let selling;
    if (selected_tickets.length === 1) {
        selling = selected_tickets[0];
    } else {
        selling = selected_tickets;
    }

    // just for testing
    let json = JSON.stringify({
        "selling": selling,
        "userid": 1,
        "coupon": "7sample"
    });
    xhr.open("POST", '/api/ticket/sell', true);
    xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    xhr.send(json);
}

function selectTickets(table) {
    const id = table.id;

    if (selected_tickets.includes(id)) {
        table.style.borderWidth="1px";
        table.style.marginBottom="20px";
        selected_tickets = arrayRemove(selected_tickets, id)
    } else {
        table.style.borderWidth="3px";
        table.style.marginBottom="16px";
        selected_tickets.push(id);
    }

    selected_tickets.sort(function(a, b){return a - b});
    console.log(selected_tickets)
}

function deleteTickets() {
    if (confirm("Вы действительно хотите удалить билет(ы)?")) {
        for (let i = 0; i < selected_tickets.length; i++) {
            let xhr = new XMLHttpRequest();

            xhr.onreadystatechange = showPossibleErrorAndReloadIfSucces(xhr);

            xhr.open("GET", '/api/ticket/delete/' + selected_tickets[i], true);
            xhr.setRequestHeader('Content-type', 'charset=utf-8');
            xhr.send();
        }
    }
}

function alterTicket() {
    if (selected_tickets.length !== 1) {
        showError('Выделите только один билет, чтобы его изменить');
    } else {
        errorBox.classList.toggle('error-message-hidden');
        // let xhr = new XMLHttpRequest();
        //
        // xhr.onreadystatechange = showPossibleErrorAndReloadIfSucces(xhr);
        //
        // xhr.open("GET", '/api/ticket/modify/' + selected_tickets[0], true);
        // xhr.setRequestHeader('Content-type', 'charset=utf-8');
        // xhr.send();
    }
}

function showNewEntryForm() {
    let newTicketForm = document.getElementById("new-ticket-form");
    newTicketForm.className = newTicketForm.className === "form-visible"?
        "form-hidden":"form-visible";
    newTicketForm.scrollIntoView(false);
}

function addTicket() {
    showSuccessMessage('Билет успешно добавлен');
}

function arrayRemove(arr, value) {
   return arr.filter(function(elem){
       return elem !== value;
   });
}

function showError(text) {
    errorBox.className = 'error-message';
    errorBox.innerText = text;
}

function showPossibleErrorAndReloadIfSucces(xhr) {
    return function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            let response = xhr.responseText;
            console.log(response);
            if (response.length !== 0) {
                showError(response)
            } else {
                // errorBox.classList.toggle('error-message-hidden');
                window.location.reload(false)
            }
        }
    };
}

function showSuccessMessage(s) {
    errorBox.className = 'error-message-success';
    errorBox.innerText = s;
}

function sleepFor(sleepDuration ){
    var now = new Date().getTime();
    while(new Date().getTime() < now + sleepDuration){ /* do nothing */ }
}
