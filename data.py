import hashlib
import json
import os
import ssl
import string
import time
from urllib import request
from urllib.parse import quote

from django.http import HttpResponse
import sqlite3


def all_data(request):
    d = getNewestData()
    oldData = json.loads(d)
    data = []
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("SELECT data FROM Covid19Data ORDER BY id DESC LIMIT 1")
    for row in c:
        data.append(row[0])
    conn.close()
    diff = int(time.time()) - oldData['curtime']
    if diff > 15 * 60:
        res = fetchData()
    else:
        res = d
    return HttpResponse(res)


def getNewestData():
    data = []
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("SELECT data FROM Covid19Data ORDER BY id DESC LIMIT 1")
    for row in c:
        data.append(row[0])
    conn.close()
    if len(data) == 0:
        return None
    return data[0]


def getData(api_url: str, appid: str, secret: str):
    print("getData")
    data = {'appid': appid, 'format': 'json', 'time': round(time.time())}
    keysArr = list(data.keys())  # 取出字典key
    keysArr.sort()  # 对字典key进行排序
    md5String = ''
    params = []
    for key in keysArr:
        if data[key]:
            val = str(data[key])
            md5String += key + val
            params.append(key + "=" + val)
    md5String += secret
    m = hashlib.md5()
    b = md5String.encode(encoding='utf-8')
    m.update(b)
    sign = m.hexdigest()

    params.append('sign=' + sign)  # 加入计算后的sign值去请求
    params = '&'.join(tuple(params))  # 把列表转成元组后用&分隔，最终转换成字符串 a=b&c=d&e=f

    ssl._create_default_https_context = ssl._create_unverified_context
    url = api_url + '?' + params
    url = quote(url, safe=string.printable)
    req = request.Request(url)
    opener = request.build_opener()
    r = opener.open(fullurl=req)

    res = r.read().decode('utf-8')
    return res


def fetchData():
    api_url, appid, secret = getEnv()
    data = getNewestData()
    lastUpdateTime = ''
    if data is not None:
        lastUpdateTime = json.loads(data)['retdata']['lastUpdateTime']

    d = getData(api_url, appid, secret)
    newdata = json.loads(d)
    if newdata['codeid'] != 10000:
        print(newdata['message'])
        return data
    data = newdata
    conn = sqlite3.connect('db.sqlite3')
    if data['retdata']['lastUpdateTime'] != lastUpdateTime:
        sql = "INSERT INTO Covid19Data(timestamp,data) VALUES ('{0}', '{1}')".format(str(data['curtime']), d)
    else:
        sql = "UPDATE Covid19Data SET timestamp = '{0}' WHERE id = (select MAX(id) from Covid19Data)".format(str(int(time.time())))
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    return d


def getEnv():
    lackEnv = []
    # 在后台我的应用查看
    api_url = os.environ.get('api_url')
    if api_url is None:
        lackEnv.append('api_url')
    appid = os.environ.get('appid')
    if appid is None:
        lackEnv.append('appid')
    secret = os.environ.get('secret')
    if secret is None:
        lackEnv.append('secret')
    if len(lackEnv) > 0:
        raise EnvironmentError(
            "Couldn't get environment variable {0}. Get from https://www.wapi.cn/api_detail/94/219.html.".format(
                lackEnv)
        )
    return api_url, appid, secret
