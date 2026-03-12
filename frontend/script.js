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
