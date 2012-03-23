#coding=utf-8

import xmlrpclib

ping_urls=['http://ping.baidu.com/ping/RPC2','http://blogsearch.google.com/ping/RPC2']

def ping(webname,hosturl,linkurl):
    for url in ping_urls:
        rpc_server = xmlrpclib.ServerProxy(url)
        rpc_server.weblogUpdates.extendedPing(webname,hosturl,linkurl)
