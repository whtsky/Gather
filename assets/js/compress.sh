for i in *.js
do
    echo "Compressing $i"
    uglifyjs -nc $i > ../../static/js/$i
done

cd ../../static/js

cat base.js >> lib.js
cat markdown.js >> editor.js

rm base.js markdown.js
