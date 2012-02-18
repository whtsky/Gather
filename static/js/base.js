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