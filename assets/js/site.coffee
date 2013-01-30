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
	
$ ->
	$('time').timeago()
	$('.dangerous').click ->
		if window.confirm(_('Are you sure?'))
			window.location = $(this).data('href')
		return false

	$.ajax
        url: "/api/notifications/new"
        success: (data) ->
            window.data = data
            for notification in data.notifications
                $.notifier.notify(notification.avatar, notification.title,
                    notification.content, notification.url)
            return
