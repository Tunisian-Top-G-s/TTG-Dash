function updateProgressBar(percentage) {
    var progressBar = document.getElementById("progressBar");
    progressBar.style.width = percentage + '%';
    //progressBar.innerHTML = percentage + '%'; // Optional: Display the percentage
  }
  
  // Example usage: Update the progress bar to 70%
  updateProgressBar(80);
  
  document.addEventListener('DOMContentLoaded', function () {
    var dropdownToggles = document.querySelectorAll('.dropdownToggle');

    dropdownToggles.forEach(function(toggle) {
        toggle.addEventListener('click', function(event) {
            event.preventDefault();
            var modules = this.parentNode.nextElementSibling; // Assuming .modules is always the next sibling
            modules.classList.toggle('is-active');
        });
    });
});




