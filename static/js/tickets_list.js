let selected_tickets = [];

function validate_search_data(form) {
    const controls = form.elements;
    for (let i=0; i<controls.length; i++) {
        controls[i].disabled = controls[i].value === '';
        if (!isNaN(controls[i].value)
            && controls[i].value !== ''
            && controls[i].type === 'text') {
            // todo: replace alert() to {error message} block
            alert('Проверьте введенные данные');
            return false;
        }
    }
    return true;
}

function sellTickets() {
    
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

function arrayRemove(arr, value) {
   return arr.filter(function(elem){
       return elem !== value;
   });
}
