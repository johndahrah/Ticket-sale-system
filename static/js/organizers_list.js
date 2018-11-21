let selected;
let errorBox = document.getElementById('error-box');
let newOrganizerForm = document.getElementById('new-organizer-form');

function deleteOrganizer() {
    if (confirm("Вы действительно хотите удалить организатора?")) {
        let xhr = new XMLHttpRequest();

        xhr.onreadystatechange = showPossibleErrorAndReloadIfSucces(xhr);

        xhr.open("GET", '/api/organizer/delete/' + selected, true);
        xhr.setRequestHeader('Content-type', 'charset=utf-8');
        xhr.send();
    }
}

function showNewOrganizerForm() {
    newOrganizerForm.className = newOrganizerForm.className === 'form-visible'?
        'form-hidden' : 'form-visible';
    newOrganizerForm.scrollIntoView(false);
}

function selectOrganizer(table) {
    const id = table.id;
    if (selected === id) {
        table.style.borderWidth="1px";
        table.style.marginBottom="20px";
        selected = 0;
    } else {
        table.style.borderWidth="3px";
        table.style.marginBottom="16px";
        selected = id;
    }
}

function showPossibleErrorAndReloadIfSucces(xhr) {
    return function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            let response = xhr.responseText;
            console.log(response);
            if (response.length !== 0) {
                if (response.substr(0, 7) === 'Успешно') {
                    showSuccessMessage(response)
                } else if (response.length < 60) {
                    showError(response);
                } else {
                    showError('Ошибка сервера')
                }
            } else {
                window.location.reload(false)
            }
        }
    };
}

function showError(text) {
    errorBox.className = 'error-message';
    errorBox.innerText = text;
}

function showSuccessMessage(s) {
    errorBox.className = 'error-message-success';
    errorBox.innerText = s;
}
