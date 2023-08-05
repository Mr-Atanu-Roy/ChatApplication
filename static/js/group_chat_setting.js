$(document).ready(function () {
  try {
    //getting the group id
    const GROUP_ID = JSON.parse(
      document.getElementById("group_id").textContent
    );

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


    //exit chat group
    $("#exit-group").on("click", function () {
      $("#popup-message").html("Are you sure that you want to exit this group?");

      let content = `
      <button id="exit-group-confirm" class="rounded-md bg-red-600 hover:bg-red-700 transition-colors py-2 px-4 xs:py-3 xs:px-6 text-sm xs:text-base text-white duration-300 uppercase font-bold">exit group</button>
      `;
      $("#btn-2-box").html(content);

      $("#popup-alert").css("display", "flex");
    });
    
    //exit group on confirmation
    $(document).on("click", "#exit-group-confirm", function () {
      $.ajax({
        type: "get",
        url: "/api/group/exit-group/",
        data: {
          "group_id": GROUP_ID,
        },
        success: function (response) {
          console.log(response)
          if(response.status == 201 && response.message == "user removed"){
            window.location.href = "/";
          }
        }
      });       
    });

    //delete chat group
    $("#delete-group").on("click", function () {
      $("#popup-message").html("Are you sure that you want to delete this group? All other members of this group will be removed from this group.");

      let content = `
      <button id="delete-group-confirm" class="rounded-md bg-red-600 hover:bg-red-700 transition-colors py-2 px-4 xs:py-3 xs:px-6 text-sm xs:text-base text-white duration-300 uppercase font-bold">delete group</button>
      `;
      $("#btn-2-box").html(content);

      $("#popup-alert").css("display", "flex");
    });

    //delete chat group on confirmation
    $(document).on("click", "#delete-group-confirm", function () {
      $.ajax({
        type: "get",
        url: "/api/group/delete-group/",
        data: {
          "group_id": GROUP_ID,
        },
        success: function (response) {
          console.log(response)
          if(response.status == 201 && response.message == "group deleted"){
            window.location.href = "/";
          }
        }
      });   
    });
  } catch (error) {
    console.log("error: ".error);
  }
});
