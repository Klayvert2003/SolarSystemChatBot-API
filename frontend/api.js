document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-content");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");
    const dangerButton = document.getElementById("danger-button");

    const date_today = new Date();

    const start_date = new Date();
    start_date.setDate(start_date.getDate() - 1);

    function formatarData(data) {
        const ano = data.getFullYear();
        const mes = String(data.getMonth() + 1).padStart(2, '0'); // Adiciona zero à esquerda, se necessário
        const dia = String(data.getDate()).padStart(2, '0'); // Adiciona zero à esquerda, se necessário
        return `${ano}-${mes}-${dia}`;
    }

    dangerButton.addEventListener("click", function () {
        const apiUrl = "http://127.0.0.1:9000/api/verify-danger";
    
        const requestData = {
            start_date: formatarData(start_date),
            end_date: formatarData(date_today)
        };
    
        const requestOptions = {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(requestData)
        };
    
        fetch(apiUrl, requestOptions)
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`Erro na requisição: ${response.status} ${response.statusText}`);
                }
                return response.json();
            })
            .then((data) => {
                console.log(data);

                const response = data.response;

                let infoHtml = '';

                for (let i = 0; i < response.length; i++) {
                    const sateliteName = response[i].satelite_name;
                    const warningMessage = response[i].warning_message;

                    infoHtml += `
                        <div>
                            <p>Satélite: ${sateliteName}, perigo: ${warningMessage}</p>
                        </div>
                    `;
                }

                const dangerInfoContainer = document.getElementById('danger-info');
                dangerInfoContainer.innerHTML = infoHtml;
                dangerInfoContainer.style.display = 'block';
            })
            .catch((error) => {
                console.error(error);
            });
    });

    function addMessage(message, sender) {
        const messageDiv = document.createElement("div");
        messageDiv.className = sender === "user" ? "message user" : "message assistant";
        messageDiv.textContent = message;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Event listener para o botão de envio
    sendButton.addEventListener("click", function () {
        const userMessage = userInput.value;
        if (userMessage.trim() !== "") {
            addMessage(userMessage, "user");

            // Faça a chamada à API local usando fetch
            fetch("http://127.0.0.1:9000/api/chat-bot", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    question: userMessage,
                }),
            })
                .then((response) => response.json())
                .then((data) => {
                    const botMessage = data.response;
                    addMessage(botMessage, "assistant");
                })
                .catch((error) => {
                    console.error("Erro na chamada à API:", error);
                });

            userInput.value = "";
        }
    });

    // Lidar com a tecla Enter para enviar a mensagem
    userInput.addEventListener("keyup", function (event) {
        if (event.key === "Enter") {
            sendButton.click();
        }
    });
});