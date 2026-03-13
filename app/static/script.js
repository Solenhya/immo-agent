const form = document.getElementById('chatForm');
const input = document.getElementById('userInput');
const chatbox = document.getElementById('chatbox');
const typingIndicator = document.getElementById('typingIndicator');
let conversation;
conversation = [];
marked.setOptions({
    breaks: true,
    gfm: true
});

function getConversationIdFromUrl() {
    const match = window.location.pathname.match(/\/conversation\/([^/]+)/);
    return match ? decodeURIComponent(match[1]) : null;
}

function getConversationIdFromTemplate() {
    const templateConversationId = chatbox?.dataset?.conversationId;
    if (!templateConversationId || templateConversationId === 'None') {
        return null;
    }
    return String(templateConversationId);
}

async function load_conversation(conversation_id){
    try{
        const response = await fetch(`/api/conversations/${conversation_id}`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) {
            throw new Error(`Erreur API: ${response.status}`);
        }
        const result = await response.json();
        const retour = result["messages"]
        return retour;
    }catch(err){
        console.error('Impossible de charger la conversation:', err);
        return null;
    }
    finally{

    }
}

document.addEventListener('DOMContentLoaded', async () => {
    const conversationId = getConversationIdFromTemplate() || getConversationIdFromUrl();
    if (!conversationId) {
        return;
    }

    const data = await load_conversation(conversationId);
    if (!data) {
        return;
    }

    conversation = data;
    show_conversations();
});

async function show_conversations(){
    console.log(conversation)
    for (let i = 0; i < conversation.length; i++) {
        let isUser=false
        if (conversation[i]["role"]=="user"){
            isUser=true
        }
        addMessage(conversation[i]["content"],isUser)
}

}

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
        const conversationId = getConversationIdFromTemplate() || getConversationIdFromUrl();
        const payload = { message: text };
        if (conversationId) {
            payload.conversation_id = conversationId;
        }else{
            console.log("Erreur conversationId vide")
            console.log(conversationId)
        }

        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        const data = await response.json();
        addMessage(data["message"], false);
    } catch (err) {
        addMessage("⚠️ Une erreur réseau est survenue. L'agent est injoignable.", false);
    } finally {
        input.disabled = false;
        input.focus();
        typingIndicator.classList.add('hidden');
    }
});
