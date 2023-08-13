$(document).ready(function () {
    
    try {

        //when something is searched in search bar
        $(document).on("keyup", "#search-chats", function () {
            
            //get the initial groups
            let old_content = $("#chat-records").html();

            //get the search box val
            query = $(this).val().trim();
            if(query != ""){
                $.ajax({
                    type: "get",
                    url: "/api/chat_search/",
                    data: {
                        "query": query,
                    },
                    success: function (response) {
                        let status = response.status;
                        let data = response.data;
                        let error = response.error;
                        let content = ``;

                        if(error == null && status == 200){
                            for (let index = data.length - 1; index >= 0; index--) {
                                content += `
                                <div class="py-2 sm:px-2 flex items-center justify-between hover:bg-light-dark transition-colors duration-300 cursor-pointer rounded">
                                    <a href="${data[index]["url"]}" class="w-full flex items-center justify-start">
                                        <div class="mr-2.5 sm:mr-3.5 text-white text-3xl col-span-1 overflow-hidden w-16 h-16 rounded-full bg-cover bg-no-repeat bg-center flex items-center justify-center `;
                                        if(data[index]["chat_pic"].includes("media/None")){
                                            content += `border-green-0 border-[3.1px] border-solid">
                                            ${data[index]["name"][0]}`;
                                        }else{
                                            content += `" style="background-image: url('${data[index]["chat_pic"]}');">`;
                                        }
                                        content += `
                                        </div>
                                        <div>
                                            <p class="font-bold text-lg text-white">${data[index]["name"].length > 24 ? data[index]["name"].substring(0, 24)+'...' : data[index]["name"]}</p>
                                            <p class="font-bold text-xs text-gray-400">`;
                                                if(data[index]["desc"] != null){
                                                    if(data[index]["desc"].length > 45){
                                                        data[index]["desc"].substring(0, 45)+'...';
                                                    }else{
                                                        data[index]["desc"];
                                                    }
                                                }
                                            content += `</p>
                                        </div>
                                    </a>
                                </div>`;
                            }
                        }else if(status == 204 && error == "nothing found"){
                            content += `<p class="pl-4 capitalize text-white text-sm font-bold">${error}</p>`;
                        }else{
                            console.log(error);
                        }
                        
                        //show the content
                        $("#chat-records").html(content);
                    }
                });
            }else{
                $("#chat-records").html(old_content);
            }

        });

    } catch (error) {
        console.log("error: ".error)
    }


});