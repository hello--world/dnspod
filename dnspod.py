#!/usr/bin/env python2
#-*- coding:utf-8 –*-
import httplib
import urllib
import socket
import time
import json

import conf

# Use Token, check https://support.dnspod.cn/Kb/showarticle/tsid/227/
ID = conf.ID
Token = conf.Token
# 新APIdomain_id和domain传其一就行
Domain = conf.Domain

needlisten = conf.needlisten

publicparams = dict(
    login_token=("%s,%s" % (ID, Token)),
    format="json",
    lang = 'cn',
)

def createconn(url,par):
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json", "User-Agent": "dnspod-batch/0.01 (hellohfy@gmail.com)"}
    conn = httplib.HTTPSConnection("dnsapi.cn")
    conn.request("POST", url, urllib.urlencode(par), headers)

    return conn

def modify(recordid,ip):
    conf.logger.info('修改：ID:%s, IP:%s' ,str(recordid)  , str(ip))
    print '修改', recordid
    mydic = publicparams.copy()
    mydic.update(dict(record_id=recordid))
    mydic.update(dict(change='value'))
    mydic.update(dict(change_to=ip))
    print mydic

    conn = createconn('/Batch.Record.Modify', mydic)

    response = conn.getresponse()
    print response.status, response.reason
    data = response.read()
    conf.logger.info('datastring:' + data)

    print data
    # logger.info(data)
    conn.close()
    return response.status == 200

# 获取需要修过的Id
def records():
    publicparams.update(dict(domain=Domain))
    conn = createconn("/Record.List", publicparams)
    response = conn.getresponse()

    print response.status, response.reason, records.__name__

    dataString = response.read()
    dataDict = json.loads(dataString)
    recordlist = list(dataDict['records'])
    recordids = ''
    ip = recordlist[0]['value']

    for record in recordlist:
        if record['type'] == 'A':
            if record['name'] in needlisten:
                recordids = recordids + record['id'] + ','

    conn.close()
    print recordids, ip
    return recordids, ip

def getip():
    sock = socket.create_connection(('ns1.dnspod.net', 6666), 20)
    ip = sock.recv(16)
    sock.close()
    return ip

if __name__ == '__main__':
    conf.logger.info('开始运行')
    record_ids, current_ip = records()
    while True:
        try:
            public_ip = getip()
            if current_ip != public_ip:
                if modify(record_ids, public_ip):
                    current_ip = public_ip
                    conf.logger.info('修改成' + public_ip)
                    print '修改成功'
            print public_ip
        except Exception as e:
            # logger.error(e)
            print e
            pass
        time.sleep(conf.sleeptime)
