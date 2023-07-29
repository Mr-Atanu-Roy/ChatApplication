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
                                <a href="${data[index]["url"]}"
                                    class="mx-1.5 md:mx-3.5 lg:mx-0 p-3 grid grid-cols-6 place-items-center hover:bg-light-dark transition-colors duration-300 cursor-pointer rounded">
                                    <div class="col-span-1 overflow-hidden w-14 h-14 rounded-full bg-cover bg-no-repeat bg-center"
                                        style="background-image: url('${data[index]["chat_pic"]}');"></div>
                                    <div class="ml-3.5 lg:ml-3 col-span-5 w-full overflow-hidden text-white pl-3.5 lg:pl-5 2xl:p-0">
                                        <p class="font-bold text-lg">${data[index]["name"]}</p>
                                        <p class="font-bold text-xs text-gray-400">${data[index]["desc"] == null ? "" : data[index]["desc"]}</p>
                                    </div>
                                </a>`;
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