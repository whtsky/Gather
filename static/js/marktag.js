var doing = false;
var tagname = $('#tagname').html();
$("#mark").click(function(){
    if(doing==true)
        return false;
    if($(this).hasClass('label-important')){
        doing=true;
        $.post("./"+tagname+"/mark",{_xsrf:$("input[name='_xsrf']").val()},
            function(data){
                $("#mark").removeClass('label-important');
                $("#mark").html('收藏');
                doing=false;
                $('#markedtag').text((parseInt($('#markedtag').text())-1).toString());
            });
    }else{
        doing=true;
        $.post("./"+tagname+"/mark",{_xsrf:$("input[name='_xsrf']").val()},
            function(data){
                $("#mark").addClass('label-important');
                $("#mark").html('取消收藏');
                doing=false;
                $('#markedtag').text((parseInt($('#markedtag').text())+1).toString());
            });
    }
    return false;
});