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


      //click on remove contact
      $(document).on("click", "#remove-contact-btn", function () {
        
        $("#popup-message").html("Are you sure that you want to remove this contact from your friend list?");
        $("#popup-alert").css("display", "flex");
        
      });

      //remove friend on confirmation
      $(document).on("click", "#popup-btn-2", function () {
        let user_phone = $("#other-user-phone").html().trim();
        $.ajax({
          type: "get",
          url: "/api/remove_contact/",
          data: {
            "phone": user_phone,
          },
          success: function (response) {
            console.log(response)
            if(response.status == 204 && response.message==true){
              $("#btn-2-box").css("display", "none");
              $("#popup-message").html(`${user_phone} removed from your contact. Reload page to se changes`);
            }else{
              $("#btn-2-box").css("display", "none");
              $("#popup-message").html("Failed to perform this action. Try again later");
            }
          }
        });       
    });


    } catch (error) {
      console.log("error: ".error);
    }
  });
  