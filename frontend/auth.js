// Fonction pour se connecter
async function login(email) {
    const response = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email })
    });
    const data = await response.json();
    if(data.status === "success") {
        console.log("Connecté ! Le cookie est maintenant dans le navigateur.");
    }
}

// Fonction d'envoi de message (Le navigateur enverra le cookie automatiquement)
async function sendMessage(text) {
    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text }) // Pas besoin d'envoyer l'ID, il est dans le cookie !
    });
    
    if (response.status === 401) {
        alert("Veuillez vous connecter d'abord.");
        return;
    }
    
    const data = await response.json();
    return data.reply;
}
