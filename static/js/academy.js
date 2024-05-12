document.addEventListener("DOMContentLoaded", function() {
    var dropdownToggles = document.querySelectorAll('.dropdownToggle');

    dropdownToggles.forEach(function(toggle) {
        toggle.addEventListener('click', function(event) {
            event.preventDefault();
            var modules = this.parentNode.nextElementSibling;
            modules.classList.toggle('is-active');
        });
    });
    
    levelProgressText = document.querySelector('.percentage-progess');
    ajaxRequest('POST', '/level_progress/', {level_id: level_id}, function(response) {
        if (response.success) {
            console.log(response);
            // Set the width of the progress bar for the current course
            levelProgressText.innerText = `${response.level_progression}% complete`;
            updateProgressBar(response.level_progression);
        } else {
            console.log(response);
        }
    }, null, true, "level progression", null)
    
    
    /* CHANGE THIS */
    let currentIndex = 0;
    const nextLessonBtn = document.getElementById('nextLessonBtn');
    const prevBtns = document.querySelectorAll('.prev-btn');
    const lessonContainers = document.querySelectorAll('.container-lesson');

    nextLessonBtn.addEventListener('click', function (event) {
        event.preventDefault();
        nextLesson(lessonContainers, currentIndex);
    });
    prevBtns.forEach(prevBtn => {
        prevBtn.addEventListener('click', function (event) {
            event.preventDefault();
            prevLesson(lessonContainers, currentIndex);
        });
    });


    // Show the first lesson initially
    showLesson(lessonContainers, currentIndex);

    const moduleDropdowns = document.querySelectorAll('.modules-dropdowns');
    let moduleIds = [];

    moduleDropdowns.forEach(function (dropdown) {
        const moduleId = dropdown.dataset.id; // Extract the data-id attribute
        moduleIds.push(moduleId); // Append the module ID to the list

        dropdown.addEventListener('click', function (e) {
            e.preventDefault(); // Prevent the default action of the event
            const videoId = moduleId; // Assuming moduleId contains the ID of the clicked video
            changeVideo(videoId);
        });
    });

    // Extract the videoId from the URL if it exists
    const urlParams = new URLSearchParams(window.location.search);
    const videoIdParam = urlParams.get('id');

    // Check if the videoIdParam exists and is in moduleIds
    let videoId = moduleIds.length > 0 ? moduleIds[0] : null;
    if (videoIdParam && moduleIds.includes(videoIdParam)) {
        videoId = videoIdParam;
    }
    changeVideo(videoId);

});
function toggleLike(element) {
    element.classList.toggle('liked');
}

function updateProgressBar(percentage) {
    var progressBar = document.getElementById("progressBar");
    progressBar.style.width = percentage + '%';
}

function showLesson(lessonContainers, index) {
    lessonContainers.forEach((container, i) => {
        container.style.display = i === index ? 'flex' : 'none';
    });
}
function nextLesson(lessonContainers, currentIndex) {
    if (currentIndex < lessonContainers.length - 1) {
        currentIndex++;
        showLesson(lessonContainers, currentIndex);
    }
}
function prevLesson(lessonContainers, currentIndex) {
    if (currentIndex > 0) {
        currentIndex--;
        showLesson(lessonContainers, currentIndex);
    }
}




function generateAnswers(answers, rightAnswer) {
    const container = document.querySelector('#container-answers');
    const nextLessonBtn = document.getElementById('nextLessonBtn');

    console.log('Right Answer:', rightAnswer); // Debugging

    container.innerHTML = ''; // Clear the container first if needed

    // Remove any existing feedback message
    const existingFeedback = document.querySelector('.feedback-message');
    if (existingFeedback) {
        existingFeedback.remove();
    }

    answers.forEach(answer => {
        const answerDiv = document.createElement('div');
        const answerSpan = document.createElement('span');

        answerDiv.className = `answer answer-${answer.id}`;
        answerSpan.classList.add('answers-texts');
        answerSpan.textContent = answer.text;

        answerDiv.appendChild(answerSpan);
        container.appendChild(answerDiv);

        answerDiv.addEventListener('click', function () {
            // Disable further clicks
            container.querySelectorAll('.answer').forEach(ans => ans.style.pointerEvents = 'none');

            const isCorrect = answer.id === rightAnswer;
            console.log('Selected Answer:', answer.id, 'Is Correct:', isCorrect);

            answerDiv.style.backgroundColor = isCorrect ? '#0F0' : '#F00';

            answers.forEach(ans => {
                const div = document.querySelector(`.answer-${ans.id}`);
                if (ans.id === rightAnswer) {
                    div.classList.add('answer-right');
                    if (!div.querySelector('img')) {
                        const iconImage = document.createElement('img');
                        iconImage.src = '/static/assets/Check Mark.png';
                        iconImage.alt = 'Correct';
                        div.appendChild(iconImage);
                    }
                } else if (ans.id === answer.id) {
                    div.classList.add('answer-wrong');
                    const iconImage = document.createElement('img');
                    iconImage.src = '/static/assets/Close.png';
                    iconImage.alt = 'Incorrect';
                    div.appendChild(iconImage);
                }
            });

            if (isCorrect) {
                console.log('Next button will be shown');
                nextLessonBtn.style.display = 'block';
            } else {
                console.log('Retry required');
                displayFeedbackMessage("Sorry, that's incorrect. Please try again.");
                showRetryButton();
            }
        });
    });
}

function showRetryButton() {
    const retryButton = document.createElement('button');
    retryButton.textContent = 'Retry Quiz';
    retryButton.classList.add('retry-button');
    retryButton.onclick = function () {
        document.location.reload(true); // Reload the page for simplicity
    };

    const container = document.querySelector('#container-answers');
    const existingButton = document.querySelector('.retry-button');
    if (!existingButton) {
        container.after(retryButton);
    }
}

function displayFeedbackMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('feedback-message');
    messageDiv.textContent = message;

    const container = document.querySelector('#container-answers');
    container.after(messageDiv);
}


function loadQuiz(videoId) {
    const nextLessonBtn = document.getElementById('nextLessonBtn');
    
    ajaxRequest('POST', '/get-video/', {"videoId": videoId}, function (response) {
        console.log('Server response (loadQuiz):', response); // Log the response

        if (response.success && response.video && response.video.quiz_options) {
            const answers = Object.entries(response.video.quiz_options).map(([key, value], index) => ({
                id: index + 1,
                text: value
            }));
            const quiz = response.video.quiz || {};
            generateAnswers(answers, quiz.answer || null);
        } else {
            console.error('Unexpected response format:', response);
            displayFeedbackMessage("Error loading quiz data. Please try again.");
        }
    }, function() {
        displayFeedbackMessage("Error loading quiz data. Please try again.")
    }, true, "Load quiz", null)

}

function changeVideo(videoId) {
    ajaxRequest('POST', '/get-video/', {"videoId": videoId}, function (response) {
        console.log('Server response (changeVideo):', response); // Log the response

        if (response.success && response.video) {
            // Update UI elements with new video data
            document.querySelector('.videoSRC').src = response.video.video_file;
            document.querySelector('video').load();
            document.querySelectorAll('.lesson-text').forEach(el => el.innerText = response.video.title);
            document.querySelectorAll('.title-lesson-description').forEach(el => el.innerText = response.video.title);
            document.querySelectorAll('.description-step-video').forEach(el => el.innerText = JSON.stringify(response.video.notes));
            document.querySelectorAll('.question-text').forEach(el => el.innerText = `Question: ${response.video.quiz_question}`);

            // Load quiz options
            loadQuiz(videoId);
        } else {
            console.error('Unexpected response format:', response);
            displayFeedbackMessage("Error loading video data. Please try again.");
        }
    }, function() {
        displayFeedbackMessage("Error loading video data. Please try again.");
    }, true, "get current video details", null)
}