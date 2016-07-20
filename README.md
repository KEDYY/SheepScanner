# SheepScanner
分布式互联网开放端口与协议扫描

-----

支持分布式的互联网主机扫描</br>
基于Celery 分布式框架，MongoDB作为存储和任务分发</br>
如果使用 redis 作为任务分发需要额外安装 redis服务器和redis模块
python-Nmap 作为 主机扫描核心程序</br>

------
## 安装
下载并安装 mongodb $`wget https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-3.2.7.tgz`
如果是ubuntu可以执行 $`sudo apt-get install mongodb`
下载并安装 nmap @[see](https://nmap.org/download.html)
如果是ubuntu可以执行 `sudo apt-get install nmap`

## 管理
通过Flask编写的json API交换任务
 
# 依赖程序
Python 2.7.x
MongoDB 3.1.x
Nmap 6.4.x
$`sudo pip install -r requirements.txt`


