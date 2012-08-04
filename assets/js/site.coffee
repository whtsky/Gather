search = ->
	txt = $('.search-query').val()
	if not txt
		return false
	window.open "https://www.google.com/search?q=site:#{domain} #{txt}"
	$('.search-query').val('')
	return false
	
$ ->
	$('.dangerous').click ->
		if window.confirm('Are you sure?')
			window.location = $(this).data('href')
		return false
		