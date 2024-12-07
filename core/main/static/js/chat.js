document.addEventListener('DOMContentLoaded', function () {
    const chatbox = document.querySelector(".chatbox");
    const chatInput = document.getElementById("user-input");
    const sendChatBtn = document.getElementById("send-btn");
    const closeBtn = document.querySelector(".close-btn");
    const chatbotToggler = document.querySelector(".chatbot-toggler");

    // Define intents (replace with your actual intents)
    const intents = [
        {
            "tag": "greeting",
            "patterns": [
                "Hi",
                "Hey",
                "How are you",
                "Is anyone there?",
                "Hello",
                "Good day"
            ],
            "responses": [
                "Barev dzez,es BMW-ist Albertn em",
                "Barev dzez,es Albertn em,ev asem vor Mercedes-y avto chi !!!",
                "Barev dzez,es Albertn em,ev ayo es LEGEND em",
                "Barev dzez,es Albertn em,Python cragravorox"
            ]
        },
        {
            "tag": "goodbye",
            "patterns": ["Bye", "See you later", "Goodbye"],
            "responses": [
                "See you later, thanks for visiting",
                "Have a nice day",
                "Bye! Come back again soon."
            ]
        },
        {
            "tag": "thanks",
            "patterns": ["Thanks", "Thank you", "That's helpful", "Thank's a lot!"],
            "responses": ["Happy to help!", "Any time!", "My pleasure"]
        },
        {
            "tag": "items",
            "patterns": [
                "Which items do you have?",
                "What kinds of items are there?",
                "What do you sell?"
            ],
            "responses": [
                "We sell electrical equipment",
            ]
        },
        {
            "tag": "payments",
            "patterns": [
                "Do you take credit cards?",
                "Do you accept Mastercard?",
                "Can I pay with Paypal?",
                "Are you cash only?"
            ],
            "responses": [
                "We accept VISA, Mastercard and Paypal",
                "We accept most major credit cards, and Paypal"
            ]
        },
        {
            "tag": "delivery",
            "patterns": [
                "How long does delivery take?",
                "How long does shipping take?",
                "When do I get my delivery?"
            ],
            "responses": [
                "Delivery takes 2-4 days",
                "Shipping takes 2-4 days"
            ]
        }
    ];

    // Function to create chat message <li> element
    const createChatLi = (message, className) => {
        const chatLi = document.createElement("li");
        chatLi.classList.add("chat", className);

        // Add image (adjust imgTag.src to your actual chatbot image)
        const imgTag = document.createElement("img");
        imgTag.src = "https://i.ibb.co/qWsG1cJ/image.png.com"; // Placeholder image URL
        imgTag.alt = className === "outgoing" ? "user avatar" : "chatbot avatar"; // Adjust alt text as needed
        imgTag.style.width = "40px"; // Example styling
        imgTag.style.height = "40px"; // Example styling
        chatLi.appendChild(imgTag);

        // Add message text
        const messageP = document.createElement("p");
        messageP.textContent = message;
        chatLi.appendChild(messageP);

        return chatLi;
    };

    // Function to generate a response based on user input or button click
    const generateResponse = (message) => {
        // Find intent by message or tag
        const intent = intents.find(intent => {
            // Check if message matches any pattern in intents
            if (intent.patterns.some(pattern => message.toLowerCase().includes(pattern.toLowerCase()))) {
                return true;
            }
            // Check if intent tag matches message
            return intent.tag === message;
        });

        if (intent) {
            // Choose a random response from matched intent
            const responses = intent.responses;
            const response = responses[Math.floor(Math.random() * responses.length)];

            // Add chat message to chatbox
            chatbox.appendChild(createChatLi(response, "incoming"));
            chatbox.scrollTo(0, chatbox.scrollHeight);
        } else {
            // Default response if no intent is matched
            const responseMessage = "Sorry, I'm not sure how to respond to that.";
            chatbox.appendChild(createChatLi(responseMessage, "incoming"));
            chatbox.scrollTo(0, chatbox.scrollHeight);
        }
    };

    // Handle user clicking send button or pressing Enter key
    const handleChat = () => {
        const userMessage = chatInput.value.trim();
        if (!userMessage) return;

        chatInput.value = "";
        chatbox.appendChild(createChatLi(userMessage, "outgoing"));
        chatbox.scrollTo(0, chatbox.scrollHeight);

        // Generate response based on user input
        generateResponse(userMessage);
    };

    // Attach event listener to send button
    sendChatBtn.addEventListener("click", handleChat);

    // Attach event listener to Enter key press in chatInput
    chatInput.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            handleChat();
        }
    });

    // Attach event listeners to each chat button
    const chatButtons = document.querySelectorAll(".chat-btn");
    chatButtons.forEach(button => {
        button.addEventListener("click", function () {
            const question = this.getAttribute("data-question");
            generateResponse(question); // Pass question as message to generate response
        });
    });

    // Other existing code (chatbot toggler, close button) should remain as is.

    // Chatbot toggler button click listener
    chatbotToggler.addEventListener("click", () => {
        document.body.classList.toggle("show-chatbot");
        if (document.body.classList.contains("show-chatbot")) {
            generateResponse("Hello");
        }
    });

    // Close button click listener
    closeBtn.addEventListener("click", () => {
        document.body.classList.remove("show-chatbot");
        // Clear chatbox when closing chatbot
        chatbox.innerHTML = "";
    });

    // Adjust textarea height as user types
    chatInput.addEventListener("input", () => {
        chatInput.style.height = "auto";
        chatInput.style.height = `${chatInput.scrollHeight}px`;
    });

});