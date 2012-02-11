$("#old").blur(function(){
    checkInput("#old",(!$(this).val() || !$(this).val().match(/.{6,}$/)));
});
$("#new").blur(function(){
    checkInput("#new",(!$(this).val() || !$(this).val().match(/.{6,}$/)));
});
$("#old-t").hide();
$("#new-t").hide();
$("#changepassword").click(function(){
    readySubmit=true;
    $("#old").blur();
    $("#new").blur();
    if(!readySubmit)
        return false;
    if($("#old").val()==$("#new").val()){
        alert('新旧密码一样你还改什么啊。。');
        return false;
    }
    $.post("/setting/password",{_xsrf:$("input[name='_xsrf']").val(),
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

//*****************

$("#email").blur(function(){
    checkInput("#email",(!$(this).val() || !$(this).val().match(/^(\w)+(\.\w+)*@(\w)+((\.\w+)+)$/)));
});
$("#submit").click(function(){
    readySubmit=true;
    $("#email").blur();
    if(!readySubmit)
        return false;
    $.post("/setting",{_xsrf:$("input[name='_xsrf']").val(),
            email:$("#email").val(),
            website:$("#website").val(),
            location:$("#location").val(),
            twitter:$("#twitter").val(),
            github:$("#github").val()},
        function(data){
            alert(data.message);
            if(data.status=="success")
                location.href="/user/"+$("#username").val();
        },"json");
    return false;
});