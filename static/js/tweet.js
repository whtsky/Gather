$("#tweetsubmit").click(function(){
    if ($("#tweetcontent").val() == "")
        return false;
    $("#tweet").modal('hide');
    $("#tweetcontent").val("");
    $.post("/twitter/tweet",{_xsrf:$("input[name='_xsrf']").val(),
            tweet:$("#tweetcontent").val()},
        function(data){},"json");
    return false;
});