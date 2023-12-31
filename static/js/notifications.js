
//func to format date
function format_date(date){

    date = new Date(date);

    // Format the date using toLocaleString
    let formattedDate = date.toLocaleString('en-US', {
        day: 'numeric',
        month: 'long',
        year: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        hour12: true
    });

    return formattedDate;
}



//func to fetch all notifications
function fetch_all_notification() {

    $.ajax({
        type: "get",
        url: "/api/notifications/load",
        success: function (response) {
            let status = response.status;
            let error = response.error;
            let data = response.data;
            let content = ``;
            
            if(status == 200 && data != null){
                for (let index = 0; index < data.length; index++) {
                    let img = 'bot';
                    if(data[index].notification_type == "group"){
                        img = "group";
                    }else if(data[index].notification_type == "personal"){
                        img = "person";
                    }
                    content += `
                    <div class="notification-box w-full flex items-start justify-start px-2 py-4">
                        <div class="w-12">
                            <img class="w-full" src="/static/images/icons/${img}.png" alt="${img}" loading="lazy">
                        </div>
                        <div class="ml-4 w-full">
                            <div class="flex justify-between items-center mb-1.5">
                                <p class="text-white text-sm">${data[index].message}</p>
                                <div data-id="${data[index].id}" class="delete-notification-btn bg-red-200 hover:bg-red-300 transition-colors cursor-pointer rounded-[0.18rem] flex items-center justify-center p-1.5">
                                    <i class="fa fa-trash text-red-800"></i>
                                </div>
                            </div>
                            <p class="text-gray-500 text-xs text-right">${format_date(data[index].created_at)}</p>
                        </div>
                    </div>
                    `;                
                }

                $("#notifications").html(content);
            }else if(status == 204 && error == ""){
                content = `<p class="text-gray-500 text-sm">You don't have any notifications yet...</p>`
                $("#notifications").html(content);
            }else{
                content = `<p class="text-gray-500 text-sm">Failed to load notifications...</p>`
                $("#notifications").html(content);
            }
        }
    });


}



//func to fetch all friend requests
function fetch_all_friend_requests() {
    let notification_type = $("input[name='friend-req-type']:checked").val() != "send" ? "received" : "send";

    $.ajax({
        type: "get",
        url: "/api/friend_requests/load",
        data: {
            "notification_type": notification_type
        },
        success: function (response) {
            let status = response.status;
            let error = response.error;
            let data = response.data;
            let content = ``;
            
            if(status == 200 && data != null){
                console.log(response)
                if(notification_type == "send"){
                    for (let index = 0; index < data.length; index++) {
                        content += `
                        <div class="w-full flex items-start justify-start p-2.5">
                            <a href="/chat/personal/p/${data[index].request_for__id}" class="w-12">
                                <img class="w-full" src="/static/images/icons/bot.png" alt="bot" loading="lazy">
                            </a>
                            <div class="ml-4 w-full">
                                <p class="text-white text-sm mb-2">You have send a friend request to ${data[index].request_for__first_name} ${data[index].request_for__last_name}</p>
                                <div class="flex items-center justify-between">
                                    <p class="text-gray-500 text-xs text-right">${format_date(data[index].created_at)}</p>
                                    <div class="flex items-start justify-between">`;
                                        if(data[index].status == true && data[index].seen == true){
                                            content += `<button class="text-white font-semibold py-1 px-3 rounded bg-light-dark capitalize">accepted</button>
                                            <div class="flex items-start justify-between">`;
                                        }else if(data[index].status == false && data[index].seen == true){
                                            content += `<button class="mr-2.5 text-white font-semibold py-1 px-3 rounded bg-light-dark capitalize">declined</button>`;
                                        }else{
                                            content += `<button class="mr-2.5 text-white font-semibold py-1 px-3 rounded bg-light-dark capitalize">pending</button>`;
                                        }
                            content += `</div>
                            </div>
                            </div>
                            </div>
                        </div>
                        `;                
                    }

                }else{
                    for (let index = 0; index < data.length; index++) {
                        content += `
                        <div class="w-full flex items-start justify-start p-2.5">
                            <a href="/chat/personal/p/${data[index].request_for__id}" class="w-12">
                                <img class="w-full" src="/static/images/icons/bot.png" alt="bot" loading="lazy">
                            </a>
                            <div class="ml-4 w-full">
                                <p class="text-white text-sm mb-2">You have a new friend request from ${data[index].request_from__first_name} ${data[index].request_from__last_name}</p>
                                <div class="flex items-center justify-between">
                                    <p class="text-gray-500 text-xs text-right">${format_date(data[index].created_at)}</p>
                                    <div class="flex items-start justify-between">`;
                                        if(data[index].status == true && data[index].seen == true){
                                            content += `<button class="text-white font-semibold py-1 px-3 rounded bg-light-dark capitalize">accepted</button>
                                            <div class="flex items-start justify-between">`;
                                        }else if(data[index].status == false && data[index].seen == true){
                                            content += `<button class="mr-2.5 text-white font-semibold py-1 px-3 rounded bg-light-dark capitalize">declined</button>`;
                                        }else{
                                            content += `<div class="flex items-start justify-between">
                                            <button id="accept-request" class="mr-4 text-white font-semibold py-1 px-3 rounded transition-colors capitalize duration-300 bg-green-0 hover:bg-green-0-dark" data-id="${data[index].id}">Accept</button>
                                            <button id="decline-request" class="text-white font-semibold py-1 px-3 rounded transition-colors duration-300 capitalize bg-red-600 hover:bg-red-700" data-id="${data[index].id}">Decline</button>
                                            </div>`;
                                        }
                            content += `</div>
                            </div>
                            </div>
                            </div>
                        </div>
                        `;                
                    }
                }

                $("#notifications").html(content);
            }else if(status == 204 && error == ""){
                content = `<p class="text-gray-500 text-sm">You`; 
                if(notification_type == "send"){
                    content += ` have not send `;
                }else{
                    content += ` don't have `;
                }
                content += `any friend requests yet...</p>`
                $("#notifications").html(content);
            }else{
                content = `<p class="text-gray-500 text-sm">Failed to load friend requests...</p>`
                $("#notifications").html(content);
            }
        }
    });


}



$(document).ready(function () {
    try {

        //PAGE LOADS
        //adding bg color to all notification tab
        $("#friend-req-notifications").css("background", "#1C1C24");
        $("#all-notifications").css("background", "#018569");
        //calling the func to fetch notification
        fetch_all_notification();

        //ALL NOTIFICATION TAB
        //adding bg color to all notification tab when clicked
        $("#all-notifications").on("click", function (e) {
            $("#friend-req-notifications").css("background", "#1C1C24");
            $("#friend-req-type-box").css("display", "none");
            $("#all-notifications").css("background", "#018569");
            fetch_all_notification();
        });


        //FRIEND REQUESTS TAB
        //adding bg color to friend request tab and making request type visible when clicked
        $("#friend-req-notifications").on("click", function (e) {
            $("#all-notifications").css("background", "#1C1C24");
            $("#friend-req-notifications").css("background", "#018569");
            $("#friend-req-type-box").css("display", "flex");
            fetch_all_friend_requests();    
        });

        //FRIEND REQUESTS TYPE TAB
        //getting friend request when type is changed
        $("#friend-req-type-box").on("change", function (e) {
            fetch_all_friend_requests();    
        });
        


        //DECLINE FRIEND REQUEST
        $(document).on("click", "#decline-request", function () {
            let parent = $(this).parent()
            $.ajax({
                type: "post",
                url: "/api/friend_requests/decline/",
                data: {
                    request_id : $(this).data("id")
                },
                success: function (response) {
                    let status = response.status;
                    let error = response.error;
                    let data = response.data;

                    if(status == 201 && data.update_status == true && error == null){
                        let content = `<button class="mr-2.5 text-white font-semibold py-1 px-3 rounded bg-light-dark capitalize">declined</button>`;
                        parent.html(content);
                    }else{
                        let content = `<p class="text-xs text-gray-500">something went wrong</p>`;
                        parent.html(content);
                    }
                },
                error: function (response) {
                    alert("something went wrong. Try again later...");
                }
            });
        });

        //ACCEPT FRIEND REQUEST
        $(document).on("click", "#accept-request", function () {
            let parent = $(this).parent()
            $.ajax({
                type: "post",
                url: "/api/friend_requests/accept/",
                data: {
                    request_id : $(this).data("id")
                },
                success: function (response) {
                    let status = response.status;
                    let error = response.error;
                    let data = response.data;

                    if(status == 201 && data.update_status == true && error == null){
                        let content = `<button class="mr-2.5 text-white font-semibold py-1 px-3 rounded bg-light-dark capitalize">accepted</button>`;
                        parent.html(content);
                    }else{
                        let content = `<p class="text-xs text-gray-500">something went wrong</p>`;
                        parent.html(content);
                    }
                },
                error: function (response) {
                    alert("something went wrong. Try again later...");
                }
            });
        });

        //DELETE NOTIFICATION
        $(document).on("click", ".delete-notification-btn", function () {
            let id = $(this).data("id");

            $.ajax({
                type: "post",
                url: "/api/notifications/delete/",
                data: {notification_id: id},
                success: function (response) {
                    let status = response.status;
                    let error = response.error;
                    let data = response.data;

                    if(data["deleted"] == true && status == 204 && error == null){
                        fetch_all_notification();
                    }
                },
                error: function (response) {
                    alert("something went wrong. Try again later...");
                }
            });
        });
        
    

    } catch (error) {
      console.log("error: ".error);
    }
});

