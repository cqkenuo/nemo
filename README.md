# Nemo

<img src="docs/nemo.png" alt="nemo" align="left" style="zoom:20%;" />

Nemo（尼莫）是《海底总动员》中的一只可爱的小丑鱼。

Nemo是用来进行信息收集的一个自动化平台，实现对内网及互联网资产信息的自动收集。



## 功能

主要实现了以下功能（代码目前在完善和优化中...）：

- 采用Nmap进行端口扫描
- 端口标题查询（后期将实现全面的指纹收集）
- 通过第三方接口查询IP归属地
- 调用Sublist3r实现子域名收集
- 调用Fofa的API接口对IP和域名信息收集（需要购买Fofa的KEY）



## 实现

- **python3** 

  ```bash 
  pip install -r requirements.txt
  ```

- **web**

Flask + gevent

后台模板：vali-admin

- **数据库**

mysql

数据库连接：DBUtils + pymysql

- **异步多任务**

celery + rabbitmq + flower



## 运行

1. 启动mysql和rabbitmq

2. 启动celery worker

   ```bash
   export PYTHONOPTIMIZE=1
   celery -A nemo.core.tasks.tasks worker --loglevel info
   ```

3. 启动celery flower

   ```bash
   celery flower -A nemo.core.tasks.tasks --address=127.0.0.1 -port-5555
   ```

4. 启动app

   ```
   python3 app.py
   ```



## 目标

最终做成像FOFA一样的信息收集平台。



## 参考

jeffzh3ng：https://github.com/jeffzh3ng/fuxi

TideSec：https://github.com/TideSec/Mars