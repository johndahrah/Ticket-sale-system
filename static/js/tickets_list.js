let selected_tickets = [];
let editingTicketID;

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
    if (selected_tickets.length === 0) {
        showError('Выберите билеты для продажи');
        return;
    }

    let xhr = new XMLHttpRequest();

    xhr.onreadystatechange = showPossibleErrorAndReloadIfSucces(xhr);

    let selling;
    if (selected_tickets.length === 1) {
        selling = selected_tickets[0];
    } else {
        selling = selected_tickets;
    }

    let couponData = prompt("Введите (при наличии) контрольную строку купона");

    let json = JSON.stringify({
        "selling": selling,
        "user_name": sessionStorage.getItem('username'),
        "coupon": couponData
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

function openTicketsForSale() {
    for (let i = 0; i < selected_tickets.length; i++) {

        let current = document.getElementById(selected_tickets[i]);
        if (current.classList[0] === "ticket-opened-sold") {
            showError("Билет уже продан");
            return false
        }
        if (current.classList[0] === "ticket-opened-not-sold") {
            showError("Билет уже открыт для продажи");
            return false
        }

        let xhr = new XMLHttpRequest();

        xhr.onreadystatechange = showPossibleErrorAndReloadIfSucces(xhr);

        let json = JSON.stringify({});
        json = JSON.parse(json);
        json[String('openedforselling')] = true;
        json = JSON.stringify(json);

        xhr.open("POST", '/api/ticket/modify/' + selected_tickets[i], true);
        xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
        xhr.send(json);
    }
}

function changeTicket(elem) {
    if (event.key === 'Enter') {
        let xhr = new XMLHttpRequest();

        xhr.onreadystatechange = showPossibleErrorAndReloadIfSucces(xhr);

        let json = JSON.stringify({});
        json = JSON.parse(json);
        json[String(elem.id)] = elem.value;
        json = JSON.stringify(json);

        xhr.open("POST", '/api/ticket/modify/' + editingTicketID, true);
        xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
        xhr.send(json);
    }
}

function makeFieldEditable(elem) {
    const id = elem.parentNode.parentNode.parentNode.parentNode.id;
    console.log(id);
    editingTicketID = id;
    elem.readOnly = false;
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
                if (response.substr(0, 7) === 'Успешно') {
                    showSuccessMessage(response)
                } else if (response.length < 70) {
                    showError(response);
                } else {
                    showError('Ошибка сервера')
                }
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
