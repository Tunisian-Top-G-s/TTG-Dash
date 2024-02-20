const answers = [
    { id: 1, text: "a) Elon Musk who created Bitcoin" },
    { id: 2, text: "b) aymen benrom who created Bitcoin" },
    { id: 3, text: "c) Satoshi Nakamoto who created Bitcoin" }, // The correct answer
    { id: 4, text: "d) Walid haj moussa who created Bitcoin" }
];

function generateAnswers() {
    const container = document.querySelector('#container-answers');
    container.innerHTML = ''; // Clear the container first if needed

    // Remove any existing feedback message
    const existingFeedback = document.querySelector('.feedback-message');
    if (existingFeedback) {
        existingFeedback.remove();
    }

    answers.forEach(answer => {
        const answerDiv = document.createElement('div');
        const answerSpan = document.createElement('span');

        answerDiv.classList.add(`answer-${answer.id}`);
        answerSpan.classList.add('answers-texts');
        answerSpan.textContent = answer.text;

        answerDiv.appendChild(answerSpan);
        container.appendChild(answerDiv);

        answerDiv.addEventListener('click', function() {
            // Disable further clicks
            container.querySelectorAll('div').forEach(div => {
                div.style.pointerEvents = 'none';
            });

            let selectedCorrectly = answer.id === 3; // Check if the selected answer is correct
            answers.forEach(ans => {
                const div = document.querySelector(`.answer-${ans.id}`);
                if (ans.id === 3) { // Correct answer
                    div.classList.add('answer-right');
                    if (!div.querySelector('img')) {
                        const iconImage = document.createElement('img');
                        iconImage.src = './assets/Check Mark.png';
                        iconImage.alt = 'Correct';
                        div.appendChild(iconImage);
                    }
                } else if (ans.id === answer.id) { // Selected answer if it's wrong
                    div.classList.add('answer-wrong');
                    const iconImage = document.createElement('img');
                    iconImage.src = './assets/Close.png';
                    iconImage.alt = 'Incorrect';
                    div.appendChild(iconImage);
                }
            });

            if (!selectedCorrectly) {
                displayFeedbackMessage("Sorry, that's incorrect. Please try again.");
            }

            // Show a retry button
            showRetryButton();
        });
    });
}

function showRetryButton() {
    const retryButton = document.createElement('button');
    retryButton.textContent = 'Retry Quiz';
    retryButton.classList.add('retry-button'); // Use the class for styling
    retryButton.onclick = function() {
        document.location.reload(true); // Reload the page for simplicity
    };

    const container = document.querySelector('#container-answers');
    // Remove existing retry button if it exists to prevent duplicates
    const existingButton = document.querySelector('.retry-button');
    if (!existingButton) {
        container.after(retryButton); // Place the retry button outside and below the container
    }
}

function displayFeedbackMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('feedback-message');
    messageDiv.textContent = message;

    const container = document.querySelector('#container-answers');
    container.after(messageDiv); // Place the message below the container
}

document.addEventListener('DOMContentLoaded', generateAnswers);
