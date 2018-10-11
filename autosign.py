# -*- coding: utf-8 -*-

import pickle
from pathlib import Path
import requests
import logging
from config import config

session = requests.session()
logger = logging.getLogger('jobs')


def main():
    set_logger()
    # session = make_session()
    (loginhash, formhash, seccodehash) = get_login_code()
    get_verifycode(get_code_info(), seccodehash)
    verifycode = input('# 请输入验证码> ')
    check_verifycode(loginhash, seccodehash, verifycode)  # 成功返回<root><![CDATA[succeed]]></root>
    login(loginhash, formhash, seccodehash, verifycode, config.bluegq['username'],
          config.bluegq['password'])  # 欢迎您回来，现在将转入登录前页面
    sign(formhash)


def set_logger():
    logger.propagate = False
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(name)s[%(module)s] %(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def download_verifycode():
    for index in range(200):
        print('%d.gif' % (index))
        (loginhash, formhash, seccodehash) = get_login_code()
        get_verifycode(get_code_info(), seccodehash, '%d.gif' % (index))


def make_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    })
    data_file = Path(__file__).parent.joinpath('data/cookies')
    if data_file.exists():
        try:
            bytes = data_file.read_bytes()
            cookies = pickle.loads(bytes)
            session.cookies = cookies
            logger.info('# 从文件加载 cookies 成功.')
        except Exception as e:
            logger.info('# 未能成功载入 cookies, 从头开始~')

    url = 'http://www.bluegq.com/member.php?mod=logging&action=login'
    headers = {'Host': 'www.bluegq.com', 'Connection': 'keep-alive',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest', 'Accept': '*/*', 'Referer': 'www.bluegq.com/member.php',
               'Accept-Encoding': 'gzip, deflate, sdch', 'Accept-Language': 'zh-CN,zh;q=0.8'}

    session.headers.clear()
    session.headers.update(headers)
    r = session.get(url)
    p = r.text.find('欢迎您回来')
    if p == -1:
        logger.info('# cookies已失效，重新登录')
        session = None
    else:
        logger.info('# cookies有效，登录成功')

    return session


def save_session(session):
    data = pickle.dumps(session.cookies)
    data_dir = Path(__file__).parent.joinpath('data/')
    data_dir.mkdir(exist_ok=True)
    data_file = data_dir.joinpath('cookies')
    data_file.write_bytes(data)


def sign(formhash):
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
    save_session(session)
    logger.info('# 签到信息:\n ' + r.text + '\n')


# 获取登录窗口中的loginhash、formhash和seccodehash
def get_login_code():
    url = 'http://www.bluegq.com/member.php?mod=logging&action=login'
    headers = {'Host': 'www.bluegq.com', 'Connection': 'keep-alive',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest', 'Accept': '*/*', 'Referer': 'www.bluegq.com/member.php',
               'Accept-Encoding': 'gzip, deflate, sdch', 'Accept-Language': 'zh-CN,zh;q=0.8'}
    # 清空原来的headers
    session.headers.clear()
    # 更新headers
    session.headers.update(headers)
    r = session.get(url)
    # 获取loginhash
    p = r.text.find('loginhash=') + len('loginhash=')
    loginhash = r.text[p:p + 5]
    # 获取formhash
    p = r.text.find('formhash') + len('formhash" value="')
    formhash = r.text[p:p + 8]
    # 获取seccodehash
    p = r.text.find('seccode_') + len('seccode_')
    seccodehash = r.text[p:p + 8]
    return (loginhash, formhash, seccodehash)


# 获取update
def get_code_info():
    url = 'http://www.bluegq.com/misc.php?mod=seccode&action=update&idhash=cSssB2dv&0.04821189811991089&modid=member::logging'
    r = session.get(url)
    p = r.text.find('update=') + len('update=')
    update = r.text[p:p + 5]
    return update


# 获取验证码
def get_verifycode(update, seccodehash, name='code.gif'):
    url = 'http://www.bluegq.com/misc.php?mod=seccode&update=' + update + '&idhash=' + seccodehash
    headers = {'Host': 'www.bluegq.com', 'Connection': 'keep-alive',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
               'Accept': 'image/webp,image/*,*/*;q=0.8',
               'Referer': 'http://www.bluegq.com/member.php?mod=logging&action=login',
               'Accept-Encoding': 'gzip, deflate, sdch',
               'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,ja;q=0.5'}
    session.headers.clear()
    session.headers.update(headers)
    r = session.get(url)
    # 保存验证码图片
    file = open('data/' + name, 'wb')
    file.write(r.content)
    file.close()


# 检查验证码是否正确
# 通过人工识别验证码code，:)
def check_verifycode(loginhash, seccodehash, code):
    url = 'http://www.bluegq.com/misc.php?mod=seccode&action=check&inajax=1&modid=member::logging&idhash=' + seccodehash + '&secverify=' + code
    headers = {'Host': 'www.bluegq.com', 'Connection': 'keep-alive',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
               'Accept': '*/*',
               'Referer': 'http://www.bluegq.com/member.php?mod=logging&action=login',
               'Accept-Encoding': 'gzip, deflate, sdch',
               'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,ja;q=0.5'}
    session.headers.clear()
    session.headers.update(headers)
    r = session.get(url)
    logger.info('# 验证码校验信息:\n ' + r.text + '\n')
    return r.text


# 模拟登录
def login(loginhash, formhash, seccodehash, verifycode, username, password):
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
    save_session(session)
    logger.info('# 登录信息:\n ' + r.text + '\n')


if __name__ == '__main__':
    main()
