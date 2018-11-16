#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-

import os
import recognize
import time
import uuid


def download():
    folder = '/img/'
    ab_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + ".") + folder
    orig_name = ab_path + 'code.png'

    (session, loginhash, formhash, seccodehash) = recognize.get_login_hash()

    while True:
        recognize.get_verifycode(session, recognize.get_update_code(session, seccodehash), seccodehash, folder=folder)
        time.sleep(0.1)
        code = recognize.recognize_code(folder=folder)
        if (recognize.check_verifycode(session, loginhash, seccodehash, code)):
            print('识别成功: %s' % (code))
            re_name = ab_path + code + '.png'
            if os.path.isfile(re_name):
                os.rename(orig_name, ab_path + code + '-' + str(uuid.uuid1()) + '.png')
            else:
                os.rename(orig_name, re_name)
            print('总文件数: %d' % (len(os.listdir(ab_path))))
        else:
            print('识别失败')


if __name__ == '__main__':
    download()
