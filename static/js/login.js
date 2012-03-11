$("#username").blur(function(){
    checkInput("#username",!$(this).val());
});
$("#password").blur(function(){
    checkInput("#password",!$(this).val());
});
$("#login").click(function(){
    readySubmit=true;
    $("#username").blur();
    $("#password").blur();
    if(!readySubmit)
        return false;
    $.post("/login",{
            username:$("#username").val(),
            password:$("#password").val()},
        function(data){
            if(data.status=="success")
                if(args.next)
                    location.href=args.next;
                else
                    location.href="/";
            else
                alert(data.message);
        },"json");
    return false;
});