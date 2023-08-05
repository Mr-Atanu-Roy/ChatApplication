$(document).ready(function () {
    try {
  
      //click on a contact
      $(document).on("click", "#add-contact-btn", function () {
        let user_phone = $(this).data("phone");
        $.ajax({
          type: "post",
          url: "/api/add_to_contact/",
          data: {
            phone: user_phone,
          },
          success: function (response) {
            let status = response.status;
            let message = response.message;
            let error = response.error;
  
            if (error == null && status == 201) {
              $("#popup-message").html(message);
              $("#popup-btn-2").css("display", "none");
              $("#popup-alert").css("display", "flex");
            } else if (status == 404 || status == 400) {
              $("#popup-message").html(error);
              $("#btn-2-box").css("display", "none");
              $("#popup-alert").css("display", "flex");
            }
  
          },
        });
      });
  


    } catch (error) {
      console.log("error: ".error);
    }
  });
  