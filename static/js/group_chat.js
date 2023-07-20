$(document).ready(function () {
  try {
    
    //scroll to bottom
    location.href = "#";
    location.href = "#end";

    //getting current user phone
    const PHONE = JSON.parse(document.getElementById("current_user_phone").textContent);

    //getting the group id
    const GROUP_NAME = JSON.parse(document.getElementById("group_name").textContent);


    //creating a websocket con
    // var ws = new WebSocket("ws://127.0.0.1:8000/api/chat/group/")
    const ws = new WebSocket(
      "ws://" + window.location.host + "/api/chat/group/" + GROUP_NAME + "/"
    );

    //msg from server
    ws.onmessage = function (event) {
      const data = JSON.parse(event.data);

      let msg = data.message;
      let name = data.user_name;
      let phone = data.user_phone;
      let user_pic = data.user_pic;
      let time = data.time;

      let content = `
      <div class="my-2 w-full flex items-center `;
        if(PHONE == phone){
          content += `justify-end`;
        }
      content += `">
        <div class="flex flex-col">`;
            if(PHONE == phone){
              content += `
              <div class="w-7 h-7 rounded-full bg-cover bg-no-repeat bg-center"
                style="background-image: url('${user_pic}');"></div>
              `;
            }
            content +=`<div class="max-w-md py-2 my-1 px-3 text-white bg-green-0 w-fit rounded-lg `;
            if(PHONE == phone){
              content += `rounded-tr-none`;
            }else{
              content += `rounded-tl-none`;
            }
              content += `">
                <div class="flex items-center justify-between text-slate-900 font-bold mb-1.5 text-xs">`;
                if(PHONE == phone){
                  content += `<p class="mr-14">you</p>`;
                }else{
                  content += `
                  <p class="mr-14">${name}</p>
                  <p>${phone}</p>
                  `;
                }
        content += `</div>
                <p>${msg}</p>
            </div>
            <p class="text-gray-300 text-xs text-right">${time}</p>
        </div>
      </div>
      `;
      //append to chat messages at end
      $("#group-chat-msg").append(content);

      //scroll to bottom
      location.href = "#end";
    };

    //handling error
    ws.onerror = function (event) {
      console.log("error occurred ...", event);
    };


    //handling msg submit
    $("#send-msg-btn").on("click", function (e) {
      e.preventDefault();

      let msg = $("#input-message").val();
      ws.send(JSON.stringify({ "msg": msg }));
      $("#input-message").val("");

    });


  } catch (error) {
    console.log(error);
  }
});
