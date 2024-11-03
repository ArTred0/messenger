function send_req_and_reload(url) {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.onload = function() {
        window.location.reload()
    }
    xhr.send();
}

function send_req_and_go_home(url) {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.onload = function() {
        window.location.assign('/');
    }
    xhr.send();
}

function send_req_and_do_nothing(url) {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.send();
}

function send_req_and_do_sth(url, func=function(){}) {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.onload = function() {
        func(JSON.parse(xhr.response))
    }
    xhr.send();
}


function post_data(url, data, csrf, func=function(){}) {    
    const xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.setRequestHeader("X-CSRFToken", csrf);
    xhr.onload = function() {
        func(JSON.parse(xhr.response))
    }
    xhr.send(JSON.stringify(data));
}


function render_new_messages(data) {
    const user = document.getElementById('sender_name').value;
    if (data) {
        for (message of data['0']) {
            if (message['nadawca']['imie'] != user) {
                if (document.getElementsByTagName('main')[0].getElementsByClassName('all-center')) {
                    document.getElementsByTagName('main')[0].removeChild(document.getElementsByTagName('main')[0].getElementsByClassName('all-center')[0])
                }
                const div1 = document.createElement('div');
                div1.className = 'd-flex message flex-row-reverse';
                const div2 = document.createElement('div');
                div2.className = 'message-body shadow-sm';
                div2.onclick = function() {
                    change_message(div2);
                };
                const ms_id = document.createElement('input');
                ms_id.type = 'hidden';
                ms_id.value = message['id'];
                const p = document.createElement('p');
                p.innerHTML = message['tekst'];
                const time_div = document.createElement('div');
                time_div.className = 'time-sended time-sended';
                const time_sended = document.createElement('p');
                time_sended.innerHTML = message['czas_wysylki'];
                time_div.appendChild(time_sended)
                div2.appendChild(ms_id);
                div2.appendChild(p);
                div2.appendChild(time_div);
                div1.appendChild(div2);
                document.getElementsByTagName('main')[0].appendChild(div1);
            }
        }
    }
}



function render_sended(message) {
    if (document.getElementsByTagName('main')[0].getElementsByClassName('all-center')) {
        document.getElementsByTagName('main')[0].removeChild(document.getElementsByTagName('main')[0].getElementsByClassName('all-center')[0])
    }
    console.log(message)
    const div1 = document.createElement('div');
    div1.className = 'd-flex message flex-row-reverse';
    const div2 = document.createElement('div');
    div2.className = 'my-message-body shadow-sm';
    div2.onclick = function() {
        change_message(div2);
    };
    const ms_id = document.createElement('input');
    ms_id.type = 'hidden';
    ms_id.value = message['id'];
    const p = document.createElement('p');
    p.innerHTML = message['tekst'];
    const time_div = document.createElement('div');
    time_div.className = 'time-sended my-time-sended';
    const time_sended = document.createElement('p');
    time_sended.innerHTML = message['czas_wysylki'];
    time_div.appendChild(time_sended)
    div2.appendChild(ms_id);
    div2.appendChild(p);
    div2.appendChild(time_div);
    div1.appendChild(div2);
    document.getElementsByTagName('main')[0].appendChild(div1);
}



function send_message(text) {
    if (text) {
        const data = {
            'tekst': text
        };
        post_data(
            `/site/js/api/send-message/`,
            data,
            document.getElementsByName('csrfmiddlewaretoken')[2].value,
            render_sended    
        );
        document.getElementById('message_input').value = '';
        // render_sended(resp);
    }
}


function change_message(message) {
    const answ = confirm('Usunąć wiadomość - OK?\nZmienić tekst - Cancel');
    if (answ) {
        send_req_and_reload(`/site/js/api/delete-message/${message.querySelector('input').value}`);
    } else {
        const ms = document.getElementsByClassName('changing')[0];
        console.log(ms)
        if (ms) {
            console.log(ms);
            const p = document.createElement('p');
            p.innerHTML = ms.querySelector('.text-change-inp').value;
            ms.className = 'my-message-body shadow-sm';
            ms.onclick = function() {
                change_message(ms)
            };
            ms.replaceChild(p, ms.querySelector('.text-change-inp'));
        }
        const input = document.createElement('input');
        input.addEventListener('keyup', function(event) {
            if (event.key === 'Enter') {
                change_message_text(message);
            }
        });
        input.className = 'form-control text-change-inp';
        input.value = message.querySelector('p').innerHTML;
        message.onclick = null;
        message.className = 'my-message-body shadow-sm changing';
        message.replaceChild(input, message.querySelector('p'));
    }
}

function change_message_text(message) {
    const inp = message.querySelector('.text-change-inp')
    const p = document.createElement('p')
    p.innerHTML = inp.value;
    message.replaceChild(p, inp);
    const data = {
        'ms_id': message.querySelector('input').value,
        'new_text': inp.value
    }
    post_data(
        '/site/js/api/change-message/',
        data,
        document.getElementsByName('csrfmiddlewaretoken')[2].value)
    // send_req_and_do_nothing(`/site/js/api/change-message`)
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
        xhr.open("GET", `/site/js/api/search-user/${username}`, true);
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
        xhr.open("GET", `/site/js/api/search-chat/${name}`, true);
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
    send_req_and_reload(`/site/js/api/accept-friend/${id}`)
}

function reject_friend(id) {
    send_req_and_reload(`/site/js/api/reject-friend/${id}`)
}

function ask_delete_friend(id, name) {
    if (confirm(`Czy chesz usunąć ${name} z listy przyjaciele?`))
        send_req_and_reload(`/site/js/api/delete-friend/${id}`)
}

function ask_cancel_request(id, name) {
    if (confirm(`Czy chcesz anulować zapyt użytkowniky ${name} o dodaniu w przyjaciele?`))
        send_req_and_reload(`/site/js/api/cancel-request/${id}`)
}



function ask_remove_member(group_id, user_id, name, group) {
    if (confirm(`Czy chcesz usunąć użytkownika ${name} z grupy ${group}?`))
        send_req_and_reload(`/site/js/api/remove-member/${group_id}/${user_id}`);
}

function ask_delete_group(id, name) {
    if (confirm(`Czy chcesz usunąć grupę ${name} na stalo? To polecenie jest nieodwrotnym!`))
        if (prompt("Dla podtwierdzenia wprowadź nazwę grupy:") == name)
            send_req_and_go_home(`/site/js/api/delete-group/${id}`)
}

function ask_leave_group(id, name) {
    if (confirm(`Czy chesz opuścić grupę ${name}?`)) {
        send_req_and_do_nothing(`/site/js/api/leave-group/${id}`)
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


if (window.location.pathname == '/') {
    document.getElementById('message_input').addEventListener('keyup', function(event) {
        if (event.key == 'Enter') {
            send_message(document.getElementById('message_input').value)
        }
    });

    interval = setInterval(() => {
        send_req_and_do_sth(
            `/site/js/api/check-new-messages/${document.getElementsByClassName('message').length}`,
            render_new_messages)
    }, 3000)
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



