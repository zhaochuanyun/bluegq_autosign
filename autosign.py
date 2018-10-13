#!/usr/bin/env/ python3
# -*-coding:utf-8-*-

import logging
from config import config
import recognize

logger = logging.getLogger('jobs')


def main():
    set_logger()
    # session = make_session()
    for bluegq in config.bluegqs:
        (session, loginhash, formhash, seccodehash, verifycode) = recognize.get_login_info()
        login(session, loginhash, formhash, seccodehash, verifycode, bluegq['username'], bluegq['password'])
        formhash = get_formhash(session)
        sign(session, formhash)
        score(session, bluegq['uid'])


def set_logger():
    logger.propagate = False
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(name)s[%(module)s] %(levelname)s: %(message)s')
    file_handler = logging.FileHandler('logger.log', encoding='utf-8')
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


# 登录
def login(session, loginhash, formhash, seccodehash, verifycode, username, password):
    url = 'http://www.bluegq.com/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=' + loginhash + '&inajax=1'
    data = {'formhash': formhash,
            'referer': 'http://www.bluegq.com/portal.php?mod=index',
            'loginfield': 'username',
            'username': username,
            'password': password,
            'questionid': '0',
            'answer': '',
            'seccodehash': seccodehash,
            'seccodemodid': 'member::logging',
            'seccodeverify': verifycode}
    headers = {'Host': 'www.bluegq.com', 'Connection': 'keep-alive', 'Content-Length': '233',
               'Cache-Control': 'no-cache', 'Origin': 'http://www.bluegq.com', 'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Referer': 'http://www.bluegq.com/member.php?mod=logging&action=login',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,ja;q=0.5'}
    session.headers.clear()
    session.headers.update(headers)
    r = session.post(url, data)
    p_start = r.text.find('欢迎您回来')
    p_endt = r.text.find('\';</script>')
    logger.info(u'登录信息: ' + r.text[p_start:p_endt])


# 获取formhash
def get_formhash(session):
    url = 'http://www.bluegq.com/forum.php'
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,ja;q=0.5',
               'Cache-Control': 'no-cache',
               'Connection': 'keep-alive',
               'Host': 'www.bluegq.com',
               'Pragma': 'no-cache',
               'Referer': 'http://www.bluegq.com/portal.php?mod=index',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    session.headers.clear()
    session.headers.update(headers)
    r = session.get(url)
    p = r.text.find('formhash=') + len('formhash=')
    return r.text[p:p + 8]


# 签到
def sign(session, formhash):
    url = 'http://www.bluegq.com/plugin.php?id=fx_checkin:checkin&formhash=' + formhash + '&infloat=yes&handlekey=fx_checkin&inajax=1&ajaxtarget=fwin_content_fx_checkin'
    headers = {'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,ja;q=0.5',
               'Cache-Control': 'no-cache',
               'Connection': 'keep-alive',
               'Host': 'www.bluegq.com',
               'Pragma': 'no-cache',
               'Referer': 'http://www.bluegq.com/forum.php',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest'}
    session.headers.clear()
    session.headers.update(headers)
    r = session.get(url)
    p_start = r.text.find('showDialog(\'') + len('showDialog(\'')
    p_end = r.text.find(', \'right\'') - 1
    logger.info('签到信息: ' + r.text[p_start:p_end])


# 查看积分
def score(session, uid):
    url = 'http://www.bluegq.com/home.php?mod=space&uid=' + uid
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,ja;q=0.5',
               'Cache-Control': 'no-cache',
               'Connection': 'keep-alive',
               'Host': 'www.bluegq.com',
               'Pragma': 'no-cache',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    session.headers.clear()
    session.headers.update(headers)
    r = session.get(url)
    p_start = r.text.find('<li><em>B币</em>') + len('<li><em>B币</em>')
    p_end = r.text.find('<li><em>蓝币</em>') - 7
    logger.info('当前B币: ' + r.text[p_start:p_end] + '\n')


if __name__ == '__main__':
    main()
