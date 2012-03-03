var doing = false;
$("#mark").click(function(){
    if(doing==true)
        return false;
    if($(this).hasClass('label-important')){
        doing=true;
        $.post("/topics/"+postID+"/mark",{_xsrf:$("input[name='_xsrf']").val()},
            function(data){
                $("#mark").removeClass('label-important');
                $("#mark").html('收藏');
                doing=false;
                $('#markedpost').text((parseInt($('#markedpost').text())-1).toString());
            });
    }else{
        doing=true;
        $.post("/topics/"+postID+"/mark",{_xsrf:$("input[name='_xsrf']").val()},
            function(data){
                $("#mark").addClass('label-important');
                $("#mark").html('取消收藏');
                doing=false;
                $('#markedpost').text((parseInt($('#markedpost').text())+1).toString());
            });
    }
    return false;
});

$(function() {
    $("#new_reply").live("ajax:success",
        function() {
            $(this).find("textarea").val("")
        }).live("ajax:error",
        function(a, b, c) {
            var d = $('<div class="alert-message error fade in"><a href="#" class="close">×</a><p></p></div>').alert();
            d.find("p").text(b.responseText),
                d.hide().prependTo($(this)).fadeIn("fast")
        }),
        $(".at").live("click",
            function(a) {
                var b = $("#wmd-input");
                b.focus().val(b.val() + "@" + $(this).data("user-name") + " "),
                    a.preventDefault()
            })
});