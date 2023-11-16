document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-content");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");

    function addMessage(message, sender) {
        const messageDiv = document.createElement("div");
        messageDiv.className = sender === "user" ? "message user" : "message assistant";
        messageDiv.textContent = message;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    sendButton.addEventListener("click", function () {
        const userMessage = userInput.value;
        if (userMessage.trim() !== "") {
            addMessage(userMessage, "user");
    
            fetch("http://127.0.0.1:9000/api/sentiment_analisys", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    phrase: userMessage,
                }),
            })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then((data) => {
                    const botMessage = data.analisys_message;
                    addMessage(botMessage, "assistant");
                })
                .catch((error) => {
                    if (error.message.includes("400")) {
                        addMessage("Não pude compreender a frase, poderia reescrevê-la por gentileza?", "assistant");
                    } else {
                        console.error("Erro na chamada à API:", error);
                    }
                });
    
            userInput.value = "";
        }
    });

    userInput.addEventListener("keyup", function (event) {
        if (event.key === "Enter") {
            sendButton.click();
        }
    });
});