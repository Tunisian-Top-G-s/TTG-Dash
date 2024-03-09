document.addEventListener("DOMContentLoaded", function() {
    // Select all toggle buttons
    const toggleButtons = document.querySelectorAll('.toggle-button');

    // Add click event listener to each toggle button
    toggleButtons.forEach(function(toggleButton) {
        toggleButton.addEventListener('click', function() {
            const parentGroup = toggleButton.closest('.text-group');
            const channelsList = parentGroup.querySelector('.channels-list');
            const toggleButtonIcon = toggleButton.querySelector('svg');

            // Toggle channels visibility
            channelsList.classList.toggle('hidden');
            if (channelsList.classList.contains('hidden')) {
                toggleButtonIcon.innerHTML = `<path d="m6 9 6 6 6-6"></path>`;
            } else {
                toggleButtonIcon.innerHTML = `<path d="m6 15 6-6 6 6"></path>`;
            }
        });

        // Find the add-channel button relative to the parent text-group
        const parentGroup = toggleButton.closest('.text-group');
        const addChannelButton = parentGroup.querySelector('.add-channel');
        addChannelButton.addEventListener('click', function() {
            const channelsList = parentGroup.querySelector('.channels-list');
            const newChannelName = prompt('Enter new channel name:');
            if (newChannelName) {
                addChannel(newChannelName, channelsList);
            }
        });
    });

    // Function to add a new channel to the list
    function addChannel(channelName, channelsList) {
        const newChannel = document.createElement('li');
        newChannel.className = 'channel-link';
        newChannel.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" data-lucide="hash" class="lucide lucide-hash"><line x1="4" x2="20" y1="9" y2="9"></line><line x1="4" x2="20" y1="15" y2="15"></line><line x1="10" x2="8" y1="3" y2="21"></line><line x1="16" x2="14" y1="3" y2="21"></line></svg> ${channelName}`;
        channelsList.appendChild(newChannel);
    }
});



document.addEventListener("DOMContentLoaded", function() {
    const changeStatusButtons = document.querySelectorAll('.change-status .status');
    const userProfile = document.querySelector('.user-profile');
    const changeStatusSection = document.querySelector('.change-status');
    const toggleButtonIcon = document.querySelector('.change-status-btn svg');

    // Toggle change-status section visibility when button is clicked
    document.querySelector('.change-status-btn').addEventListener('click', function() {
        changeStatusSection.classList.toggle('hidden');
        if (changeStatusSection.classList.contains('hidden')) {
            toggleButtonIcon.innerHTML = `<path d="m6 9 6 6 6-6"></path>`;
        } else {
            toggleButtonIcon.innerHTML = `<path d="m6 15 6-6 6 6"></path>`;
        }
    });

    // Add click event listener to each change status button
    changeStatusButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const status = button.classList[1]; // Get the second class which represents the status
            updateStatus(status);
            changeStatusSection.classList.add('hidden'); // Hide change-status section after selecting a status
            if (changeStatusSection.classList.contains('hidden')) {
                toggleButtonIcon.innerHTML = `<path d="m6 9 6 6 6-6"></path>`;
            } else {
                toggleButtonIcon.innerHTML = `<path d="m6 15 6-6 6 6"></path>`;
            }
        });
    });

    // Function to update user status
    function updateStatus(status) {
        const userStatus = userProfile.querySelector('.user-status-text');
        const userStatusIcon = userProfile.querySelector('.user-status');
        const statusText = userProfile.querySelector('.status-text');
        const statusIcons = userProfile.querySelectorAll('.status');
        
        // Remove 'active' class from all status icons
        statusIcons.forEach(icon => icon.classList.remove('active'));

        // Update user status and status text
        userStatus.textContent = status.charAt(0).toUpperCase() + status.slice(1); // Capitalize first letter
        statusText.textContent = status.charAt(0).toUpperCase() + status.slice(1);

        // Set background color based on status
        if (status === 'online') {
            userStatusIcon.style.backgroundColor = '#4CAF50'; // Green for Online
        } else if (status === 'away') {
            userStatusIcon.style.backgroundColor = '#FFC107'; // Yellow for Away
        } else if (status === 'busy') {
            userStatusIcon.style.backgroundColor = '#FF5722'; // Orange for Busy
        }

        // Add 'active' class to the clicked status icon
        userProfile.querySelector(`.status-${status}`).classList.add('active');
    }
});




document.addEventListener("DOMContentLoaded", function() {
    const changeStatusButtons = document.querySelectorAll('.change-status .status');

    // Add click event listener to each change status button
    changeStatusButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const status = button.classList[1]; // Get the second class which represents the status
            updateStatus(status);
        });
    });

    // Function to update user status
    function updateStatus(status) {
        const userStatusText = document.querySelector('.user-status-text');
        const userStatus = document.querySelector('.user-status');
        
        // Update user status and status text
        userStatusText.textContent = status.charAt(0).toUpperCase() + status.slice(1); // Capitalize first letter

        // Remove all existing status classes
        userStatus.classList.remove('online', 'away', 'busy');

        // Add the appropriate status class
        userStatus.classList.add(status);

        // Update background color based on status
        if (status === 'online') {
            userStatus.style.backgroundColor = '#2ECC71'; // Green for Online
        } else if (status === 'away') {
            userStatus.style.backgroundColor = '#FFC107'; // Yellow for Away
        } else if (status === 'busy') {
            userStatus.style.backgroundColor = '#FF5722'; // Orange for Busy
        }
    }
});

document.addEventListener("DOMContentLoaded", function() {
    const changeStatusButtons = document.querySelectorAll('.change-status-btn');
    const changeStatusSection = document.querySelector('.change-status');

    // Add click event listener to the toggle button
    changeStatusButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            changeStatusSection.classList.toggle('visible');
        });
    });
});


// SVGS
const SmileSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" data-lucide="smile" class="lucide lucide-smile"><circle cx="12" cy="12" r="10"></circle><path d="M8 14s1.5 2 4 2 4-2 4-2"></path><line x1="9" x2="9.01" y1="9" y2="9"></line><line x1="15" x2="15.01" y1="9" y2="9"></line></svg>`;
const ReplySvg = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" data-lucide="reply" class="lucide lucide-reply"><polyline points="9 17 4 12 9 7"></polyline><path d="M20 18v-2a4 4 0 0 0-4-4H4"></path></svg>`;

// Variable to store the current message being replied to
let currentReplyMessage = null;

// Function to send a message or a reply
function send() {
    // Get the user input
    var message = document.getElementById("userInput").value;

    if (message.trim() === "") {
        // If the message is empty, don't do anything
        return;
    }

    // If there is a currentReplyMessage, it means we are replying
    if (currentReplyMessage) {
        sendReplyMessage(message);
    } else {
        sendMessage(message);
    }
}

// Function to send a regular message
function sendMessage(message) {
    // Create a new message element
    var newMessage = createMessageElement("You", message);

    // Get the chat box and append the new message
    var chatBox = document.querySelector(".chat-box");
    chatBox.appendChild(newMessage);

    // Clear the input field after sending
    document.getElementById("userInput").value = "";
}

// Function to send a reply message
function sendReplyMessage(replyMessage) {
    // Create a new reply message element
    var newReplyMessage = document.createElement("div");
    newReplyMessage.classList.add("reply-message");

    // Message replied section
    var messageReplied = document.createElement("div");
    messageReplied.classList.add("message-replied");
    messageReplied.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="46" height="16" viewBox="0 0 46 16" fill="none">
            <path d="M1 15V15C1 7.26801 7.26801 1 15 1H45" stroke="#ADABAB" stroke-width="2"
                stroke-linecap="round" />
        </svg>
        <div class="user-pic">
            <img src="./assets/userpic.svg" alt="user-pic">
        </div>
        <div class="user-tag">@Figgy</div>
        <span>${currentReplyMessage}</span>
    `;

    // Chat message section
    var chatMessage = createMessageElement("You", replyMessage);

    newReplyMessage.appendChild(messageReplied);
    newReplyMessage.appendChild(chatMessage);

    // Get the chat box and append the new reply message
    var chatBox = document.querySelector(".chat-box");
    chatBox.appendChild(newReplyMessage);

    // Hide the "Replying to" section after sending the reply
    closeReplyMessage();

    // Clear the reply input field after sending
    document.getElementById("userInput").value = "";

    // Reset the current reply message
    currentReplyMessage = null;
}

// Function to create a message element
// Function to create a message element
function createMessageElement(userName, message) {
    var newMessage = document.createElement("div");
    newMessage.classList.add("chat-message");

    // Message header
    var messageHeader = document.createElement("div");
    messageHeader.classList.add("message-header");
    var userPic = document.createElement("div");
    userPic.classList.add("user-pic");
    userPic.innerHTML = '<img src="./assets/userpic.svg" alt="user-pic">';
    messageHeader.appendChild(userPic);

    // Message content
    var messageContent = document.createElement("div");
    messageContent.classList.add("message-content");
    var userInfo = document.createElement("div");
    userInfo.classList.add("user-info");
    userInfo.innerHTML = `<span class="user-name">${userName}</span>`;
    var messageDate = document.createElement("span");
    messageDate.classList.add("message-date");
    messageDate.innerText = "Today";
    var messageTime = document.createElement("span");
    messageTime.classList.add("message-time");
    var currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    messageTime.innerText = currentTime;
    userInfo.appendChild(messageDate);
    userInfo.appendChild(messageTime);
    messageContent.appendChild(userInfo);
    var messageText = document.createElement("div");
    messageText.classList.add("message-text");

    messageText.innerText = message;
    messageContent.appendChild(messageText);

    // Add the message header and content to the message element
    newMessage.appendChild(messageHeader);
    newMessage.appendChild(messageContent);

    // Reply and React section
    var replyReact = document.createElement("div");
    replyReact.classList.add("reply-react");
    var replyButton = document.createElement("button");
    replyButton.classList.add("reply");
    replyButton.onclick = function () {
        // Set the current reply message when this reply button is clicked
        currentReplyMessage = message;
        // Show the replying section
        showReplyingTo(message);
    };
    replyButton.innerHTML = ReplySvg;

    var reactButton = document.createElement("button");
    reactButton.classList.add("react");
    reactButton.innerHTML = SmileSvg;
    var ReactsAvailable = document.createElement("div");
    ReactsAvailable.classList.add("reacts-available");
    var reactionsList = ['😂', '😍', '👍', '👎', '😢', '😡'];
    reactionsList.forEach(function(react) {
        var reactSpan = document.createElement("span");
        reactSpan.innerText = react;
        reactSpan.onclick = function() {
            addReact(react, messageContent);
        };
        ReactsAvailable.appendChild(reactSpan);
    });

    reactButton.appendChild(ReactsAvailable);
    replyReact.appendChild(replyButton);
    replyReact.appendChild(reactButton);

    
    newMessage.appendChild(replyReact);

    return newMessage;
}

function addReact(react, messageContent) {
    // Find the existing reactions box or create a new one
    var reactionsBox = messageContent.querySelector(".reactions-box");
    if (!reactionsBox) {
        reactionsBox = document.createElement("div");
        reactionsBox.classList.add("reactions-box");
        messageContent.appendChild(reactionsBox);
    }

    // Check if the reaction already exists
    var existingReact = reactionsBox.querySelector(`.react .emoji[data-emoji="${react}"]`);
    if (existingReact) {
        // If the reaction already exists, increase the count
        var countDiv = existingReact.parentElement.querySelector('.count');
        var currentCount = parseInt(countDiv.innerText);
        countDiv.innerText = currentCount + 1;
    } else {
        // If the reaction does not exist, create a new one
        var reactDiv = document.createElement("div");
        reactDiv.classList.add("react");
        var emojiDiv = document.createElement("div");
        emojiDiv.classList.add("emoji");
        emojiDiv.setAttribute("data-emoji", react);
        emojiDiv.innerText = react;
        var countDiv = document.createElement("div");
        countDiv.classList.add("count");
        countDiv.innerText = "1"; // Initial count is 1

        reactDiv.appendChild(emojiDiv);
        reactDiv.appendChild(countDiv);

        reactionsBox.appendChild(reactDiv);
    }
}




// Function to show the "Replying to" section
function showReplyingTo(message) {
    var replyingToDiv = document.querySelector(".chat-footer-box .replying-to");
    replyingToDiv.style.display = "flex";
    replyingToDiv.innerHTML = `
        <span>Replying to:</span>
        <div class="message-replied">
            <div class="user-pic">
                <img src="./assets/userpic.svg" alt="user-pic">
            </div>
            <div class="user-tag">@Figgy</div>
            <span>${message}</span>
        </div>
        <button class="close" onclick="closeReplyMessage()">
            <i data-lucide="x-circle"></i>
        </button>
    `;
}

// Function to close the "Replying to" section
function closeReplyMessage() {
    var replyingToDiv = document.querySelector(".chat-footer-box .replying-to");
    replyingToDiv.style.display = "none";
}

// Function to toggle the emoji picker
function toggleEmojiPicker() {
    var emojiPicker = document.getElementById("emojiPicker");
    emojiPicker.classList.toggle("show");
    fetchEmojis(); // Fetch emojis when the picker is toggled
}

// Function to fetch emojis from the API
function fetchEmojis() {
    var emojiPicker = document.getElementById("emojiPicker");
    emojiPicker.innerHTML = ""; // Clear previous results

    fetch("https://emoji-api.com/emojis?access_key=36648086e6b1d3c021726d4a3399bafaa5c2eaa3")
        .then(response => response.json())
        .then(data => {
            // Loop through the emoji data and create buttons for each emoji
            data.forEach(emoji => {
                var emojiButton = document.createElement("button");
                emojiButton.innerHTML = emoji.character;
                emojiButton.classList.add("emoji");
                emojiButton.addEventListener("click", function() {
                    insertEmoji(emoji.character);
                });
                emojiPicker.appendChild(emojiButton);
            });
        })
        .catch(error => console.error('Error fetching emojis:', error));
}

// Function to insert the selected emoji into the input field
function insertEmoji(emoji) {
    var userInput = document.getElementById("userInput");
    var cursorPosition = userInput.selectionStart;
    var textBefore = userInput.value.substring(0, cursorPosition);
    var textAfter = userInput.value.substring(cursorPosition);
    userInput.value = textBefore + emoji + textAfter;

    // Move the cursor position after the inserted emoji
    userInput.selectionStart = cursorPosition + emoji.length;
    userInput.selectionEnd = cursorPosition + emoji.length;

    // Hide the emoji picker after inserting
    var emojiPicker = document.getElementById("emojiPicker");
    emojiPicker.classList.remove("show");
}


function toggleRoomsMobile() {
    var rooms = document.querySelector('.chat-rooms');
    var close = document.querySelector('.close-rooms');
    rooms.classList.toggle('show');
    //give body style overlay Y none 

    // IF CLOSE BUTTON IS CLICKED CLOSE ROOMS
    close.addEventListener('click', function() {
        rooms.classList.remove('show');

    });
}
function toggleMembersMobile() {
    var rooms = document.querySelector('.chat-members');
    var close = document.querySelector('.close-toggle');
    rooms.classList.toggle('show');
    // IF CLOSE BUTTON IS CLICKED CLOSE ROOMS
    close.addEventListener('click', function() {
        rooms.classList.remove('show');
    });
    
}