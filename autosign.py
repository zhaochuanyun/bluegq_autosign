# -*- coding: utf-8 -*-

import logging
from config import config
import recognize

logger = logging.getLogger('jobs')


def main():
    set_logger()
    # session = make_session()
    (session, loginhash, formhash, seccodehash, verifycode) = recognize.get_login_info()
    login(session, loginhash, formhash, seccodehash, verifycode, config.bluegq['username'], config.bluegq['password'])
    sign(session, formhash)


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
    logger.info('登录信息: ' + r.text[p_start:p_endt] + '\n')


# 签到
def sign(session, formhash):
    url = 'http://www.bluegq.com/plugin.php?id=fx_checkin:checkin'
    data = {'formhash': formhash + '&' + formhash,
            'infloat': 'yes',
            'handlekey': 'fx_checkin',
            'inajax': '1',
            'ajaxtarget': 'fwin_content_fx_checkin'
            }
    headers = {'Host': 'www.bluegq.com', 'Connection': 'keep-alive', 'Content-Length': '233',
               'Cache-Control': 'no-cache',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Accept': '*/*',
               'Referer': 'http://www.bluegq.com/forum.php',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,ja;q=0.5'}
    session.headers.clear()
    session.headers.update(headers)
    r = session.post(url, data)
    logger.info('签到信息: ' + r.text)


if __name__ == '__main__':
    main()
