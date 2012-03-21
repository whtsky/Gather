$("#login").click(function(){
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