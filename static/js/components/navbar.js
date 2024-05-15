document.addEventListener('DOMContentLoaded', function () {
    var chevronDownIcon = document.getElementById('chevron-down-icon');
    var profileDropDown = document.getElementById('profile-dropdown');
    var containerProfile = document.querySelector('.container-profile');
    var dropdownMenu = document.getElementById("dropDownMenu");
    var navLinks = document.querySelectorAll(".menu-item");
    var hamburgerLines = document.querySelector(".hamburger-lines");
    var navToggle = document.getElementById("navToggle");
    var navContainer = document.getElementById("navContainer");
    var notification = document.querySelector('.notification');
    var notificationMenu = document.querySelector('.notification > .menu');
    var messages = document.querySelector('.messages');
    var messagesMenu = document.querySelector('.messages > .menu');
    var body = document.querySelector('body');

    profileDropDown.addEventListener('click', function () {
        chevronDownIcon.classList.toggle('rotate');
        containerProfile.style.display = containerProfile.style.display === 'flex' ? 'none' : 'flex';
    });

    navToggle.addEventListener("change", function () {
        if (this.checked) {
            hamburgerLines.classList.add("checked");
            dropdownMenu.style.transform = "translate(0)";
            dropdownMenu.style.zIndex = "120";
            dropdownMenu.style.display = "block";
            navContainer.style.position = "fixed";
            navContainer.style.zIndex = "120";
        } else {
            hamburgerLines.classList.remove("checked");
            dropdownMenu.style.transform = "translate(-150%)";
            dropdownMenu.style.display = "none";
            navContainer.style.position = "relative";
            navContainer.style.zIndex = "100";
        }
    });
    
    
    navLinks.forEach(function (link) {
        link.addEventListener("click", function () {
            document.querySelectorAll('.nav-slipe').forEach(n => n.classList.remove('active-nav')); // Remove active class from all nav items
            this.querySelector('.nav-slipe').classList.add('active-nav'); // Add active class to clicked nav item
        });
    });

    notification && notificationMenu && setupMenuInteraction(notification, messages);
    messages && messagesMenu && setupMenuInteraction(messages, notification);

    body.addEventListener('click', closeAllMenus);

    highlightCurrentPage();

    function setupMenuInteraction(menu, otherMenu) {
        menu.addEventListener('click', function (e) {
            e.stopPropagation();
            otherMenu.classList.remove('--active');
            menu.classList.toggle('--active');
        });

        menu.querySelector('.menu').addEventListener('click', function (e) {
            e.stopPropagation();
        });
    }

    function closeAllMenus() {
        [notification, messages].forEach(menu => {
            if (menu) menu.classList.remove('--active');
        });
    }
});

function highlightCurrentPage() {
    var currentPage = getCurrentPage();
    var currentLink = document.querySelector(`a[id="${currentPage}"] > .nav-slipe`);
    if (!currentLink) {
        currentLink = document.querySelector(`a[id="home"] .nav-slipe`);
        currentLink.classList.add('active-nav');
    }
    if(currentPage === 'video-course') currentLink = document.querySelector(`a[id="courses"] .nav-slipe`);
    if(currentPage === 'levels') currentLink = document.querySelector(`a[id="courses"] .nav-slipe`);
    if (currentLink) {
        currentLink.classList.add('active-nav');
    }

}

function getCurrentPage() {
    var pathArray = window.location.pathname.split('/');
    var currentPage = pathArray.pop() || pathArray.pop(); // Handles trailing slash
    
    // Check if the URL contains '/levels' or '/video-course'
    if (window.location.pathname.includes('/levels')) return 'courses';
    if (window.location.pathname.includes('/video-course')) return 'courses';
    if (window.location.pathname.includes('/private-session')) return 'private-session';
    if (window.location.pathname.includes('/shop')) return 'shop';
    if (window.location.pathname.includes('/product')) return 'shop';
    if (window.location.pathname.includes('/cart')) return 'shop';
    if (window.location.pathname.includes('/checkout')) return 'shop';
    if (window.location.pathname.includes('/courses')) return 'courses';
    if (window.location.pathname.includes('/dashboard')) return 'dashboard';





    
    // Check if the URL ends with 'server-chat/badges/' or 'server-chat/'
    if (pathArray[1] === 'server-chat') return 'serverChat';


    return pathArray;
}
function CountNotification(){
    var count = document.querySelector('.counter-noti-messd');
    var notificationList = document.querySelector('.notifications-list');
    var notificationCount = notificationList.children.length;
    if(notificationCount == 0){
        count.innerHTML = 0;
    }
    else if(notificationCount > 9){
        count.innerHTML = '9+';
    }
    else{
        count.innerHTML = notificationCount;
    }
}
CountNotification();

function CountMessages(){
    var count = document.querySelector('.messages-counter');
    var messagesList = document.querySelector('.messages-list');
    var messagesCount = messagesList.children.length;
    if(messagesCount == 0){
        count.innerHTML = 0;
    }
    else if(messagesCount > 9){
        count.innerHTML = '9+';
    }
    else{
        count.innerHTML = messagesCount;
    }
}
CountMessages();