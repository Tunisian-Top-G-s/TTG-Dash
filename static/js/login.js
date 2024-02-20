const signinSubmit = document.querySelector("#signinSubmit");

signinSubmit.addEventListener("click", (event) => {
    event.preventDefault();
    $.ajax({
    
        type: 'POST',
        url: "/loginf/",
        data: {
          username: $('#loginUsername').val(),
          password: $('#loginPassword').val()
        },  
    
        /* csrf */
        beforeSend: function(xhr, settings) {
          xhr.setRequestHeader('X-CSRFToken', getCookie("csrftoken"));
        },  
    
        success: function(response) {
            if (response.success) {
                console.log(response);
                window.location.href = "/"

            }
            else{
                console.log(response);

            }
        },
    
        error: function(error) {

            console.log(error);
        }
    });
})

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