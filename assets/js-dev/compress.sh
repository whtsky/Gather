mkdir ../../static/js
mkdir ../../static/js/languages
for i in *.js
do
    echo "Compressing $i"
    uglifyjs -nc $i > ../../static/js/$i
done

cd languages
for i in *.js
do
    echo "Compressing $i"
    uglifyjs -nc $i > ../../../static/js/languages/$i
done