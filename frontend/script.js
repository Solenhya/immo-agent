const form = document.getElementById('chatForm');
const input = document.getElementById('userInput');
const chatbox = document.getElementById('chatbox');
const typingIndicator = document.getElementById('typingIndicator');

marked.setOptions({
    breaks: true,
    gfm: true
});

function addMessage(content, isUser) {
    const div = document.createElement('div');
    div.className = `message ${isUser ? 'user-message' : 'ai-message'}`;
    
    // Parse markdown if it's AI
    const htmlContent = isUser ? `<p>${escapeHTML(content)}</p>` : marked.parse(content);
    
    div.innerHTML = `
        <div class="avatar">${isUser ? '👤' : '🤖'}</div>
        <div class="message-content">${htmlContent}</div>
    `;
    
    chatbox.appendChild(div);
    chatbox.scrollTop = chatbox.scrollHeight;
}

function escapeHTML(str) {
    return str.replace(/[&<>'"]/g, 
        tag => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            "'": '&#39;',
            '"': '&quot;'
        }[tag])
    );
}

// Gestion de l'authentification
async function handleLogin() {
    const emailInput = document.getElementById('emailInput');
    const email = emailInput.value.trim();
    const loginBtn = document.getElementById('loginBtn');
    
    if (!email) return alert("Veuillez entrer une adresse e-mail.");
    
    loginBtn.disabled = true;
    loginBtn.innerText = "Connexion...";

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email })
        });
        
        if (response.ok) {
            document.getElementById('authOverlay').style.opacity = '0';
            setTimeout(() => {
                document.getElementById('authOverlay').style.display = 'none';
            }, 500);
            addMessage("Bienvenue ! Je suis prêt à répondre à vos questions sur l'immobilier.", false);
        } else {
            alert("Erreur lors de la connexion. Veuillez réessayer.");
        }
    } catch (err) {
        alert("Impossible de contacter le serveur d'authentification.");
    } finally {
        loginBtn.disabled = false;
        loginBtn.innerText = "Ouvrir la session";
    }
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;

    addMessage(text, true);
    input.value = '';
    
    // Disable input while loading
    input.disabled = true;
    typingIndicator.classList.remove('hidden');

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });
        
        const data = await response.json();
        addMessage(data.reply, false);
    } catch (err) {
        addMessage("⚠️ Une erreur réseau est survenue. L'agent est injoignable.", false);
    } finally {
        input.disabled = false;
        input.focus();
        typingIndicator.classList.add('hidden');
    }
});
