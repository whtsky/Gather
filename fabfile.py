from fabric.api import *

env.hosts = ['whtsky@ssh.whouz.com']


def update():
    with cd('~/PBB'):
        run('git pull origin master')
        run('./bin/pip install -r requirements.txt')
    local("~/Downloads/qiniu/qrsync ~/qiniu_PBB.json")
