const conversationList = document.getElementById('conversationList');
const newConversationBtn = document.getElementById('newConversationBtn');

function formatConversationLabel(conversationId) {
    return `Conversation ${conversationId}`;
}

function renderConversations(conversations) {
    conversationList.innerHTML = '';

    if (!Array.isArray(conversations) || conversations.length === 0) {
        const emptyState = document.createElement('div');
        emptyState.className = 'empty-state';
        emptyState.textContent = 'Aucune conversation pour le moment.';
        conversationList.appendChild(emptyState);
        return;
    }

    conversations.forEach((conversationId) => {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'conversation-item';
        button.dataset.conversationId = conversationId;

        const title = document.createElement('span');
        title.className = 'conversation-title';
        title.textContent = formatConversationLabel(conversationId);

        const meta = document.createElement('span');
        meta.className = 'conversation-meta';
        meta.textContent = conversationId;

        button.appendChild(title);
        button.appendChild(meta);

        button.addEventListener('click', () => {
            window.location.href = `/conversation/${conversationId}`;
        });

        conversationList.appendChild(button);
    });
}

async function loadConversations() {
    try {
        const response = await fetch('/api/user/conversations', {
            credentials: 'same-origin'
        });

        if (!response.ok) {
            throw new Error(`Erreur HTTP ${response.status}`);
        }

        const data = await response.json();
        const conversations = Array.isArray(data?.conversations) ? data.conversations : [];
        renderConversations(conversations);
    } catch (error) {
        console.error('Impossible de charger les conversations:', error);
        conversationList.innerHTML = '';

        const emptyState = document.createElement('div');
        emptyState.className = 'empty-state';
        emptyState.textContent = 'Impossible de charger les conversations.';
        conversationList.appendChild(emptyState);
    }
}

newConversationBtn.addEventListener('click', () => {
    window.location.href = '/conversation';
});

loadConversations();
