document.addEventListener('DOMContentLoaded', function() {
    const chatWidget = document.querySelector('.chat-widget');
    const chatbotLogo = document.querySelector('.chatbot-logo');
    const welcomePopup = document.querySelector('.welcome-popup');
    const closePopupBtns = document.querySelectorAll('.close-popup');
    
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
    });

    // Send message functionality
    const input = document.querySelector('.chat-input input');
    const sendBtn = document.querySelector('.chat-input button');

    function sendMessage() {
        const message = input.value.trim();
        if (message) {
            const messagesContainer = document.querySelector('.chat-messages');
            const userMessage = document.createElement('div');
            userMessage.className = 'message user-message';
            userMessage.textContent = message;
            messagesContainer.appendChild(userMessage);
            input.value = '';
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    }

    sendBtn.addEventListener('click', sendMessage);
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });




    // Add hover functionality for chatbot logo
    chatbotLogo.addEventListener('mouseenter', () => {
        // Only show popup if it's not already visible
        if (!welcomePopup.classList.contains('show')) {
            welcomePopup.classList.add('show');
        }
    });

    // Optional: Hide popup when mouse leaves the chatbot logo
    chatbotLogo.addEventListener('mouseleave', () => {
        // Only hide if the popup wasn't shown by the initial 3-second timer
        // Get the current time and check if 3 seconds have passed since page load
        const timeElapsed = Date.now() - performance.timing.navigationStart;
        if (timeElapsed > 3000) {
            welcomePopup.classList.remove('show');
        }
    });
});