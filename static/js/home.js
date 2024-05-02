
points_counter = document.querySelector(".points-counter")
courseProgressionCounter = document.querySelector(".progress-percent");
courseProgressionSlider = document.querySelector(".progress-bar-inner");
ajaxRequest('POST', "/course-progress/", null, function(response) {points_counter.innerText = response.course_progression;courseProgressionCounter.innerText = response.course_progression + "%";courseProgressionSlider.style.width = response.course_progression}, function(response) {const errorMessageDiv = document.getElementById("errorMessage");errorMessageDiv.textContent = "An error occurred while processing your request.";}, true, "Fetch course pgroggress")


var lossesPercentageBtcElement = document.querySelectorAll('.btc-percentage');
var lossesPercentageEthElement = document.querySelectorAll('.eth-percentage');
var lossesPercentageEthElement = document.querySelectorAll('.eth-percentage');

var lossesBtcElement = document.querySelectorAll('.btc-price');
var lossesEthElement = document.querySelectorAll('.eth-price');

ajaxRequest('GET', '/getDashboard/', null, function(response){
        var btc = response["dashboard"].btc;
        var eth = response["dashboard"].eth;

        lossesPercentageBtcElement.forEach(function(element) {
          element.textContent = '%' + btc[1].toFixed(2);
        });
        lossesPercentageEthElement.forEach(function(element) {
          element.textContent = '%' + eth[1].toFixed(2);
        });

        lossesBtcElement.forEach(function(element) {
          element.textContent = '$' + btc[0];
        });
        lossesEthElement.forEach(function(element) {
          element.textContent = '$' + eth[0];
        });
    }
    , null, true, "Update Crypto stats")


// Event listener for the rating icons
document.querySelectorAll('.rating li').forEach(icon => {
    icon.addEventListener('click', event => {
        // Reset all icons to original state
        document.querySelectorAll('.rating label').forEach(svgIcon => {
            svgIcon.style.background = ""; // Clear any set background
            svgIcon.style.fill = ""; // Assuming SVG, we use fill for color
        });

        // Change the clicked icon's appearance
        const svgElement = icon.querySelector('label');
        if (svgElement) { // Ensure the SVG element exists
            svgElement.style.background = "rgb(200 124 255 / 40%)"; // White background
        }
    });
});

// The submit button listener remains the same

// Get all the radio buttons with the class "feedback-option"
const radioButtons = document.querySelectorAll('.feedback-option');
let selectedValue = "";
// Add event listener to each radio button
radioButtons.forEach(radioButton => {
    radioButton.addEventListener('change', () => {
        // Check if radio button is checked
        if (radioButton.checked) {
            // Get the value of the checked radio button
            selectedValue = radioButton.value;
            console.log('Selected value:', selectedValue);
        }
    });
});

function showThankYouMessage() {

}

function showErrorMessage() {

}

console.log("kyrix/zend: 9ol ll user 'select an option w raj3o ye5tar option ml options'")
document.getElementById('submit-btn').addEventListener('click', function(event) {
    event.preventDefault(); // Prevents navigating to a new page if href="#".

    console.log(selectedValue);
    if (selectedValue) {
        ajaxRequest('POST', "/submit-feedback/", {feedback: selectedValue}, function (response) {
            if (response.success) {
                document.querySelector('.told-wrapper').innerHTML = 
                    `<div class="thank-you-message">
                        <span>Thank you for your reviews! ; ) </span>
                        <span>You've earned 20 Points </span>
                    </div>`;
                // Trigger animation after setting innerHTML
                document.querySelector('.thank-you-message').classList.add('slide-in');
            }
            else {
                document.querySelector('.told-wrapper').innerHTML = 
                    `<div class="thank-you-message">
                        <span>You already submitted a review! ; ) </span>
                        <span>You already earned your 20 Points </span>
                    </div>`;
                // Trigger animation after setting innerHTML
                document.querySelector('.thank-you-message').classList.add('slide-in');
            }
        }, null, true, "Feedback submit")
    }
    else {
        console.log("kyrix/zend: 9ol ll user 'select an option w raj3o ye5tar option ml options'")
    }
});



// Call the function to fetch course progress when the document is ready
$(document).ready(function() {
    changeCourseProgress();  // Ensure this function is defined and working properly

    var claimButton = document.querySelector('#claimPoints');

    var popupMessage = document.getElementById('popupMessage');
    var popupImage = document.getElementById('popupImage');
    var popupSpan = document.getElementById('popupSpan');

    claimButton.addEventListener('click', function(event) {
        event.preventDefault(); // Stop the form from submitting normally
        console.log('Claim button clicked.');
        ajaxRequest('POST', '/add_points/', null, function(response){
            if (response.success) {
                claimButton.textContent = 'Claimed';
                claimButton.disabled = true;
                popupMessage.classList.add('success');
                popupImage.src = "{% static 'assets/points-icon.svg' %}";
                popupSpan.textContent = "You claimed 1000 points, get back the next day.";
                popupMessage.style.display = 'block';
            } else {
                popupMessage.classList.remove('success');
                popupImage.src = "{% static 'assets/x-circle.svg' %}";
                popupSpan.textContent = "You already claimed your daily points! Try again tomorrow.";
                popupMessage.style.display = 'block';
            }
        }, function(error){
            popupSpan.textContent = "An error occurred while processing your request.";
            popupImage.src = "{% static 'assets/error-icon.svg' %}";
            popupMessage.style.display = 'block';
        }, true, "Claim daily points")
    });

    /* Close pop up after 5 seconds */

    document.getElementById('popUpCloseButton').addEventListener('click', function() {
        popupMessage.style.display = 'none';
    });
});

function changeCourseProgress() {
    // Iterate through each course element
    document.querySelectorAll('.course').forEach(function(course) {
        // Get the course ID from the data attribute
        var courseId = course.getAttribute('data-id');
        // Select the progress bar element within the current course
        var progressBar = course.querySelector('.progress-bar-inner');
        var progressPercent = course.querySelector('.progress-percent');
        // Make an AJAX request
        ajaxRequest('POST', "/course_progress/", {course_id: courseId}, function(response) {
            progressBar.style.width = `${response.course_progression}%`;
            progressPercent.innerText = `${response.course_progression}%`;
        }, null, true, "Fetch Course Progression")

    });
}


console.log(tracks)
console.log("kyrix/zend: when track loads change the name/image/banner and description if needed")

let currentTrackIndex = 0;
let isPlaying = false;
const audio = new Audio();

function loadTrack(index) {
    audio.src = tracks[index].src;
    audio.load();
    updateTrackInfo(tracks[index].name, tracks[index].image, tracks[index].description);

    updateUI(false); 
}

function togglePlay() {
    if (audio.src) {
        if (isPlaying) {
            audio.pause();
        } else {
            audio.play().catch(error => {
                console.error("Playback failed:", error);
            });
        }
        isPlaying = !isPlaying;
        updateUI(isPlaying);
    } else {
        loadTrack(currentTrackIndex);
        audio.play().catch(error => {
            console.error("Playback failed:", error);
        });
        isPlaying = true;
        updateUI(true);
    }
}

function updateUI(playing) {
    const playButton = document.querySelector('.play-pause-button'); // Ensure you have this element
    if (playButton) {
        playButton.textContent = playing ? 'Pause' : 'Play';
    }
}

// Update track information displayed on the UI
function updateTrackInfo(name, image, description) {
    const trackNameElement = document.querySelector('.track-name'); // Ensure you have this element
    const trackImageElement = document.querySelector('.player-image'); // Ensure you have this element
    const trackDescriptionElement = document.querySelector('.description-music'); // Ensure you have this element
    if (trackNameElement) trackNameElement.textContent = name;
    if (trackImageElement) trackImageElement.src = image;
    if (trackDescriptionElement) trackDescriptionElement.src = description;
}

const playPauseButton = document.querySelector('.play-pause-button'); // Ensure you have a button with this class
if (playPauseButton) {
    playPauseButton.addEventListener('click', togglePlay);
}

function nextTrack() {
    currentTrackIndex = (currentTrackIndex + 1) % tracks.length;
    loadTrack(currentTrackIndex);
}

function previousTrack() {
    currentTrackIndex = (currentTrackIndex - 1 + tracks.length) % tracks.length;
    loadTrack(currentTrackIndex);
}

function updateCurrentTime() {
    const current = audio.currentTime;
    const duration = audio.duration;
    const progress = (current / duration) * 100;
    document.querySelector('.last-time').textContent = formatTime(current);
    document.querySelector('.total-time').textContent = formatTime(duration);
    document.querySelector('.progress').style.width = progress + '%';
}

function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    const formattedTime = `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
    return formattedTime;
}

function updatePlayButton() {
    const playButton = document.querySelector('.play');
    playButton.innerHTML = isPlaying ? `
        <!-- SVG for pause -->
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="#dbdbdf" viewBox="0 0 16 16">
            <path d="M5.5 3.5A1.5 1.5 0 0 1 7 5v6a1.5 1.5 0 0 1-3 0V5a1.5 1.5 0 0 1 1.5-1.5m5 0A1.5 1.5 0 0 1 12 5v6a1.5 1.5 0 0 1-3 0V5a1.5 1.5 0 0 1 1.5-1.5"/>
        </svg>
        ` : `
        <!-- SVG for play -->
        <svg width="20" height="20" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M8.32137 25.586C7.9759 25.5853 7.63655 25.4948 7.33669 25.3232C6.66148 24.9406 6.24173 24.1978 6.24173 23.3915V7.07398C6.24173 6.26542 6.66148 5.52494 7.33669 5.14232C7.64369 4.96589 7.99244 4.87516 8.3465 4.87961C8.70056 4.88407 9.04692 4.98354 9.34938 5.16764L23.2952 13.5155C23.5859 13.6977 23.8255 13.9508 23.9916 14.251C24.1577 14.5511 24.2448 14.8886 24.2448 15.2316C24.2448 15.5747 24.1577 15.9121 23.9916 16.2123C23.8255 16.5125 23.5859 16.7655 23.2952 16.9478L9.34713 25.2979C9.0376 25.485 8.68307 25.5846 8.32137 25.586V25.586Z" fill="#E1E1E6"/>
        </svg>
    `;
}

function updateUI() {
    updateCurrentTime();
    updatePlayButton();
}

audio.addEventListener('timeupdate', updateCurrentTime);

document.addEventListener("DOMContentLoaded", function() {
    document.querySelector('.play').addEventListener('click', togglePlay);
    document.querySelector('.next').addEventListener('click', nextTrack);
    document.querySelector('.prev').addEventListener('click', previousTrack);
    loadTrack(0);
});