if(isChrome)
    $('#markdown-commands').html('<input id="wmd-input_speech" class="btn toolbar_button" x-webkit-speech onwebkitspeechchange="var f=function(t) {    var a=$(\'#wmd-input\');    a.val(a.val()+t.val());    $(\'#markdown-commands input\').val(\'\');    t.blur();    a.focusEnd();};f(this);" onclick="var f=function(t) {t.blur();};f(this);" lang="zh-CN"/>'+$('#markdown-commands').html());

$("#wmd-input").blur(function(){
    $.post("/markdown",{_xsrf:$("input[name='_xsrf']").val(),
            md:$("#wmd-input").val()},
        function(data){
            $("#md-preview").html(data);
        });
});