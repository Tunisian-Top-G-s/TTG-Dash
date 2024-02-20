document.addEventListener('DOMContentLoaded', function () {
    var chevronDownIcon = document.getElementById('chevron-down-icon');
    var ProfileDropDown = document.getElementById('profile-dropdown');
    var containerProfile = document.querySelector('.container-profile');

    ProfileDropDown.addEventListener('click', function () {
        chevronDownIcon.classList.toggle('rotate');
        containerProfile.style.display = containerProfile.style.display === 'flex' ? 'none' : 'flex';
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const dropdownMenu = document.getElementById("dropDownMenu");
    const navLinks = document.querySelectorAll(".menu-item");
    const hamburgerLines = document.querySelector(".hamburger-lines");
    const navToggle = document.getElementById("navToggle");
  
    navToggle.addEventListener("change", function () {
      if (this.checked) {
        hamburgerLines.classList.add("checked"); 
        dropdownMenu.style.transform = "translate(0)";
        dropdownMenu.style.zIndex = "1";
  
      } else {
        hamburgerLines.classList.remove("checked");
        dropdownMenu.style.transform = "translate(-150%)";
      }
    });
    // Close the menu when a menu item is clicked
    navLinks.forEach(function (link) {
      link.addEventListener("click", function () {
        dropdownMenu.style.transform = "translate(-150%)";
        hamburgerLines.classList.remove("checked");
      });
    });
  });
  