## 资产收集系统设计
## 功能设计

### 一、资产管理

#### 1、IP资产：

- masscan、nmap主动探测
- fofa、shodan等接口进行被动收集

#### 2、域名资产

- 子域名收集
- 子域名对应的IP资产

#### 3、指纹识别（菜单成功集成在资产收集中）

- nmap
- whatweb
- 第三方在线

### 二、任务管理

#### 1、新建任务

#### 2、当前任务

### 三、插件管理

#### 1、资产收集类插件

### 四、配置管理

#### 1、参数设置



## 技术路线

#### 一、python3 

#### 二、web：

Flask + gevent

vali-admin后台模板

#### 三、数据库

mysql

数据库连接：DBUtils + pymysql

#### 四、异步多任务

celery + rabbitmq

#### 五、指纹
采用标签（tag）存放资产的各种属性
对资产关键属性生成hash来保存历史变更信息

## 下一步功能：

#### 一、漏洞验证

#### 二、漏洞管理



## 终极目标

实现fofa功能的资产管理和漏洞验证



