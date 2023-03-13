# Covid19-Charts

## 简介

仿~[百度新型冠状病毒肺炎疫情实时大数据报告](https://voice.baidu.com/act/newpneumonia/newpneumonia/)~此网站已关停

应用Demo：~[Demo](http://101.42.106.83:8000/index/)~Demo已停止展示

## 实现框架

服务端：Django

网页端：jQuery+Echarts

数据库：Sqlite3

## 数据来源

[全球新冠疫情数据-新型肺炎疫情数据-API接口-挖数据](https://www.wapi.cn/api_detail/94/222.html)

## 实现逻辑

整体逻辑：服务端启动==>浏览器访问服务端端口获取网页端静态文件==>网页端访问服务器获取疫情数据==>网页端使用Echarts渲染实现可视化。

后端逻辑：服务端启动==>当网页端访问服务器获取疫情数据时，检查数据库数据时间戳，若数据为15分钟前的数据，调用API获取最新疫情数据入库并返回给网页端；若数据为15分钟内的数据，直接返回给网页端。

前端逻辑：jQuery+Echarts处理JSON格式的疫情数据。

数据库逻辑：数据库拥有表`Covid19Data`，格式为<id,timestamp,data>。其中id为自增主键、timestamp为时间戳、data为疫情数据，是从API接口获取的全部疫情信息，为JSON字符串。

## 使用

本程序要求4个环境变量，其中3个为必填。

| 环境变量      | 必填 | 类型   | 说明                                                         | 示例                                     |
| ------------- | ---- | ------ | ------------------------------------------------------------ | ---------------------------------------- |
| api_url       | 是   | String | API请求所需的URL地址                                         | https://grnx.api.storeapi.net/api/94/222 |
| appid         | 是   | String | 应用ID，在API后台[我的应用](https://www.wapi.cn/member/my_apply)查看或者添加 | 12345                                    |
| secret        | 是   | String | 密钥，在API后台[我的应用](https://www.wapi.cn/member/my_apply)查看或者添加 | a971da6d6bdf1e3678c3d60f9c1c0145         |
| ALLOWED_HOSTS | 否   | String | Django的Allowed_hosts，默认为['0.0.0.0']                     | ['0.0.0.0','127.0.0.1']                  |

声明好环境变量后，在项目根目录下执行命令即可启动：

```
python3 manage.py runserver 0.0.0.0:8000
```

## Use in docker

[fuming/covid-data - DockerHub](https://hub.docker.com/r/fuming/covid-data)
