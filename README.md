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

`cookie_secret` must to be a random string.

Then run `python add_superadmin.py` or `make superadmin` to init datebase and add a superadmin.

Finally,run`python main.py` and goto http://localhost:8888/


##Stylesheets
PBB uses [sass](http://sass-lang.com/) and [Bootstrap](http://twitter.github.com/bootstrap).

You need to install sass before change the stylesheets.

You can run `make css-watch` to watch and generate css automatically or run `make css` to generate css manually after changing.