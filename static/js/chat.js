function onLoad() {
    const messagesContainer = document.getElementById('messages-container');
    let messageInput = document.getElementById('message')
    let submitButton = document.getElementById('send-message')
    let form = document.getElementById('chat-form')

    // Scroll inicial al último mensaje
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    // Manejar los botones de acceso rápido
    const buttons = document.getElementsByClassName('btn-shortcut');
    Array.from(buttons).forEach(button => {
        button.addEventListener('click', function() {
            messageInput.value = this.value;
        });
    });

    // Manejar envío con Enter
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            document.getElementById('send-message').click();
        }
    });

    
    // Escuchar cambios en el input de texto para habilitar/deshabilitar el botón de enviar
    messageInput.addEventListener('input', (event) => {
        if (event.target.value.length > 0) {
            submitButton.classList.remove('disabled')
        } else {
            submitButton.classList.add('disabled')
        }
    })

    // Mostrar loading al enviar
    form.addEventListener('submit', function(event) {
        document.querySelector('.loading-overlay').style.display = 'flex';

        //envío por ajax
        event.preventDefault()
        const formData = new FormData(this)
        sendMessage(formData)
    });
    
    // Función para manejar la lógica de envío de mensajes
    async function sendMessage(formData) {
        submitButton.classList.add('disabled')
        messageInput.classList.add('disabled')
        submitButton.innerText = 'Enviando...'

        addMessageToChat({
            content: formData.get('message'),
            author: 'user',
        })
        
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
               'Accept': 'application/json',
            },
            body: formData,
        })

        const message = await response.json()
        addMessageToChat(message)
        messageInput.value = ''
        messageInput.classList.remove('disabled')
        submitButton.classList.remove('disabled')
        submitButton.innerText = 'Enviar'
        document.querySelector('.loading-overlay').style.display = 'none';
    }
    

    function addMessageToChat(message) {
        let messageHTML = ''

        if (message.author === 'assistant') {
            messageHTML = `
                <div class="d-flex flex-row justify-content-start mb-4">
                    <img src="/static/pixelart_logo.png" alt="avatar 1" >
                    <div class="p-3 ms-3 message-assistant">
                        <p class="small mb-0">${message.content}</p>
                    </div>
                </div>
            `;
        } else {
            messageHTML = `
                <div class="d-flex flex-row justify-content-end mb-4">
                    <div class="p-3 me-3 message-user" >
                        <p class="small mb-0">${message.content}</p>
                    </div>
                </div>
            `
        }

        document.getElementById('messages-container').insertAdjacentHTML('beforeend', messageHTML)

        // Scroll suave hacia el último mensaje
        const lastMessage = document.getElementById('messages-container').lastElementChild;
        lastMessage.scrollIntoView({ behavior: 'smooth' });
    }

    

    
}

document.addEventListener('DOMContentLoaded', onLoad)