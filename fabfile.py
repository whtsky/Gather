from fabric.api import *

env.hosts = ['whtsky@pbb.whouz.com']


def update():
    with cd('~/PBB'):
        run('git pull origin master')
        run('./bin/pip install -r requirements.txt')

