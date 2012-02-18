$("#markdown").blur(function(){
    checkInput("#tags",(!$(this).val() || !$(this).val().match(/.{1,}$/)));
    $.post("/markdown",{_xsrf:$("input[name='_xsrf']").val(),
            md:$("#markdown").val()},
        function(data){
            $("#preview").html(data);
        },"html");
});