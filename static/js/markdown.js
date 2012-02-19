var speech_fake=function() {
    var a=$('#wmd-input');
    var t=$('#markdown-commands input')
    a.val(a.val()+t.val());
    t.blur();
    a.focusEnd();
};

if(isChrome){
    $('#markdown-commands').html('<input id="wmd-input_speech" class="btn toolbar_button" x-webkit-speech onwebkitspeechchange="speech_fake();" onclick="this.blur();" lang="zh-CN"/>'+$('#markdown-commands').html());
    $('#markdown-commands input').blur(function(){
      this.value="";
    });
}
$("#wmd-input").blur(function(){
    $.post("/markdown",{_xsrf:$("input[name='_xsrf']").val(),
            md:$("#wmd-input").val()},
        function(data){
            $("#md-preview").html(data);
        });
});