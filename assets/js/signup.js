$("#username").blur(function(){
    checkInput("#username",(!$(this).val() || !$(this).val().match(/[\u4e00-\u9fa5A-Za-z0-9]{1,30}$/)));
});
$("#email").blur(function(){
    checkInput("#email",(!$(this).val() || !$(this).val().match(/^(\w)+(\.\w+)*@(\w)+((\.\w+)+)$/)));
});
$("#password").blur(function(){
    checkInput("#password",(!$(this).val() || !$(this).val().match(/.{6,}$/)));
});
$("#password-ag").blur(function(){
    checkInput("#password-ag",($(this).val()!=$("#password").val()));
});
$("#submit").click(function(){
    readySubmit=true;
    $("#username").blur();
    $("#email").blur();
    $("#password").blur();
    $("#password-ag").blur();
    if(!readySubmit)
        return false;
    $.post("/signup",{
            username:$("#username").val(),
            email:$("#email").val(),
            password:$("#password").val()},
        function(data){
            if(data.status=="success"){
                if(args.next)
                    location.href=args.next;
                else
                    location.href="/";
            }
            else
                alert(data.message);
        },"json");
    return false;
});