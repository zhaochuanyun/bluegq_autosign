#!/bin/sh
# 注意crontab的环境变量跟用户环境不一致，所以需要在shell脚本另外配置环境变量！
source /Users/mvpzhao/.bash_profile
export LANG=en_US.UTF-8
python /Users/mvpzhao/Tools/python-workspace/bluegq_autosign/autosign.py