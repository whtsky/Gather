$("#submit").click(function(){
    readySubmit=true;
    $("#markdown").blur();
    if(!readySubmit)
        return false;
    $.post("/topics/"+postID+"/comment",{_xsrf:$("input[name='_xsrf']").val(),
            markdown:$("#markdown").val(),
            html:$("#html").val()},
        function(data){
            alert(data.message);
            if(data.status=="success")
                location.reload();
        },"json");
    return false;
});
