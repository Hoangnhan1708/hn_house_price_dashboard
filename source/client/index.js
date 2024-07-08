
const inputBox = document.getElementById('input');
const messageHistory = document.querySelector('.message-history')

var listMessage= [
    
];



const handleSubmit = async () => {
    const clientMessage = inputBox.value.trim();
    if (clientMessage === '') return;

    const newRequest = {
        type: "client",
        content: clientMessage
    };
    listMessage.push(newRequest);
    inputBox.value = '';
    renderListMessage(listMessage);

    try {
        const response = await fetch('http://localhost:3000/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ content: clientMessage }),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const responseData = await response.json();
        const chatGptResponse = responseData.content;

        const newResponse = {
            type: "server",
            content: chatGptResponse
        };
        listMessage.push(newResponse);
        renderListMessage(listMessage);

    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
    }
};

const handleEnter = (event) =>{
    if (event.key === 'Enter') {
        handleSubmit();
    }
}

const renderListMessage = (listMessage)=>{
    messageHistory.innerHTML = ""
    listMessage.map((item) => {
        if(item.type === "client"){
            messageHistory.innerHTML += 
                    `<div class="message-item ${item.type}">
                        <p>${item.content}</p>
                    </div>`;
        }
        else{
            messageHistory.innerHTML += 
            `<div class="message-item server">
            <img class="model-icon" src="./assets/gemini-icon.png" alt="gemini icon">
            <p>${item.content}</p>
        </div>`;
        }
    });
}

renderListMessage(listMessage);    