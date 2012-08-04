all: css js

css:
	sass assets/css/pbb.scss:static/css/style.css --style compressed

css-watch:
	sass --watch assets/css/pbb.scss:static/css/style.css --style compressed
	
js:
	uglifyjs -nc assets/js/jquery-1.7.2.min.js > static/js/lib.js
	uglifyjs -nc assets/js/bootstrap.min.js >> static/js/lib.js
	coffee -b -p assets/js/site.coffee | uglifyjs >> static/js/lib.js
	uglifyjs -nc assets/js/jquery.caret.js > static/js/editor.js
	uglifyjs -nc assets/js/jquery.atwho.js >> static/js/editor.js
	coffee -p assets/js/editor.coffee | uglifyjs >> static/js/editor.js