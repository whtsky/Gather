$.ajaxSetup({
    beforeSend: function(jqXHR, settings) {
        type = settings.type
        if (type != 'GET' && type != 'HEAD' && type != 'OPTIONS') {
            var pattern = /(.+; *)?_xsrf *= *([^;" ]+)/;
            var xsrf = pattern.exec(document.cookie);
            if (xsrf) {
                jqXHR.setRequestHeader('X-Xsrftoken', xsrf[2]);
            }
        }
}}); 