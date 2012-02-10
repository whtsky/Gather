readySubmit=false;
function checkInput(id,bool)
{
    if(bool)
    {
        readySubmit=false;
        $(id+"-t").show();
        $(id+"-g").addClass("error");
    }
    else
    {
        $(id+"-g").removeClass("error");
        $(id+"-t").hide();
    }
}
function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}
$("#newPost").click(function(){
  location.href="/topics/add";
});
