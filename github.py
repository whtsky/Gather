#coding=utf-8
__author__ = 'whtsky'
from urllib import urlopen

def getrepos(username):
    '''return list of user's public repos.
    '''
    json = urlopen('https://api.github.com/users/whtsky/repos').read()