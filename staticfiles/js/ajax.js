$(document).ready(function () {
    $('#contactForm').on('submit', function (e) {
      e.preventDefault();
  
      let name = $('#name').val();
      let email = $('#email').val();
      let phone = $('#phone').val();
      let message = $('#message').val();
      let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
      let responseMessage = $('#responseMessage');
  
      $.ajax({
        url: "{% url 'contact_view' %}", // URL to your Django view
      
        type: 'POST',
        data: {
          csrfmiddlewaretoken: csrfToken,
          name: name,
          email: email,
          phone: phone,
          message: message
        },
        success: function (data) {
          if (data.success) {
            responseMessage.html(`<div class="alert alert-success">${data.message}</div>`);
            $('#contactForm')[0].reset(); // Reset the form on success
          } else {
            responseMessage.html(`<div class="alert alert-danger">${data.message}</div>`);
          }
        },
        error: function () {
          responseMessage.html(`<div class="alert alert-danger">An error occurred. Please try again later.</div>`);
        }
      });
    });
  });
  