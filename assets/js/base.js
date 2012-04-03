function checkInput(id,bool){
    if(bool){
        readySubmit=false;
        $(id+"-g").addClass("error");
    }else
        $(id+"-g").removeClass("error");
}
jQuery.timeago.settings.strings = {
    prefixAgo: null,
    prefixFromNow: "从现在开始",
    suffixAgo: "之前",
    suffixFromNow: null,
    seconds: "不到 1 分钟",
    minute: "大约 1 分钟",
    minutes: "%d 分钟",
    hour: "大约 1 小时",
    hours: "大约 %d 小时",
    day: "1 天",
    days: "%d 天",
    month: "大约 1 个月",
    months: "%d 月",
    year: "大约 1 年",
    years: "%d 年",
    numbers: [],
    wordSeparator: ""
};
var init_article = function(){
    $('pre>code').each(function(i, e) {hljs.highlightBlock(e, '    ')});
}
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
    $('time').timeago();
    $("a[rel=popover]").popover()
    init_article();
    var doing = false;
    $("#mark").click(function(){
        if(doing)
            return false;
        doing=true;
        if($("#mark-show").hasClass('icon-heart-empty')){
            $.post("/topics/"+postID+"/mark",{},
                function(data){
                    $("#mark-show").removeClass('icon-heart-empty');
                    $("#mark-show").addClass('icon-heart')
                    doing=false;
                    $('#markedpost').text((parseInt($('#markedpost').text())+1).toString());
                });
        }else{
            $.post("/topics/"+postID+"/mark",{},
                function(data){
                    $("#mark-show").addClass('icon-heart-empty');
                    $("#mark-show").removeClass('icon-heart')
                    doing=false;
                    $('#markedpost').text((parseInt($('#markedpost').text())-1).toString());
                });
        }
        return false;
    });

    if (islogin){
        if (isadmin){
            $('.kill').removeClass('hide');
            $('#changetag-link').removeClass('hide');
        }
        all_user = $('#comments a[rel=popover]');
        for(var i=0;all_user[i];i++){
            user = $(all_user[i]);
            if (block_user.indexOf('.'+user.html()+'.') !== -1)
                user.parents('tr').hide();
        }
    }
    $('.kill').click(
        function(){
            return confirm("真的要和谐么")
        }
    );
    $("#tweetsubmit").click(function(){
        if ($("#tweetcontent").val() == "")
            return false;
        $("#tweet").modal('hide');
        $.post("/twitter/tweet",{
                tweet:$("#tweetcontent").val()},
            function(data){
                $("#tweetcontent").val("");
            },"json");
        return false;
    });
    document.onkeyup=function(event) {
        if(window.ActiveXObject) {
            var keydown = window.event.keyCode;
            event=window.event;
        }else{
            var keydown = event.keyCode;
            if(event.ctrlKey && keydown == 13){
                if ($('body').hasClass('modal-open'))
                    $('#tweetsubmit').click();
                else
                    $('#submit').click();
            }
        }
    };
    $('#search_form').submit(function(e){
        e.preventDefault();
        search();
    });
    function search(){
        window.open('http://www.google.com/search?q=site:' + location.href.split('/')[2] + ' ' + $('#q').val(), '_blank');
        return false;
    }
});