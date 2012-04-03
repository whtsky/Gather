cp -f lib.js ../../static/js
uglifyjs -nc base.js >> ../../static/js/lib.js

cp -f editor.js ../../static/js
uglifyjs -nc markdown.js >> ../../static/js/editor.js

uglifyjs -nc authsetting.js > ../../static/js/authsetting.js
uglifyjs -nc signup.js > ../../static/js/signup.js
uglifyjs -nc login.js > ../../static/js/login.js

