$("#old").blur(function(){
    checkInput("#old",(!$(this).val() || !$(this).val().match(/.{6,}$/)));
});
$("#new").blur(function(){
    checkInput("#new",(!$(this).val() || !$(this).val().match(/.{6,}$/)));
});
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

//*****************

$("#email").blur(function(){
    checkInput("#email",(!$(this).val() || !$(this).val().match(/^(\w)+(\.\w+)*@(\w)+((\.\w+)+)$/)));
});
