import os

from fabric.api import *

base_path = os.path.dirname(__file__)
project_root = "~/Gather"
pip_path = os.path.join(project_root, "bin/pip")
python_path = os.path.join(project_root, "bin/python")


env.user = "gather"
env.hosts = ["gather.whouz.com"]


def update_from_github():
    with cd(project_root):
        run("git pull")


def update_pip_requirements():
    with cd(project_root):
        run("%s install -r requirements.txt" % pip_path)


def migrate_databases():
    with cd(project_root):
        run("%s manage.py db upgrade" % python_path)
        run("%s manage.py create_all" % python_path)


def reload_nginx():
    _current_user = env.user
    env.user = 'root'
    run("/etc/init.d/nginx reload")
    env.user = _current_user


def restart_gunicorn():
    _current_user = env.user
    env.user = 'root'
    run("supervisorctl reload")
    env.user = _current_user


def reload_gunicorn():
    run("kill -HUP `cat /tmp/gather.pid`")


def clear_cache():
    with cd(project_root):
        run("%s manage.py clear_cache" % python_path)


def update():
    update_from_github()
    migrate_databases()
    reload_gunicorn()


def fullyupdate():
    update_from_github()
    update_pip_requirements()
    migrate_databases()
    reload_nginx()
    reload_gunicorn()
    clear_cache()
