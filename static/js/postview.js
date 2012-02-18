$("#submit").click(function(){
    readySubmit=true;
    $("#wmd-input").blur();
    if(!readySubmit)
        return false;
    $.post("/topics/"+postID+"/comment",{_xsrf:$("input[name='_xsrf']").val(),
            markdown:$("#wmd-input").val()},
        function(data){
            if(data.status=="success")
                location.reload();
            alert(data.message);
        },"json");
    return false;
});
