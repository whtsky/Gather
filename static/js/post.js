$("#title").blur(function(){
    checkInput("#title",(!$(this).val() || !$(this).val().match(/.{5,50}$/)));
});
$("#markdown").blur(function(){
    checkInput("#markdown",!$(this).val());
    $.post("/markdown",{_xsrf:$("input[name='_xsrf']").val(),
            md:$("#markdown").val()},
        function(data){
            $("#preview").html(data);
        },"html");
});
$("#tags").blur(function(){
    checkInput("#tags",(!$(this).val() || !$(this).val().match(/.{1,}$/)));
});
$("#title-t").hide();
$("#markdown-t").hide();
$("#tags-t").hide();
$("#submit").click(function(){
    readySubmit=true;
    $("#title").blur();
    $("#markdown").blur();
    $("#tags").blur();
    if(!readySubmit)
        return false;
    $.post("/topics/add",{_xsrf:$("input[name='_xsrf']").val(),
            title:$("#title").val(),
            markdown:$("#markdown").val(),
            html:$("#html").val(),
            tags:$("#tags").val()},
        function(data){
            alert(data.message);
            if(data.status=="success")
                location.href="/topics/"+data.tid;
        },"json");
    return false;
});