//getting the other user phone
const OTHER_USER_PHONE = JSON.parse(
    document.getElementById("other_user_phone").textContent
);
       
//getting current user phone
const PHONE = JSON.parse(
    document.getElementById("current_user_phone").textContent
);

//getting the group id
const GROUP_NAME = JSON.parse(
document.getElementById("group_name").textContent
);


// func to set header in chat
function set_header(content=OTHER_USER_PHONE) {
    $("#online-users").css("display", "none");
    $("#online-users").html(content);
    $("#online-users").fadeIn();
}
  
// func to set online user
function online() {
    let content = `<i class="fa fa-circle text-green-0 transition-colors mr-2"></i> Online`;
    set_header(content);
}
  
//func for handling user join task for other user
function user_join(phone, user_phone) {
    if (phone != user_phone) {
        online();
    }
}
  
//func for handling user leave task for other user
function user_leave(phone, user_phone, last_seen) {
    if(phone != user_phone){
        if(last_seen=="" || last_seen==null){
            content = phone;
        }else{
            content = "last seen: "+last_seen;
        }
        set_header(content);
    }
}


//func for handling user join task for self
function user_list(online_users_num = 0, last_seen) {
    //setting online users when user join
    if(online_users_num > 0){
        online();
    }else{
        if(last_seen!="" && last_seen!=null){
            set_header("last seen: "+last_seen);
        }
    }
}



$(document).ready(function () {
    try {

        
        //setting the header to show other user phone when page loaded
        set_header();
        
        //scroll to bottom
        location.href = "#end";

        //scroll to bottom btn
        $("#scroll_to_bottom_btn").on("click", function () {
            location.href = "#end";            
        });


        //creating a websocket con to: /api/chat/personal/<group-name>/
        const ws = new WebSocket(
        "ws://" + window.location.host + "/api/chat/personal/" + GROUP_NAME + "/"
        );

        //handling text msg submit
        $("#send-msg-btn").on("click", function (e) {
            e.preventDefault();
    
            let msg = $("#input-message").val().trim();
            if (msg != "") {
                ws.send(
                    JSON.stringify({
                        msg_type: "text",
                        msg: msg,
                    })
                );
                $("#input-message").val("");
                $("#input-message").focus();
            }
        });

        //msg from server
        ws.onmessage = function (event) {
            const data = JSON.parse(event.data);

            if (data.type == "chat.message") {
                let msg = data.message;
                let msg_type = data.msg_type;
                let phone = data.user_phone;
                
                if (msg_type == "text") {
                    let time = data.time;

                    let content = `
                    <div class="my-2 w-full flex `;
                    if (PHONE == phone) {
                        content += `justify-end`;
                    }
                    content += `">
                        <div class="flex flex-col `;
                        if(PHONE == phone){
                            content += `items-end`;
                        }
                        content += `">
                            <div class="max-w-[18rem] sm:max-w-sm md:max-w-md py-2 my-1 px-3 text-white bg-green-0 w-fit rounded-lg `;
                            if (PHONE == phone) {
                                content += `rounded-tr-none`;
                            } else {
                                content += `rounded-tl-none`;
                            }
                            content += `">
                                <p class="break-words">${msg}</p>
                            </div>
                            <p class="text-gray-300 text-xs text-right">${time}</p>
                        </div>
                    </div>`;
                    
                      //append to chat messages at end
                      $("#group-chat-msg").append(content);
          
                      //scroll to bottom
                      location.href = "#end";
          
                }else if(msg_type == "file"){
                    if(msg.length > 0){
                        msg.forEach(obj => {
                            let obj_msg_type = obj["file_type"];

                            if(obj_msg_type == "img"){
                                let content = `
                                <div class="my-2 w-full flex items-center `;
                                    if (PHONE == phone) {
                                        content += `justify-end`;
                                    }
                                    content += `">
                                    <div class="flex flex-col">
                                        <div class="max-w-[18rem] sm:max-w-sm md:max-w-md py-1.5 my-1 px-2 text-white bg-green-0 w-fit rounded-lg `;
                                        if (PHONE == phone) {
                                            content += `rounded-tr-none`;
                                        }else{
                                            content += `rounded-tl-none`;
                                        }
                                            content += `">
                                            <div class="flex items-center justify-center text-slate-900 font-bold text-xs relative">
                                                <img src="${obj["file_url"]}" alt="${obj_msg_type}" class="w-56 xs:w-64 sm:w-72 md:w-80 h-auto" loading="lazy">
                                                <div class="opacity-0 h-full w-full absolute top-0 left-0 transition-all duration-300 backdrop-brightness-50 flex items-center justify-center hover:opacity-100">
                                                    <a target="_blank" href="${obj["file_url"]}" download="${obj["file_url"]}" class="text-2xl text-white text-center">
                                                        <i class="fa fa-arrow-circle-o-down"></i>
                                                        <p class="text-white text-base">Download</p>
                                                    </a>
                                                </div>
                                            </div>
                                        </div>
                                        <p class="text-gray-300 text-xs text-right">${obj["created_at"]}</p>
                                    </div>
                                </div>`;
            
                                //append to chat messages at end
                                $("#group-chat-msg").append(content);
                      
                                //scroll to bottom
                                location.href = "#end";
                            }else if(obj_msg_type == "video"){
                                content = `
                                <div class="my-2 w-full flex items-center `;
                                    if (PHONE == phone) {
                                    content += `justify-end`;
                                    }
                                    content += `">
                                    <div class="flex flex-col">
                                    <div class="max-w-[18rem] sm:max-w-sm md:max-w-md py-1.5 my-1 px-2 text-white bg-green-0 w-fit rounded-lg `; 
                                    if (PHONE == phone) {
                                    content += `rounded-tr-none`;
                                    } else {
                                    content += `rounded-tl-none`;
                                    }
                                    content += `">
                                    <a target="_blank" href="${obj["file_url"]}" class="flex items-center justify-center text-slate-900 font-bold text-xs">
                                                <video class="w-56 xs:w-64 sm:w-72 md:w-80 h-auto" controls>
                                                    <source src="${obj["file_url"]}" type="video/${obj["file_ext"]}" loading="lazy">
                                                </video>
                                            </a>
                                        </div>
                                        <p class="text-gray-300 text-xs text-right">${obj["created_at"]}</p>
                                    </div>
                                </div>`;
            
                                //append to chat messages at end
                                $("#group-chat-msg").append(content);
                                
                                //scroll to bottom
                                location.href = "#end";
                            }else if(obj_msg_type == "audio"){
                                content = `
                                <div class="my-2 w-full flex items-center `;
                                    if (PHONE == phone) {
                                    content += `justify-end`;
                                    }
                                    content += `">
                                    <div class="flex flex-col">
                                    <div class="max-w-[18rem] sm:max-w-sm md:max-w-md py-1.5 my-1 px-2 text-white w-fit rounded-lg `; 
                                    if (PHONE == phone) {
                                    content += `rounded-tr-none`;
                                    } else {
                                    content += `rounded-tl-none`;
                                    }
                                    content += `">
                                    <div class="flex items-center justify-center text-slate-900 font-bold text-xs">
                                                <audio class="w-56 xs:w-64 sm:w-72 md:w-80" controls>
                                                    <source src="${obj["file_url"]}" type="audio/${obj["file_ext"]}" loading="lazy">
                                                </audio>
                                            </div>
                                        </div>
                                        <p class="text-gray-300 text-xs text-right">${obj["created_at"]}</p>
                                    </div>
                                </div>`;
            
                                //append to chat messages at end
                                $("#group-chat-msg").append(content);
            
                                //scroll to bottom
                                location.href = "#end";
                            }else if(obj_msg_type == "doc"){
                                content = `
                                <div class="my-2 w-full flex items-center `;
                                if (PHONE == phone) {
                                content += `justify-end`;
                                }
                                content += `">
                                    <div class="flex flex-col">
                                    <div class="max-w-[18rem] sm:max-w-sm md:max-w-md p-2.5 my-1 text-white bg-green-0 w-fit rounded-lg `;
                                    if (PHONE == phone) {
                                        content += `rounded-tr-none`;
                                    } else {
                                        content += `rounded-tl-none`;
                                    }
                                    content += `">
                                    <div class="border-2 rounded p-2.5 w-48 xs:w-56 sm:w-64 md:w-72">
                                                <div class="flex flex-col sm:flex-row items-center justify-evenly text-slate-900 font-bold text-xs">
                                                    <div class="flex items-center justify-center mb-1.5 w-14 h-14 sm:mr-3 sm:mb-0">`;
                                                    if(obj["file_ext"] == "pdf"){
                                                    content += `<img src="/static/images/icons/pdf.png" alt="${obj["file_ext"]}" class="w-full h-full">`;
                                                    }else if(obj["file_ext"] == "doc" || obj["file_ext"] == "docx"){
                                                    content += `<img src="/static/images/icons/doc.png" alt="${obj["file_ext"]}" class="w-full h-full">`;
                                                    }else if(obj["file_ext"] == "ppt" || obj["file_ext"] == "pptx"){
                                                    content += `<img src="/static/images/icons/ppt.png" alt="${obj["file_ext"]}" class="w-full h-full">`;
                                                    }else{
                                                    content += `<img src="/static/images/icons/txt.png" alt="${obj["file_ext"]}" class="w-full h-full">`;
                                                    }
                                                        
                                        content += `</div>
                                                    <div class="w-full sm:w-fit">
                                                        <p class="text-white text-sm break-words">${obj["file_name"]}</p>
                                                        <p class="text-xs text-gray-700 mt-1 break-words">${obj["file_size"].toString().slice(0,4)} MB `;
                                                        if(obj["file_ext"] == "pdf"){
                                                        content += `PDF`;
                                                        }else if(obj["file_ext"] == "doc" || obj["file_ext"] == "docx"){
                                                        content += `MS Word`;
                                                        }else if(obj["file_ext"] == "ppt" || obj["file_ext"] == "pptx"){
                                                        content += `MS Powerpoint`;
                                                        }
                                                content += `Document</p>
                                                    </div>
                                                </div>
                                                <div class="flex flex-col sm:flex-row justify-between items-center mb-1 mt-3">
                                                    <a href="${obj["file_url"]}" target="_blank" class="py-2.5 px-2 w-full mb-2 sm:mb-0 sm:w-1/2 sm:mr-2 text-center uppercase text-white rounded transition-colors duration-300 bg-gray-700 hover:bg-gray-800 text-xs sm:text-sm">open file</a>
                                                    <a href="${obj["file_url"]}" target="_blank" download="${obj["file_url"]}" class="py-2.5 px-2 w-full sm:w-1/2 text-center uppercase text-white rounded transition-colors duration-300 bg-gray-700 hover:bg-gray-800 text-xs sm:text-sm">download</a>
                                                </div>
                                            </div>
                                        </div>
                                        <p class="text-gray-300 text-xs text-right">${obj["created_at"]}</p>
                                    </div>
                                </div>`;
            
                            //append to chat messages at end
                            $("#group-chat-msg").append(content);
                            
                            //scroll to bottom
                            location.href = "#end";
                            }
                        });
                    }
                }

            }else if (data.type == "user.list") {
                //new user joins and gets informed of other user is online or offline
                user_list(data.online_num, data.last_seen);
            } else if (data.type == "user.join") {
                //new user joins and other user get notified about it
                user_join(data.phone, PHONE);
            } else if (data.type == "user.leave") {
                //new user joins and other user get notified about it
                user_leave(data.phone, PHONE, data.last_seen);
            } else {
                console.log("error: Invalid message type");
            }
        }

        //handling file msg
        $("#file-msg").click(function (e) {
            $("#file-msg").on("change", function (event) {
                var fileCount = event.target.files.length;
        
                //show the submit btn only if file is present
                if (fileCount > 0) {
                    $("#select-file-msg-btn").fadeOut(55);
                    $("#send-file-btn").html("send " + fileCount + " file");
                    $("#send-file-btn").fadeIn();
                    $("#cancel-file-send").fadeIn();
                }
            });
        });

        //cancel file input
        $("#cancel-file-send").on("click", function () {
            $("#cancel-file-send").fadeOut(55);
            $("#send-file-btn").fadeOut(55);
            $("#select-file-msg-btn").fadeIn();
            $("#file-msg").val("");
        });
  
        //sending file data
        $("#send-file-btn").on("click", function (e) {
            e.preventDefault();
    
            var formData = new FormData(document.getElementById("file-msg-form"));
            //adding group id to form data
            formData.append("group_id", GROUP_NAME);
    
            $.ajax({
            type: "POST",
            url: "/api/msg/upload-file/",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                let error = response["error"];
                let data = response["data"];
                let status = response["status"];
    
                if (data.length == 0) {
                    $("#popup-message").html("Error : " + error);
                    $("#btn-2-box").css("display", "none");
                    $("#popup-alert").css("display", "flex");
                } else if (data.length > 0 && error == null && status == 201) {
                    $("#send-file-btn").fadeOut(55);
                    $("#cancel-file-send").fadeOut(55);
                    $("#select-file-msg-btn").fadeIn();
                    //sending the data to websocket
                    ws.send(
                        JSON.stringify({
                            msg_type: "file",
                            files: data,
                        })
                    );
                }
            },
            });
        });

        //handling error
        ws.onerror = function (event) {
            console.log("error occurred: ", event.message);
            console.log("Closing connection.");
            ws.close();
        };
        
        //handling closing event
        ws.onclose = function (event) {
            console.log("Connection closed unexpectedly...");
        };
  

    } catch (error) {
      console.log(error);
    }
  });
  