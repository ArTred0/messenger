function send_req_and_reload(slug, arg, arg2) {
    const xhr = new XMLHttpRequest();
    if (arg2){
        xhr.open("GET", `/${slug}/${arg}/${arg2}`, true);
    } else {
        xhr.open("GET", `/${slug}/${arg}`, true);
    }
    xhr.onload = function() {
        window.location.reload();
    }
    xhr.send();
}

function send_req_and_go_home(slug, arg, arg2) {
    const xhr = new XMLHttpRequest();
    if (arg2){
        xhr.open("GET", `/${slug}/${arg}/${arg2}`, true);
    } else {
        xhr.open("GET", `/${slug}/${arg}`, true);
    }
    xhr.onload = function() {
        window.location.assign('/');
    }
    xhr.send();
}

function send_req_and_do_nothing(slug, arg, arg2) {
    const xhr = new XMLHttpRequest();
    if (arg2){
        xhr.open("GET", `/${slug}/${arg}/${arg2}`, true);
    } else {
        xhr.open("GET", `/${slug}/${arg}`, true);
    }
    xhr.send();
}


function delete_message(message) {
    let answ = confirm('Chcesz usunąć tą wiadomość?');
    console.log(answ)
    if (answ) {
        send_req_and_reload('delete-message', message.querySelector('input').value)
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
        xhr.open("GET", `/search-user/${username}`, true);
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

function search_chat() {
    console.log('searching a chats...')
    const xhr = new XMLHttpRequest();
    const name = document.getElementById('chat_search').value;
    if (name) {
        xhr.open("GET", `/search-chat/${name}`, true);
        xhr.onload = function() {
            const cont = document.getElementById('chatListCont');
            while (cont.firstChild) {
                cont.removeChild(cont.firstChild);
            }

            const p = document.createElement('p');
            p.innerHTML = 'Wyniki:';
            p.style = "color: #969696; width: auto;";
            cont.appendChild(p);

            if (xhr.responseText) {
                const data = JSON.parse(xhr.responseText);
                for (const chat of data['0']) {
                    const row = document.createElement('div');
                    row.className = 'chat-res-card shadow';
                    row.onclick = function() {
                        send_req_and_reload('enter-chat', chat.id)
                    }
                    const img = document.createElement('img');
                    img.className = 'img-fluid rounded';
                    img.src = chat.img;
                    const col = document.createElement('div');
                    col.className = 'd-flex flex-column';
                    const h6 = document.createElement('h6');
                    h6.innerHTML = chat.name;
                    col.appendChild(h6);
                    usrs = document.createElement('h6');
                    usrs.style = 'color: #969696;';
                    usrs.innerHTML = `${chat.users} uczęstników`;
                    col.appendChild(usrs);
                    row.appendChild(img);
                    row.appendChild(col);
                    cont.appendChild(row);
                }
            } else {
                const c = document.createElement('div');
                c.innerHTML = `Brak wyników dla zapytania "${name}"`
                cont.appendChild(c);
            }

        }
        xhr.send();
    }
    
}


function accept_friend(id) {
    send_req_and_reload('accept-friend', id)
}

function reject_friend(id) {
    send_req_and_reload('reject-friend', id)
}

function ask_delete_friend(id, name) {
    if (confirm(`Czy chesz usunąć ${name} z listy przyjaciele?`))
        send_req_and_reload('delete-friend', id)
}

function ask_cancel_request(id, name) {
    if (confirm(`Czy chcesz anulować zapyt użytkowniky ${name} o dodaniu w przyjaciele?`))
        send_req_and_reload('cancel-request', id)
}



function ask_remove_member(group_id, user_id, name, group) {
    if (confirm(`Czy chcesz usunąć użytkownika ${name} z grupy ${group}?`))
        send_req_and_reload('remove-member', group_id, user_id);
}

function ask_delete_group(id, name) {
    if (confirm(`Czy chcesz usunąć grupę ${name} na stalo? To polecenie jest nieodwrotnym!`))
        if (prompt("Dla podtwierdzenia wprowadź nazwę grupy:") == name)
            send_req_and_go_home('delete-group', id)
}

function ask_leave_group(id, name) {
    if (confirm(`Czy chesz opuścić grupę ${name}?`)) {
        send_req_and_do_nothing('leave-group', id)
        window.location.assign('/')
        window.reload()
    }
}

function toggle_theme(btn) {
    const main_link = document.getElementById('mainThemeLink');
    const prof_link = document.getElementById('profileLink');
    html = document.getElementById('html');
    if ('light.css' === main_link.href.split('/')[5]) {
        html.setAttribute('data-bs-theme', 'dark')
        if (prof_link)
            prof_link.href = '/static/css/profile_dark.css'
        main_link.href = '/static/css/dark.css';
        btn.innerHTML = '<span></span>Ciemny';
        send_req_and_do_nothing('toggle-theme', 'dark')

    } else {
        html.setAttribute('data-bs-theme', 'light')
        if (prof_link)
            prof_link.href = '/static/css/profile_light.css'
        main_link.href = '/static/css/light.css';
        btn.innerHTML = '<span></span>Jasny';
        send_req_and_do_nothing('toggle-theme', 'light')
    }
}



u_s = document.getElementById('user_search')
if (u_s) {
    u_s.addEventListener('keyup', function(event) {
        if (event.key === 'Enter') {
            search_user()
        }
    });
}
    
document.getElementById('chat_search').addEventListener('keyup', function(event) {
    if (event.key === 'Enter') {
        search_chat()
    }
});


