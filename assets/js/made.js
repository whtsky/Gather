
function update(mode) {
    var source = $.trim(editor.getSession().getValue());
    $.post("/notes/raw/"+note_id,{
            md:source},
        function(data){
            $('#preview').html(data);
        });
    setTimeout(update, 2000);
}
function onresize() {
    var view_h = $(this).height();
    var view_w = $(this).width();
    $('#container').height(view_h - $('#bar').height() - 1);
    $('#container').children('.pane')
        .height(view_h - $('#bar').height - 5);
    $('#input').width(parseInt(view_w/2)+10);
    $('#preview_pane').width(parseInt(view_w/2)-20);
}
function change_theme(theme) {
    if (theme == 'dark') {
        $('.ace_scroller, .ace_sb, .ace_editor').addClass('dark');
        editor.setTheme("ace/theme/twilight");
    } else {
        $('.ace_scroller, .ace_sb, .ace_editor').removeClass('dark');
        editor.setTheme("ace/theme/textmate");
    }
}

function resume_state() {
    $.get("/notes/raw/"+note_id,{},
        function(data){
            editor.getSession().setValue(data);
        });
}

function load_source(file) {
    var reader = new FileReader();
    reader.onload = function (e) {
        editor.getSession().setValue(e.target.result);
    }
    reader.readAsText(file);
}

var editor = null;
var can_update = true;
$(window).resize(function () {
    onresize();
});
editor = ace.edit("input");
editor.getSession().setValue('');
editor.getSession().setTabSize(4);
editor.getSession().setUseSoftTabs(true);
document.getElementById('input').style.fontSize='14px';
editor.getSession().setUseWrapMode(true);
editor.setShowPrintMargin(true);
var mode = require("ace/mode/markdown").Mode;
editor.getSession().setMode(new mode());

$('body').bind('dragover', function () {
    return false;
}).bind('dragend', function () {
        return false;
    }).bind('drop', function (ev) {
        var md_file = ev.originalEvent.dataTransfer.files[0];
        load_source(md_file);
        return false;
    });

$('#import_file_button').hover(function () {
    $('#import_button').addClass('hover');
}, function () {
    $('#import_button').removeClass('hover');
    $('#import_button').removeClass('active');
}).mousedown(function () {
        $('#import_button').addClass('active');
    }).mouseup(function () {
        $('#import_button').removeClass('active');
    }).change(function () {
        load_source($(this).get(0).files[0]);
    });
$('#save').click(function(){update();});

$('#color_scheme > a').click(function () {
    $('#color_scheme > a').removeClass('selected');
    $(this).addClass('selected');
    change_theme($(this).attr('href'));
    return false;
})

$('#preview_pane').hover(function () {
    can_update = false;
}, function () {
    can_update = true;
});

update();
resume_state();
change_theme('dark');
onresize();

window.onunload = function () {
    update();
}
