function delete_message(message) {
    let answ = confirm('Chcesz usunąć tą wiadomość?');
    console.log(answ)
    if (answ) {
        const xhr = new XMLHttpRequest();
        const id = message.querySelector('input').value
        xhr.open("GET", `delete_message/${id}`, true);
        xhr.onload = function() {
            window.location.reload();
        }
        xhr.send();

    }
}