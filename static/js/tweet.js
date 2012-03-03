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