# bluegq_autosign
blue高清公馆自动登录签到，自动获取B币

`注意crontab的环境变量跟用户环境不一致，所以需要在shell脚本另外配置环境变量！`

crontab -e  
*/1 * * * * sh /../run.sh >> /../logger.log 2>&1