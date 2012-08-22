if window.devicePixelRatio is 2
	$ ->
		for avatar in $('.avatar img')
			url = avatar.src.split('=')
			size = parseInt(url[url.length-1])
			retina_size = size * 2
			url[url.length-1] = retina_size.toString()
			retina_url = url.join('=')
			avatar.src = retina_url
