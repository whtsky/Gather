$("#title").blur(function(){
    checkInput("#title",(!$(this).val() || !$(this).val().match(/.{1,50}$/)));
});
$("#tags").blur(function(){
    checkInput("#tags",(!$(this).val() || !$(this).val().match(/.{1,}$/)));
});
$("#submit").click(function(){
    readySubmit=true;
    $("#title").blur();
    $("#wmd-input").blur();
    $("#tags").blur();
    if(!readySubmit)
        return false;
    $.post("/topics/add",{_xsrf:$("input[name='_xsrf']").val(),
            title:$("#title").val(),
            markdown:$("#wmd-input").val(),
            html:$("#html").val(),
            tags:$("#tags").val()},
        function(data){
            alert(data.message);
            if(data.status=="success")
                location.href="/topics/"+data.tid;
        },"json");
    return false;
});