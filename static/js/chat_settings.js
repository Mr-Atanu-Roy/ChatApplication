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
          let content = ``;

          if (error == null && status == 201) {
            alert(message)

            //reload page to see the changes
            location.reload();
          } else if (status == 404 || status == 400) {
              alert(error)
          }

        },
      });
    });


    //exit chat group
    $("#exit-group").on("click", function () {
      $.ajax({
        type: "get",
        url: "/api/group/exit-group/",
        data: {
          "group_id": GROUP_ID,
        },
        success: function (response) {
          console.log(response)
          if(response.status == 201 && response.message == "user removed"){
            alert("you have exited the group")
            window.location.href = "/";
          }
        }
      });
    });


    //delete chat group
    $("#delete-group").on("click", function () {
      $.ajax({
        type: "get",
        url: "/api/group/delete-group/",
        data: {
          "group_id": GROUP_ID,
        },
        success: function (response) {
          console.log(response)
          if(response.status == 201 && response.message == "group deleted"){
            alert("you have deleted the group")
            window.location.href = "/";
          }
        }
      });
    });
  } catch (error) {
    console.log("error: ".error);
  }
});
