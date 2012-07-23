superadmin:
	python add_superadmin.py

css:
	sass assets/css/pbb.scss:static/css/style.css --style compressed

css-watch:
	sass --watch assets/css/pbb.scss:static/css/style.css --style compressed
	
js:
	uglifyjs -nc assets/js/jquery-1.7.2.min.js > static/js/script.js
	uglifyjs -nc assets/js/bootstrap.min.js >> static/js/script.js