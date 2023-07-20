$(document).ready(function () {
  try {
    $("#search-contact-form").submit(function (e) {
      e.preventDefault();

      //search contact
      let phone = $("#phone").val();
      $.ajax({
        type: "post",
        url: "/api/search_contact_ajax/",
        data: {
          phone: phone,
        },
        success: function (response) {
          let status = response.status;
          let data = response.data;
          let error = response.error;
          let content = ``;

          if (error == null && status == 200) {
            content = `
                <div class="py-2.5 px-2 grid grid-cols-6 place-items-center hover:bg-light-dark transition-colors duration-300 cursor-pointer rounded" id="user-search-contact-box">
                    <div class="col-span-1 overflow-hidden w-16 h-16 rounded-full bg-cover bg-no-repeat bg-center"
                        style="background-image: url('${data["profile_pic"]}');"></div>
                    <div class="ml-2.5 col-span-5 w-full overflow-hidden text-white">
                        <p class="font-bold text-lg">${data["name"]}</p>
                        <p class="font-bold text-xs text-gray-400" id="user-search-contact-phone">${data["phone"]}</p>
                    </div>
                </div>
                `;
          } else if (status == 404 || status == 400) {
            content = `
                <div class="py-2 px-1.5">
                    <p class="font-bold text-sm text-white capitalize">${error}</p>
                </div>
                `;
          }

          $("#searched-user-view").html(content);
        },
      });

      //click on searched contact
      $(document).on("click", "#user-search-contact-box", function () {
        let user_phone = $("#user-search-contact-phone").html();
        $.ajax({
          type: "post",
          url: "/api/add_to_user_contact/",
          data: {
            phone: user_phone,
          },
          success: function (response) {
            let status = response.status;
            let message = response.message;
            let error = response.error;
            let content = ``;

            if (error == null && status == 201) {
              content = `
              <div class="py-2 px-1.5">
                <p class="font-bold text-sm text-white capitalize">${message}</p>
            </div>
                `;
            
            //reload page to see the changes
            setTimeout(function() {
                location.reload();
            }, 1600);

            } else if (status == 404 || status == 400) {
              content = `
                <div class="py-2 px-1.5">
                    <p class="font-bold text-sm text-white capitalize">${error}</p>
                </div>
                `;
            }

            $("#searched-user-view").html(content);
          },
        });
      });


    });
  } catch (error) {
    console.log("error: ".error);
  }
});
