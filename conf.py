#!/usr/bin/env python2
#-*- coding:utf-8 –*-

import logging
import logging.handlers

ID = 'xxxx'
Token = 'xxxxxxxxxxxxxxxxxxxx'
# 新API中domain_id和domain传其一就行
Domain = 'xxxx.xxxx'
needlisten = ['@', 'git', 'test', 'hh']

sleeptime = 300

LOG_FILE = 'dnspod.log'

handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5) # 实例化handler
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'

formatter = logging.Formatter(fmt)   # 实例化formatter
handler.setFormatter(formatter)      # 为handler添加formatter

logger = logging.getLogger('dnspod')    # 获取名为dnspod的logger
logger.addHandler(handler)           # 为logger添加handler
logger.setLevel(logging.DEBUG)