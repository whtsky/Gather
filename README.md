#PBB

PBB is a simple forum.

##Install && Run
```bash
git clone git://github.com/whtsky/PBB.git
cd PBB
pip install -r requirements.txt
vim settings.py
```
You must rewrite `forum_title` and `forum_url` and set `cookie_secret` to a random string.
Then you can run `python add_superadmin.py` or `make superadmin` to init datebase and add a superadmin.
Finally,run`python main.py` and goto http://localhost:8888/


##Stylesheets
PBB uses [sass](http://sass-lang.com/) and [Bootstrap](http://twitter.github.com/bootstrap).
You need to install sass before change the stylesheets.
After changing,you need to run `make css` to generate css.