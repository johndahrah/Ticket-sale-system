function disableEmptyInputs(form) {
    const controls = form.elements;

    for (let i=0; i<controls.length; i++) {
        controls[i].disabled = controls[i].value === '';
        if (controls[i].className === 'search-input-text') {
            controls[i].value = '\'' + controls[i].value + '\'';
        }
    }
}

function sellTickets() {
    
}
