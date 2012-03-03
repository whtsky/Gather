$("#tweetsubmit").click(function(){
    if ($("#tweetcontent").val() == "")
        return false;
    $("#tweet").modal('hide');
    $.post("/twitter/tweet",{_xsrf:$("input[name='_xsrf']").val(),
            tweet:$("#tweetcontent").val()},
        function(data){
            $("#tweetcontent").val("");
        },"json");
    return false;
});
document.onkeyup=function(event) {
    if(window.ActiveXObject) {
        var keydown = window.event.keyCode;
        event=window.event;
    }else{
        var keydown = event.keyCode;
        if(event.ctrlKey && keydown == 13){
            if ($('body').hasClass('modal-open'))
                $('#tweetsubmit').click();
            else
                $('#submit').click();
        }
    }
};