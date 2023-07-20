$(document).ready(function () {
    
    try {
        
        $("#create-group-form").submit(function(e) {
            e.preventDefault(); 
        
            var selectedContacts = [];
        
            $(".phone-checkbox:checked").each(function() {
              selectedContacts.push($(this).val()); 
            });
    
            if(selectedContacts.length >= 2){
                this.submit();
            }else{
                alert("Your group must have at least 2 contacts")
            }
        
        });

    } catch (error) {
        console.log("error: ".error)
    }


});