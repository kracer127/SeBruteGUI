# -*- coding:utf-8 -*-
# Date: 2021-11-14
# Author:kracer
# Version: 1.0


import base64
import json
import ctypes
import inspect
import os, time
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



""" 变量部分 """
successList = []
captcha = []
proxy = []
chromePath = []
threadStopFlag = False


if os.path.exists("config.json"):
    with open('config.json', 'r') as f:
        data = json.loads(f.read())
        captcha += data['captcha']
        proxy += data['proxy']
        chromePath += data["chromePath"]


def processUrl(url0):
    """ 对url的预处理 """
    if 'http' not in url0:
        url = 'http://'+url0
    else:
        url = url0
    return url


def getFileDatas(filepath):
    """ 从文件中读取数据 """
    dataList = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            datas = f.readlines()
            for i in datas:
                dataList.append(i.strip())
            return dataList
    except Exception as e:
        return []


def isManyAlive(result, ipList):
    """ 检测是否ip存活 """
    isAlivePool = ThreadPoolExecutor(max_workers=50, thread_name_prefix="browser")
    ipQueue = Queue()
    sumIp = len(ipList)
    for u in ipList:
        ipQueue.put_nowait(u)
    """ 输出 """
    msg ='[+] IP存活检测，ALL: {0} | Thread: 50 | Schedule: 1min......'.format(sumIp)
    result.insert("end", str(msg)+'\n')
    """ 通过request请求的反应来判断ip是否存活 """
    def request(url):
        try:
            res = requests.get(url=url, timeout=10, allow_redirects=True, verify=False)
        except Exception as e:
            ipList.remove(url)
    """ 多线程判断ip存活情况 """
    while not ipQueue.empty():
        url = ipQueue.get_nowait()
        isAlivePool.submit(request, url)
    isAlivePool.shutdown(wait=True)  # 等待所有检测完毕才进行下一步
    return ipList


def codeShiBie(url, result):
    '''函数：验证码识别'''
    if captcha[0] != '':
        user = captcha[0]
        passwd = captcha[1]
        try:
            getImgBytes = requests.get(url=url, timeout=6, allow_redirects=True, verify=False)  # 请求获取验证码二进制数据
            base64Data = base64.b64encode(getImgBytes.content)
            b64 = base64Data.decode()
            data = {"username": user, "password": passwd, "typeid": 3, "image": b64}
            result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
            if result['success']:
                code = result["data"]["result"]  # 获取识别后的验证码
                if (len(code) == 4) or (len(code) == 6):  # 进一步提升识别率，限制识别出的字符在4个以内
                    return code
                else:
                    codeShiBie(url, result)
            else:
                codeShiBie(url, result)
        except Exception as f:
            result.config(fg='red')
            result.insert("end", "\033[1;31m[-] 验证码识别模块失败，请检查配置文件！\033[0m\n")
            return ''
    else:
        result.config(fg='red')
        result.insert("end", "\033[1;31m[-] 验证码识别模块失败，请检查配置文件！\033[0m\n")
        return ''


def resultOutput(result):
    """ 生成结果文件 """
    with open('result.txt', 'a+', encoding="utf-8") as f:
        if len(result) != 0:
            f.write(result+"\n")
        else:
            msg = "很遗憾，没有一个爆破成功！"
            f.write(msg)


def _async_raise(tid, exctype):
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

