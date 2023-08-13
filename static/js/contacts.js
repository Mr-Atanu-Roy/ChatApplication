$(document).ready(function () {
  try {
    //search contact
    $("#search-contact-form").submit(function (e) {
      e.preventDefault();

      let phone = $("#phone").val();
      $.ajax({
        type: "post",
        url: "/api/search_contact/",
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
                <div class="py-2.5 sm:px-2 flex items-center justify-between hover:bg-light-dark transition-colors duration-300 cursor-pointer rounded">
                    <div class="w-full flex items-center justify-start">
                        <div class="mr-2.5 sm:mr-3.5 text-white text-3xl col-span-1 overflow-hidden w-16 h-16 rounded-full bg-cover bg-no-repeat bg-center flex items-center justify-center `;
                          if (data["profile_pic"] == null) {
                            content += `border-green-0 border-[3.1px] border-solid">`;
                          }else{
                            content += `" style="background-image: url('${data["profile_pic"]}');">`;
                          }
                          if (data["profile_pic"] == null) {
                            content += `${data["name"][0]}`;
                          }
                          content += `
                        </div>
                        <div>
                            <p class="font-bold text-lg text-white">${data["name"]}</p>
                            <p class="font-bold text-xs text-gray-400">
                                ${data["phone"]}
                            </p>
                        </div>
                    </div>
                </div>`;
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

    //click on searched contact
    $(document).on("click", "#user-search-contact-box", function () {
      let user_phone = $("#user-search-contact-phone").html();
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
            content = `
            <div class="py-2 px-1.5">
              <p class="font-bold text-sm text-white capitalize">${message}</p>
          </div>
              `;

            // reload page to see the changes
            setTimeout(function () {
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

  } catch (error) {
    console.log("error: ".error);
  }
});
