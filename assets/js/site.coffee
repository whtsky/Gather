search = ->
    txt = $('.search-query').val()
    if not txt
        return false
    window.open "https://www.google.com/search?q=site:#{domain} #{txt}"
    $('.search-query').val('')
    return false

_ = (msg) ->
    return i18n[msg] if i18n?[msg]?
    return msg

window.notify = () ->
    setTimeout(window.notify, 20000)
    $.ajax
        url: "/api/notifications/new"
        success: (data) ->
            if not data.id?
                return
            last_id = window.localStorage.getItem('last_notify')
            window.localStorage.setItem('last_notify', data.id)
            for notification in data.notifications
                if notification.id == last_id
                    return
                $.notifier.notify(notification.avatar, notification.title,
                notification.content, notification.url)
            return


$ ->
    notify()
    $('time').timeago()
    $('.dangerous').click ->
        if window.confirm(_('Are you sure?'))
            window.location = $(this).data('href')
        return false
