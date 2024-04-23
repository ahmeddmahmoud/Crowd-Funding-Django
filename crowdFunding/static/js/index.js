// <!-- js for star styling   -->
document.addEventListener('DOMContentLoaded', function () {
    const stars = document.querySelectorAll('.rating input[type="radio"]');
    const rateInput = document.getElementById('id_rate'); 
//   rateInput.style.display="none";
    stars.forEach(star => {
      star.addEventListener('change', function () {
        rateInput.value = this.value;
        console.log("Selected rating:", this.value);
        console.log("Rate input value:", rateInput.value);
      });
    });

    var deleteButtonClicked = false;
    document.getElementById('delete-project-btn').addEventListener('click', function(event) {
      deleteButtonClicked = true;
      // Prevent the default action by default
      event.preventDefault();

      // Fetch the data from the provided URL
      fetch(this.href)
          .then(response => response.json())
          .then(data => {
              // Check if there's an error message in the response
              if (data.error) {
                  // Update the error message placeholder with the received error message
                  var errorMessageElement = document.getElementById('error-message');
                  errorMessageElement.textContent = data.error;
                  errorMessageElement.style.display = 'block'; // Show the error message
              } else {
                  // If no error message, allow the default action (redirecting to list.html)
                //    window.location.href = ''http://127.0.0.1:8000/project/''; 
                  window.location.href = 'http://127.0.0.1:8000/project/';

              }
          })
          .catch(error => console.error('Error:', error));
  });


  document.getElementById('add-comment-btn').addEventListener('click', function() {
      if (!deleteButtonClicked){
          var commentForm = document.querySelector('.add-comment-form');
      if (commentForm.style.display === 'none' || commentForm.style.display === '') {
          commentForm.style.display = 'block';
      } else {
          commentForm.style.display = 'none';
      }
      }
  });



  });