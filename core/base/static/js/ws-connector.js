let roomId = document.getElementById('room').value
let url = `ws://${(window.location.host)}/ws/socket-server/${roomId}`
const chatSocket = new WebSocket(url)
const currentUser = document.getElementById('user').value
console.log(roomId)
chatSocket.onmessage = function(e){
    let data = JSON.parse(e.data)
    if(data.type === 'chat'){
        const chatLog = document.querySelector('#chat-log-row')
        const divSelf = document.createElement('div')
        const divOther = document.createElement('div')
        const link = document.createElement('a')
        const drop = document.createElement('ul')
        divSelf.classList.add('col-6', 'd-flex', 'justify-content-end')
        divOther.classList.add('col-6', 'd-flex')
        link.classList.add('btn', 'mt-2')
        drop.classList.add('dropdown-menu', 'dropdown-menu-left')
        link.textContent = data.message;
        link.href = '#';
        link.setAttribute('data-bs-toggle', 'dropdown');
        console.log(data.user)
        if (currentUser == data.user){
            link.classList.add('self-message', 'btn-primary')
            divSelf.appendChild(link)
            divSelf.appendChild(drop)
        }
        else {
            link.classList.add('other-message', 'btn-light')
            divOther.appendChild(link)
            divOther.appendChild(drop)
        }
        chatLog.appendChild(divOther)
        chatLog.appendChild(divSelf)
        scrollToBottom()
    }
}
let form = document.getElementById('form')
form.addEventListener('submit', (e)=>{
    e.preventDefault()
    let message = e.target.message.value
    let user = e.target.user.value
    let room = e.target.room.value
    chatSocket.send(JSON.stringify({
        'message': message,
        'user': user,
        'room': room
    }))
    form.reset()
})