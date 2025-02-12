document.addEventListener('DOMContentLoaded', function() {
    const chatWidget = document.querySelector('.chat-widget');
    const chatbotLogo = document.querySelector('.chatbot-logo');
    const welcomePopup = document.querySelector('.welcome-popup');
    const closePopupBtns = document.querySelectorAll('.close-popup');
    const messagesContainer = document.querySelector('.chat-messages');
    const textarea = document.querySelector('.chat-input textarea');
    const sendBtn = document.querySelector('.chat-input button');

    // Show welcome popup after 3 seconds
    setTimeout(() => {
        welcomePopup.classList.add('show');
    }, 3000);

    // Close popup when clicking the close button
    closePopupBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            if (e.target.closest('.welcome-popup')) {
                welcomePopup.classList.remove('show');
            } else if (e.target.closest('.chat-widget')) {
                chatWidget.classList.remove('open');
            }
        });
    });

    // Toggle chatbot when clicking the logo
    chatbotLogo.addEventListener('click', () => {
        chatWidget.classList.toggle('open');
        welcomePopup.classList.remove('show');
        if (chatWidget.classList.contains('open')) {
            textarea.focus();
        }
    });

    // Function to auto-resize textarea
    function autoResize() {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    }

    // Function to add a message to the chat
    function addMessage(message, type) {
        const messageElement = document.createElement('div');
        messageElement.className = `message ${type}-message`;
        
        if (type === 'bot' && message.includes('Order Invoice')) {
            const formattedMessage = message.replace(/\n/g, '<br>');
            messageElement.innerHTML = `<pre>${formattedMessage}</pre>`;
        } else {
            messageElement.textContent = message;
        }
        
        messagesContainer.appendChild(messageElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    function showTypingIndicator() {
        const indicator = document.querySelector('.typing-indicator');
        indicator.classList.add('active');
    }

    function hideTypingIndicator() {
        const indicator = document.querySelector('.typing-indicator');
        indicator.classList.remove('active');
    }

    // Function to send message to backend and get response
    async function sendMessage() {
        const message = textarea.value.trim();
        if (!message) return;

        addMessage(message, 'user');
        textarea.value = '';
        autoResize();

        showTypingIndicator();
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ input: message })
            });

            if (!response.ok) throw new Error('Network response was not ok');

            const data = await response.json();
            hideTypingIndicator();
            
            let formattedResponse = data.response;
            if (formattedResponse.includes('Order Invoice')) {
                formattedResponse = formattedResponse
                    .replace(/-----------------------------/g, '─'.repeat(35))
                    .replace(/ {2,}/g, ' ')
                    .trim();
            }
            
            addMessage(formattedResponse, 'bot');

        } catch (error) {
            console.error('Error:', error);
            hideTypingIndicator();
            addMessage('Sorry, I am unable to process your request right now.', 'bot');
        }
    }

    // Event listeners
    textarea.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            if (e.shiftKey) {
                // Let the new line happen
                return;
            } else {
                e.preventDefault();
                sendMessage();
            }
        }
    });

    textarea.addEventListener('input', autoResize);
    sendBtn.addEventListener('click', sendMessage);

    // Add hover functionality for chatbot logo
    chatbotLogo.addEventListener('mouseenter', () => {
        if (!welcomePopup.classList.contains('show')) {
            welcomePopup.classList.add('show');
        }
    });

    chatbotLogo.addEventListener('mouseleave', () => {
        const timeElapsed = Date.now() - performance.timing.navigationStart;
        if (timeElapsed > 3000) {
            welcomePopup.classList.remove('show');
        }
    });
});