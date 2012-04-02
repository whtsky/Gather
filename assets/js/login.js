$("#login").click(function(){
    $.post("/login",{
            username:$("#username").val(),
            password:$("#password").val()},
        function(data){
            if(data.status=="success"){
                next = location.href.match(/next=.+/);
                location.href=next?decodeURIComponent(next[0].split('=')[1]):'/';
            }else
                alert(data.message);
        },"json");
    return false;
});