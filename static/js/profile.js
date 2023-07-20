$(document).ready(function () {
    
    try {
        $("#remove-pic").on("click", function () {
            $("#profile-pic-box").css("background-image", "none");
            $("#profile-pic-letter").css("display", "flex");
        });    
    } catch (error) {
        console.log("error: ". error)
    }

});