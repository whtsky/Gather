ajaxNum=1;
function ajaxComment()
{
    $.post("/topics/{{ post['_id'] }}",{_xsrf:$("input[name='_xsrf']").val(),
            start_num:ajaxNum},
        function(data){
            $("#comments").append(data);
        },"html");
    ajaxNum=ajaxNum+10;
    alert(ajaxNum+" "+commentNum);
    if(ajaxNum>commentNum)
    {
        $("#more").hide();
    }
    else
    {
        $("#more").show();
    }
}
ajaxComment();
$("#more").click(function(){
    ajaxComment();
});
$("#markdown").blur(function(){
    checkInput("#markdown",!$(this).val());
    $.post("/markdown",{_xsrf:$("input[name='_xsrf']").val(),
            md:$("#markdown").val()},
        function(data){
            $("#preview").html(data);
        },"html");
});
$("#markdown-t").hide();
$("#submit").click(function(){
    readySubmit=true;
    $("#markdown").blur();
    if(!readySubmit)
        return false;
    $.post("/topics/{{ post['_id'] }}/comment",{_xsrf:$("input[name='_xsrf']").val(),
            markdown:$("#markdown").val(),
            html:$("#html").val()},
        function(data){
            alert(data.message);
            if(data.status=="success")
                location.reload();
        },"json");
    return false;
});