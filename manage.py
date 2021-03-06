# -*- coding: utf-8 -*-
# @Description: description

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import itchat
import logging
import requests
from itchat.content import *


def tuling(text, user):
    data = {
        'key': 'a5dda1dcd346464090f6195eee757b4c',
        'info': text,
        'userid': user.lstrip('@')[:32],
    }
    logging.error(data)
    received = requests.post('http://www.tuling123.com/openapi/api', data=data).json()
    return received.get('text')


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    itchat.send(tuling(msg['Text'], msg['FromUserName']), msg['FromUserName'])


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg['Text'](msg['FileName'])
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])


@itchat.msg_register(FRIENDS)
def add_friend(msg):
    itchat.add_friend(**msg['Text'])  # 该操作会自动将新好友的消息录入，不需要重载通讯录
    itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])


@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    logging.error(msg)
    if msg['isAt']:
        if u'老闷儿' in msg['Text']:
            itchat.send(u'老闷儿小胖墩', msg['FromUserName'])
        if u'高阳' in msg['Text']:
            itchat.send(u'高阳大和尚', msg['FromUserName'])
        else:
            rep = tuling(msg['Text'].strip('@Router'), msg['FromUserName'])
            itchat.send(rep, msg['FromUserName'])

itchat.auto_login(hotReload=True, enableCmdQR=2)
itchat.run()
