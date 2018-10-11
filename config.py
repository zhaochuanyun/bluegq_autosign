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
        self.debug = False
        self.log_format = log_format
        self.ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:52.0) Gecko/20100101 Firefox/52.0'

        self.bluegq = {
            'username': '',
            'password': ''
        }

    @classmethod
    def load(cls, d):
        the_config = Config()

        the_config.debug = d.get('debug', False)

        try:
            the_config.bluegq = {
                'username': base64.b85decode(d['bluegq']['username']).decode(),
                'password': base64.b85decode(d['bluegq']['password']).decode()
            }
        except Exception as e:
            logging.error('获取帐号出错: ' + repr(e))

        if not (the_config.bluegq['username'] and the_config.bluegq['password']):
            logging.info('用户名/密码未找到.')

        return the_config


def load_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='config file name')
    args = parser.parse_args()

    config_name = args.config or 'config.json'
    logging.info('使用配置文件 "{}".'.format(config_name))

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
        config_dict = json.loads(config_file.read_text())
    except Exception as e:
        sys.exit('# 错误: 配置文件载入失败: {}'.format(e))

    the_config = Config.load(config_dict)

    return the_config


config = load_config()
# print(base64.b85encode(b'abc'))
