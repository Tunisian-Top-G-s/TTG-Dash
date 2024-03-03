document.addEventListener('DOMContentLoaded', function() {
    var tabs = document.querySelectorAll('ul.tabs li');
    var nextTabButtons = document.querySelectorAll('.next-tab-btn');
    var prevTabButtons = document.querySelectorAll('.back-tab-btn');
  
    // Function to switch tabs
    function switchTab(tabId) {
        tabs.forEach(function(item) {
            item.classList.remove('current');
        });
        var tabContents = document.querySelectorAll('.tab-content');
        tabContents.forEach(function(content) {
            content.classList.remove('current');
        });
  
        var selectedTab = document.querySelector('ul.tabs li[data-tab="' + tabId + '"]');
        selectedTab.classList.add('current');
        document.getElementById(tabId).classList.add('current');
    }
  
    // Event listener for tab clicks
    tabs.forEach(function(tab) {
        tab.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent the default action (switching tabs)
        });
    });
  
    // Event listener for next tab buttons
    nextTabButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var currentTab = document.querySelector('ul.tabs li.current');
            var currentIndex = Array.from(tabs).indexOf(currentTab);
            var nextIndex = (currentIndex + 1) % tabs.length;
            var nextTabId = tabs[nextIndex].getAttribute('data-tab');
            switchTab(nextTabId);
        });
    });
  
    // Event listener for previous tab buttons
    prevTabButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var currentTab = document.querySelector('ul.tabs li.current');
            var currentIndex = Array.from(tabs).indexOf(currentTab);
            var prevIndex = (currentIndex - 1 + tabs.length) % tabs.length;
            var prevTabId = tabs[prevIndex].getAttribute('data-tab');
            switchTab(prevTabId);
        });
    });
  });
  

form = document.querySelector("#sessionForm")
submitButton = document.querySelector(".next-tab-btn.submit")

submitButton.addEventListener("click", function (event) {
    event.preventDefault();
    formData = new FormData(form)


    for (const entry of formData.entries()) {
        console.log(entry);
    }

    $.ajax({
        type: 'POST',
        url: '/schedulePrivateSession/',
        data: formData,
        processData: false,
        contentType: false,
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', getCookie("csrftoken"));
        },
        success: function(response) {
            
            console.log(response);
            
        },
        error: function(error) {
            console.error('Error filtering products:', error);
        }
    });

});


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
