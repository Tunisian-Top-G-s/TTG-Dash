    // --------------Change Status----------------
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
    // --------------Change Status 2-----------------------
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
        // --------------------------------------------------
    // --------------Change Status 3----------------------
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