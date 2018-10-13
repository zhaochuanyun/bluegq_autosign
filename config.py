# -*- coding: utf-8 -*-

import argparse
import json
import logging
import sys
import base64
from pathlib import Path

log_format = '%(asctime)s %(name)s[%(module)s] %(levelname)s: %(message)s'
logging.basicConfig(format=log_format, level=logging.INFO)


class Config:
    def __init__(self):
        self.log_format = log_format
        self.bluegqs = []

    @classmethod
    def load(cls, list):
        the_config = Config()

        configs = []

        try:
            for blue in list:
                dict = {
                    'username': base64.b85decode(blue['bluegq']['username']).decode(),
                    'password': base64.b85decode(blue['bluegq']['password']).decode(),
                    'uid': blue['bluegq']['uid']
                }
                configs.append(dict)
            the_config.bluegqs = configs
        except Exception as e:
            logging.error('获取帐号出错: ' + repr(e))

        if len(configs) == 0:
            logging.info('用户名/密码未找到.')

        return the_config


def load_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='config file name')
    args = parser.parse_args()

    config_name = args.config or 'config.json'
    logging.debug('使用配置文件 "{}".'.format(config_name))

    config_file = Path(__file__).parent.joinpath('conf/', config_name)

    if not config_file.exists():
        config_name = 'config.default.json'
        logging.warning('配置文件不存在, 使用默认配置文件 "{}".'.format(config_name))
        config_file = config_file.parent.joinpath(config_name)

    try:
        # 略坑, Path.resolve() 在 3.5 和 3.6 上表现不一致... 若文件不存在 3.5 直接抛异常, 而 3.6
        # 只有 Path.resolve(strict=True) 才抛, 但 strict 默认为 False.
        # 感觉 3.6 的更合理些...
        config_file = config_file.resolve()
        config_list = json.loads(config_file.read_text())
    except Exception as e:
        sys.exit('# 错误: 配置文件载入失败: {}'.format(e))

    return Config.load(config_list)


config = load_config()
# print(base64.b85encode(b'abc'))
