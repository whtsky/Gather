superadmin:
	python add_superadmin.py

css:
	sass assets/css/pbb.scss:static/css/style.css --style compressed

css-watch:
	sass --watch assets/css/pbb.scss:static/css/style.css --style compressed