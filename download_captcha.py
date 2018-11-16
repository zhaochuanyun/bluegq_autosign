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
        try:
            os.remove(orig_name)
        except OSError:
            pass

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
            print('%s 总文件数: %d' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), len(os.listdir(ab_path))))


if __name__ == '__main__':
    download()
