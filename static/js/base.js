readySubmit=false;

function checkInput(id,bool)
{
    if(bool)
    {
        readySubmit=false;
        $(id+"-g").addClass("error");
    }
    else
    {
        $(id+"-g").removeClass("error");
    }
}
function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

var args = {};
var query = location.search.substring(1);
// Get query string
var pairs = query.split("&");
// Break at ampersand
for(var i = 0; i < pairs.length; i++) {
    var pos = pairs[i].indexOf('=');
    // Look for "name=value"
    if (pos == -1) continue;
    // If not found, skip
    var argname = pairs[i].substring(0,pos);// Extract the name
    var value = pairs[i].substring(pos+1);// Extract the value
    value = decodeURIComponent(value);// Decode it, if needed
    args[argname] = value;
    // Store as a property
}
var sUrl = document.URL;
var domain = sUrl.slice(sUrl.indexOf('://')+3, sUrl.indexOf('/', sUrl.indexOf('://')+3));

$(document).ready(function(){
    $('#search_form').submit(function(e){
        e.preventDefault();
        search();
    });

    function search(){
        var q = document.getElementById('q');
        if (q.value != '')
            window.open('http://www.google.com/search?q=site:' + domain + ' ' + q.value, '_blank');
        return false;
    }

});

function adjustOffset(el, offset) {
    /* From http://stackoverflow.com/a/8928945/611741 */
    var val = el.value, newOffset = offset;
    if (val.indexOf("\r\n") > -1) {
        var matches = val.replace(/\r\n/g, "\n").slice(0, offset).match(/\n/g);
        newOffset += matches ? matches.length : 0;
    }
    return newOffset;
}

$.fn.setCursorPosition = function(position){
    /* From http://stackoverflow.com/a/7180862/611741 */
    if(this.lengh == 0) return this;
    return $(this).setSelection(position, position);
}

$.fn.setSelection = function(selectionStart, selectionEnd) {
    /* From http://stackoverflow.com/a/7180862/611741
     modified to fit http://stackoverflow.com/a/8928945/611741 */
    if(this.lengh == 0) return this;
    input = this[0];

    if (input.createTextRange) {
        var range = input.createTextRange();
        range.collapse(true);
        range.moveEnd('character', selectionEnd);
        range.moveStart('character', selectionStart);
        range.select();
    } else if (input.setSelectionRange) {
        input.focus();
        selectionStart = adjustOffset(input, selectionStart);
        selectionEnd = adjustOffset(input, selectionEnd);
        input.setSelectionRange(selectionStart, selectionEnd);
    }

    return this;
}

$.fn.focusEnd = function(){
    /* From http://stackoverflow.com/a/7180862/611741 */
    this.setCursorPosition(this.val().length);
}

var isChrome = navigator.userAgent.indexOf("Chrome") !== -1

$(document).ready(function(){
    $(".item-list a").attr('target','_blank');
    if (isadmin){
        $('.kill').removeClass('hide');
        $('#changetag-link').removeClass('hide');
    }
    $('.kill').click(
        function(){
            if (confirm("真的要和谐么"))
                $.get($(this).attr('href')).success(function(){location.reload();}).error(function() { alert("和谐中出现错误，重试一下呗？"); });
            return false;
        }
    );
});