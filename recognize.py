#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import pytesseract
import requests
import os


def get_login_info():
    (session, loginhash, formhash, seccodehash) = get_login_hash()
    get_verifycode(session, get_update_code(session, seccodehash), seccodehash)
    verifycode = recognize_code()
    while not check_verifycode(session, loginhash, seccodehash, verifycode):
        (session, loginhash, formhash, seccodehash) = get_login_hash()
        get_verifycode(session, get_update_code(session, seccodehash), seccodehash)
        verifycode = recognize_code()
    return session, loginhash, formhash, seccodehash, verifycode


# 进入登录界面获取loginhash、formhash和seccodehash
def get_login_hash():
    url = 'http://www.bluegq.com/member.php?mod=logging&action=login'
    headers = {'Host': 'www.bluegq.com', 'Connection': 'keep-alive',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest', 'Accept': '*/*', 'Referer': 'www.bluegq.com/member.php',
               'Accept-Encoding': 'gzip, deflate, sdch', 'Accept-Language': 'zh-CN,zh;q=0.8'}
    # 清空原来的headers
    session = requests.session()
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
    return (session, loginhash, formhash, seccodehash)


# 获取update
def get_update_code(session, idhash):
    url = 'http://www.bluegq.com/misc.php?mod=seccode&action=update&idhash=' + idhash + '&modid=member::logging'
    r = session.get(url)
    p = r.text.find('update=') + len('update=')
    update = r.text[p:p + 5]
    return update


# 获取验证码
def get_verifycode(session, update, seccodehash, name='code.png'):
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
def check_verifycode(session, loginhash, seccodehash, code):
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
    p = r.text.find('succeed')
    if p == -1:
        return False
    else:
        return True


def recognize_code():
    try:
        img = Image.open('data/code.png')
    except OSError:
        os.remove('data/code.png')
        return 'abcd'

    img_width, img_height = img.size
    img = img.convert('L')

    array = np.array(img)
    threshold = np.mean(array, axis=0)

    for w in range(img_width):
        for h in range(img_height):
            if array[h, w] >= threshold[w]:
                array[h, w] = 255
            else:
                array[h, w] = 0

    img = Image.fromarray(array).convert('')
    # plt.imshow(img)
    # plt.show()

    # img.save('data/code_l.png')

    return pytesseract.image_to_string(img).lower()
