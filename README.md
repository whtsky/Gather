#PBB

PBB is a simple forum.

##Install && Run
```bash
git clone git://github.com/whtsky/PBB.git
cd PBB
pip install -r requirements.txt
vim settings.py
```

You must rewrite `forum_title` and `forum_url`.

`cookie_secret` must be a random string.

Then,run`python main.py` and goto http://localhost:8888/.The first member will be superadmin.


##Stylesheets
PBB uses [sass](http://sass-lang.com/) and [Bootstrap](http://twitter.github.com/bootstrap).

You need to install sass before changing the stylesheets.

You can run `make css-watch` to watch and generate css automatically or run `make css` to generate css manually after changing.

##Scripts
PBB uses [coffeescript](http://jashkenas.github.com/coffee-script/) to write scripts and [UglifyJS](https://github.com/mishoo/UglifyJS/) to compress scripts.
You need to install them before changing the scripts.

You can run `make js` to generate js.

##Thanks
+ [PyCharm](http://www.jetbrains.com/pycharm/)