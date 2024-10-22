function send_req_and_reload(slug, arg) {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", `/${slug}/${arg}`, true);
    xhr.onload = function() {
        window.location.reload();
    }
    xhr.send();
}


function delete_message(message) {
    let answ = confirm('Chcesz usunąć tą wiadomość?');
    console.log(answ)
    if (answ) {
        send_req_and_reload('delete_message', message.querySelector('input').value)
    }
}

function switch_hidden(switcher, id) {
    console.log('switching...')
    const obj = document.getElementById(id)
    // if (obj.hidden) {
    obj.hidden = false;
    switcher.class = switcher.class + ' lol';
    switcher.hidden = true;
        // switcher.querySelector('img').src = '/img/cross.svg'
    // } else {
        
        // obj.hidden = true;
        // switcher.querySelector('img').src = '/img/pencil.svg'
    // }
}

function search_user() {
    console.log('searching a user...')
    const xhr = new XMLHttpRequest();
    const username = document.getElementById('user_search').value;
    if (username) {
        xhr.open("GET", `/search_user/${username}`, true);
        xhr.onload = function() {
            const cont = document.getElementById('userListCont');
            const submitCont = document.createElement('div');
            submitCont.style = 'display: flex; justify-content: center; margin-top: 1em;'
            const submit = document.createElement('button');
            submit.type = 'submit';
            submit.className = 'btn btn-primary';
            submit.innerHTML = 'Dodaj przyjaciele';
            submitCont.appendChild(submit);
            while (cont.firstChild) {
                cont.removeChild(cont.firstChild);
            }

            const p = document.createElement('p');
            p.innerHTML = 'Wyniki:';
            p.style = "color: #969696;";
            cont.appendChild(p);
            const data = xhr.responseText.replace(/'/g, '').split(', ');

            if (xhr.responseText) {
                for (const name of data) {
                    const row = document.createElement('div');
                    row.className = 'form-row'
                    const inp = document.createElement('input');
                    inp.className = 'form-check-input';
                    inp.type = 'checkbox';
                    const username = name.toLowerCase().split(' ').slice(0, 2).join('_')
                    inp.name = username;
                    inp.id = username;
                    inp.value = 1;
                    const lbl = document.createElement('label');
                    lbl.className = 'form-check-label ms-2';
                    lbl.htmlFor = username;
                    lbl.innerHTML = name;
                    row.appendChild(inp);
                    row.appendChild(lbl);
                    cont.appendChild(row);
                }
                document.getElementById('user_add_form').append(submitCont);
            } else {
                const c = document.createElement('div');
                c.innerHTML = `Brak wyników dla zapytania "${username}"`
                cont.appendChild(c);
            }

        }
        xhr.send();
    }
    
}


function accept_friend(id) {
    send_req_and_reload('accept_friend', id)
}

function reject_friend(id) {
    send_req_and_reload('reject_friend', id)
}

function ask_delete_friend(id, name) {
    if (confirm(`Czy chesz usunąć ${name} z listy przyjaciele?`)) {
        send_req_and_reload('delete_friend', id)
    }
}

function ask_cancel_request(id, name) {
    if (confirm(`Czy chcesz anulować zapyt użytkowniky ${name} o dodaniu w przyjaciele?`)) {
        send_req_and_reload('cancel_request', id)
    }
}



document.getElementById('user_search').addEventListener('keyup', function(event) {
    if (event.key === 'Enter') {
        search_user()
    }
});

