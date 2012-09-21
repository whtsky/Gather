search = ->
	txt = $('.search-query').val()
	if not txt
		return false
	window.open "https://www.google.com/search?q=site:#{domain} #{txt}"
	$('.search-query').val('')
	return false
	
window._ = (msg) ->
	i18n = window.i18n || {}
	if msg in i18n
		return i18n[msg]
	return msg
	
$ ->
	$('time').timeago()
	$('.dangerous').click ->
		if window.confirm(_('Are you sure?'))
			window.location = $(this).data('href')
		return false
		