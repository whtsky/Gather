var speech_fake=function() {
    var a=$('#wmd-input');
    var t=$('#markdown-commands input')
    a.val(a.val()+t.val());
    t.blur();
    a.focusEnd();
};

if(isChrome){
    $('#markdown-commands').html('<div class="left"><input id="wmd-input_speech" class="btn" x-webkit-speech onwebkitspeechchange="speech_fake();" onclick="this.blur();" lang="zh-CN"/></div>'+$('#markdown-commands').html());
    $('#markdown-commands input').blur(function(){
      this.value="";
    });
}
$("#wmd-input").blur(function(){
    window.onbeforeunload = function(){
        if ($("#wmd-input").val().length > 0)
            return "离开本页面会导致编辑的内容丢失！";
    }
    $.post("/markdown",{
            md:$("#wmd-input").val()},
        function(data){
            $("#md-preview").html(data);
            $('pre>code').each(function(i, e) {hljs.highlightBlock(e, '    ')});
        });
});
$(document).ready(function(){
    $('#submit').click(function(){
        window.onbeforeunload = null;
    });
});
