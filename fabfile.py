from fabric.api import *

env.hosts = ['whtsky@ssh.whouz.com']


def update():
    with cd('~/PBB'):
        run('git pull')
        run('./bin/pip install -r requirements.txt')
