// func to set header in chat
function set_header(content) {
  $("#online-users").html(content);
}

// func to set online user
function online() {
  online_users = sessionStorage.getItem("online_users_num");

  let content = `<i class="fa fa-circle text-green-0 transition-colors mr-2"></i> Online: ${online_users}`;
  set_header(content);
}

//func for handling user join task for other user
function user_join(name, phone, user_phone) {
  //updating session
  online_users_num = parseInt(sessionStorage.getItem("online_users_num")) + 1;
  sessionStorage.setItem("online_users_num", online_users_num);

  let content = ``;

  if (phone == user_phone) {
    content = `You joined now...`;
  } else {
    content = `${name}: ${phone} joined now...`;
  }
  set_header(content);

  setTimeout(function () {
    online();
  }, 2500);
}

//func for handling user leave task for other user
function user_leave(name, phone) {
  //updating session
  online_users_num = parseInt(sessionStorage.getItem("online_users_num")) - 1;
  sessionStorage.setItem("online_users_num", online_users_num);

  let content = `${name}: ${phone} left now...`;
  set_header(content);

  setTimeout(function () {
    online();
  }, 2500);
}

//func for handling user join task for self
function user_list(online_users_num = 0, users) {
  //setting online users when user join
  sessionStorage.setItem("online_users_num", online_users_num - 1);

  let content = ``;

  for (let index = 0; index < users.length; index++) {
    content += users[index];
    if (index != users.length - 1) {
      content += `, `;
    }
  }
  set_header(content);

  setTimeout(function () {
    online();
  }, 2500);
}

$(document).ready(function () {
  try {
    //scroll to bottom
    location.href = "#";
    location.href = "#end";

    //getting current user phone
    const PHONE = JSON.parse(
      document.getElementById("current_user_phone").textContent
    );

    //getting the group id
    const GROUP_NAME = JSON.parse(
      document.getElementById("group_name").textContent
    );

    //creating a websocket con to: /api/chat/group/<group-name>/
    const ws = new WebSocket(
      "ws://" + window.location.host + "/api/chat/group/" + GROUP_NAME + "/"
    );

    //msg from server
    ws.onmessage = function (event) {
      const data = JSON.parse(event.data);

      if (data.type == "chat.message") {
        let msg = data.message;
        let name = data.user_name;
        let phone = data.user_phone;
        let user_pic = data.user_pic;
        let time = data.time;

        let content = `
      <div class="my-2 w-full flex items-center `;
        if (PHONE == phone) {
          content += `justify-end`;
        }
        content += `">
        <div class="flex flex-col">`;
        if (PHONE != phone) {
          content += `
              <div class="flex items-center justify-center w-7 h-7 text-white rounded-full bg-cover bg-no-repeat bg-center `;
          if (user_pic == "/media/") {
            content += `border-green-0 border-[2.2px] border-solid `;
          }
          content += `"`;
          if (user_pic != "/media/") {
            content += `style="background-image: url('${user_pic}');"`;
          }
          content += `>`;
          if (user_pic == "/media/") {
            content += `${name[0]}`;
          }

          content += `</div>`;
        }
        content += `<div class="max-w-md py-2 my-1 px-3 text-white bg-green-0 w-fit rounded-lg `;
        if (PHONE == phone) {
          content += `rounded-tr-none`;
        } else {
          content += `rounded-tl-none`;
        }
        content += `">
                <div class="flex items-center justify-between text-slate-900 font-bold mb-1.5 text-xs">`;
        if (PHONE == phone) {
          content += `<p class="mr-14">you</p>`;
        } else {
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
      } else if (data.type == "user.list") {
        //new user joins and gets list of online users(if any)
        user_list(data.online_num, data.online_users);
      } else if (data.type == "user.join") {
        //new user joins and others get notified about it
        user_join(data.username, data.phone, PHONE);
      } else if (data.type == "user.leave") {
        //new user leaves and others get notified about it
        user_leave(data.username, data.phone);
      } else {
        console.log("error: Invalid message type");
      }
    };

    //handling error
    ws.onerror = function (event) {
      console.log("error occurred: ", event.message);
      console.log("Closing connection.");
      ws.close();
    };

    //handling msg submit
    $("#send-msg-btn").on("click", function (e) {
      e.preventDefault();

      let msg = $("#input-message").val().trim();
      if (msg != "") {
        ws.send(JSON.stringify({ msg: msg }));
        $("#input-message").val("");
        $("#input-message").focus();
      }
    });

    //handling closing event
    ws.onclose = function (event) {
      console.log("Connection closed unexpectedly...");
    };
  } catch (error) {
    console.log(error);
  }
});
