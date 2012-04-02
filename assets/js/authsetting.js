$('#imgur_form').submit(function(){
    button = $('#imgur_form button');
    button.html('正在绑定...');
    button.attr("disabled","disabled");
    $.post('/imgur/oauth',{
        username:$('#imgur_username').val(),
        password:$('#imgur_password').val()
    }).success(function(){location.reload();}).error(
        function() {
            alert("绑定失败，请检查用户名或密码是否正确");
            button = $('#imgur_form button');
            button.removeAttr("disabled");
            button.html('绑定imgur');
        }
    );
    return false;
});

$("#old").blur(function(){
    checkInput("#old",$(this).val().match(/.{6,}$/));
});
$("#new").blur(function(){
    checkInput("#new",$(this).val().match(/.{6,}$/));
});
$("#changepassword").click(function(){
    readySubmit=true;
    $("#old").blur();
    $("#new").blur();
    if(readySubmit)
        if($("#old").val()==$("#new").val())
            alert('新旧密码一样你还改什么啊。。');
        else
            $.post("/setting/password",{
                    old:$("#old").val(),
                    new:$("#new").val()},
                function(data){
                    if(data.status=="success"){
                        $("#old").val("");
                        $("#new").val("");
                    }
                    alert(data.message);
                },"json");
    return false;
});