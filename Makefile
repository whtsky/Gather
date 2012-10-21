all: css js

css:
	sass assets/css/pbb.scss:static/css/style.css --style compressed

css-watch:
	sass --watch assets/css/pbb.scss:static/css/style.css --style compressed
	
js: js-lib js-editor js-locale

js-lib:
	uglifyjs -nc assets/js/jquery-1.7.2.min.js > static/js/lib.js
	uglifyjs -nc assets/js/bootstrap.min.js >> static/js/lib.js
	uglifyjs -nc assets/js/jquery.timeago.js >> static/js/lib.js
	coffee -b -p assets/js/site.coffee | uglifyjs >> static/js/lib.js
	coffee -p assets/js/retina.coffee | uglifyjs >> static/js/lib.js
	
js-editor:
	uglifyjs -nc assets/js/jquery.caret.js > static/js/editor.js
	uglifyjs -nc assets/js/jquery.atwho.js >> static/js/editor.js
	uglifyjs -nc assets/js/jquery.elastic.js >> static/js/editor.js
	coffee -p assets/js/editor.coffee | uglifyjs >> static/js/editor.js
	
js-locale:
	rm -rf static/js/locale
	mkdir static/js/locale
	uglifyjs -nc assets/js/locale/en_US.js > static/js/locale/en_US.js
	uglifyjs -nc assets/js/locale/zh_CN.js > static/js/locale/zh_CN.js
	uglifyjs -nc assets/js/locale/ja_JP.js > static/js/locale/ja_JP.js