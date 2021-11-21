# -*- coding:utf-8 -*-
# Date: 2021-10-18
# Author:kracer
# Version: 1.0


from tkinter import *
import tkinter.messagebox  # 消息弹出框
import tkinter.filedialog  # 文件选择框
from PIL import Image, ImageTk
from threading import Thread
from common import *
from processOneIp import processOneIp
from processManyIp import processManyIp
import os
sys.setrecursionlimit(1500)



class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.title('登入框暴力破解v1.0 __by:kracer')
        self.root.iconbitmap(default=r'.//imgs//icon.ico')
        """ 添加背景图片 """
        self.canvas = Canvas(self.root, width=1000, height=700, bd=0, highlightthickness=0)  # 创建画布，bd(borderwidth)为文本框边框宽度， highlightthickness边框灰度
        self.backgroundImage = ImageTk.PhotoImage(Image.open('.//imgs//background.gif'))  # 加载gif图片
        self.canvas.create_image(500, 400, image=self.backgroundImage)  # 500, 400为偏移参数
        self.canvas.pack()
        """ 获得本地窗口的大小 """
        left = (self.root.winfo_screenwidth()-1000)/2  # 向右偏移量
        top = (self.root.winfo_screenheight()-700)/2  # 向下偏移量
        self.root.geometry('%dx%d+%d+%d' % (1000, 650, left, top))
        self.root.resizable(0, 0)  # 强制窗口大小，不可缩放


    def setVal(self):
        """ 常量设置 """
        self.startFlag = True  # 开启爆破任务标志
        self.allUserInput = []  # 装载用户的所有输入
        self.modeValue = StringVar()  # 爆破模式 1 , 2
        self.threadNum = IntVar()  # 用户选择的线程数
        self.threadNumFile = []  # 线程数列表
        self.url = StringVar()  # 爆破目标url
        self.urlFile = []  # 爆破目标文件批量url
        self.username = StringVar()  # 爆破的用户名
        self.usernameFile = []  # 爆破的用户名(文件批量）
        self.password = StringVar()  # 爆破的密码
        self.passwordFile = []  # 爆破的密码(文件批量）
        self.captchaUrl = StringVar()  # 验证码url
        self.captchaFile = []  # 验证码列表
        self.usernameXpath = StringVar()  # 用户名输入框的xpath
        self.passwordXpath = StringVar()  # 密码输入框的xpath
        self.captchaXpath = StringVar()  # 验证码输入框的xpath
        self.submitXpath = StringVar()  # 提交按钮的xpath
        self.submitFile = []  # 提交按钮列表
        self.proxy = []
        if proxy != [""]:
            self.proxyFile = proxy  # 浏览器代理的ip地址池
        else:
            self.proxyFile = []
          # 浏览器代理的ip地址池(文件批量）
        self.chromedriver = StringVar()  # chromedriver.exe的路径
        if chromePath != [""]:
            self.chromedriverFile = chromePath
        else:
            self.chromedriverFile = []  # chromedriver.exe的路径(通过文件选择）


    def run(self):
        """ 添加其他组件或窗口 """
        self.setVal()
        self.Frame1()
        self.Frame2()
        self.Frame3()
        self.Frame4()
        self.Frame5()
        self.Frame6()
        self.Frame7()
        self.root.mainloop()


    def Frame1(self):
        ''' 框架1：导航栏 '''
        frame1 = Frame(self.root, bd=2)
        frame1.pack()
        self.canvas.create_window(0, 0, width=2000, height=55, window=frame1)  # 在画布上嵌入
        """ 添加说明、关于按钮 """
        buttonExplain = Button(self.root, text="说明", font=('微软雅黑', 12), fg='black', justify=CENTER, bd=3, bg='#CDCDCD', command=self.frameExplain)  # 说明按钮
        buttonExplain.pack()
        self.canvas.create_window(32, 13, width=60, height=25, window=buttonExplain)  # 在画布上嵌入
        buttonAbout = Button(self.root, text="关于", font=('微软雅黑', 12), fg='black', justify=CENTER, bd=3, bg='#CDCDCD', command=self.frameAbout)  # 说明按钮
        buttonAbout.pack()
        self.canvas.create_window(94, 13, width=60, height=25, window=buttonAbout)  # 在画布上嵌入


    def Frame2(self):
        '''框架2：爆破模式'''
        self.canvas.create_rectangle(15, 45, 260, 185)  # 爆破模式的矩形边框
        textLable1 = Label(self.root, text="爆破模式", bg='red')
        textLable1.pack()
        self.canvas.create_window(55, 45, width=60, height=25, window=textLable1)  # 在画布上嵌入
        """ 两个单选按钮 """
        self.modeValue.set(' ')  # 清除两个首次打开即默认选中的状态
        rdbOne = Radiobutton(self.root, text="单个IP爆破", font=("微软雅黑", 12), bg='#32CD32', fg='blue', variable=self.modeValue, value="mode1")
        rdbOne.pack()
        self.canvas.create_window(100, 90, width=160, height=25, window=rdbOne)  # 在画布上嵌入
        rdbMany = Radiobutton(self.root, text="批量IP爆破", font=("微软雅黑", 12), bg='#32CD32', fg='blue', variable=self.modeValue, value="mode2")
        rdbMany.pack()
        self.canvas.create_window(100, 140, width=160, height=25, window=rdbMany)  # 在画布上嵌入
        textLable11 = Label(self.root, text="必\n选\n项", font=("微软雅黑", 13), fg='red', bg='#ADDBE6')
        textLable11.pack()
        self.canvas.create_window(225, 117, width=30, height=85, window=textLable11)  # 在画布上嵌入


    def Frame3(self):
        '''说明面板：简单提示 '''
        self.canvas.create_rectangle(15, 340, 260, 205)  # 爆破模式的矩形边框
        textLable12 = Label(self.root, text="Tips", bg='red')
        textLable12.pack()
        self.canvas.create_window(55, 205, width=60, height=25, window=textLable12)  # 在画布上嵌入
        tipsText = Text(self.root, fg='green')  # 文本
        tipsText.insert("insert", "①安装chrome浏览器，并下载版本对应的chromedriver.exe。\n\n"
                                  "②请先选择好爆破模式，再开始爆破任务。\n\n"
                                  "③线程建议6-20，电脑配置不高的高线程软件会卡死。")
        tipsText.pack()
        self.canvas.create_window(137, 278, width=243, height=120, window=tipsText)  # 在画布上嵌入


    def Frame4(self):
        ''' 线程数选择和开始、清空按钮 '''
        textLable13 = Label(self.root, text="线程数", bg='red', font=("微软雅黑, 13"))
        textLable13.pack()
        self.canvas.create_window(45, 375, width=70, height=40, window=textLable13)  # 在画布上嵌入
        threadScale = Scale(self.root, bg='#ADD8E6', variable=self.threadNum, from_=1, to=30, length=450, width=16, orient=HORIZONTAL)
        threadScale.pack(anchor=CENTER)
        self.canvas.create_window(325, 375, width=450, height=40, window=threadScale)  # 在画布上嵌入


    def Frame5(self):
        """ 输出面板 """
        self.canvas.create_line(0, 435, 1000, 435, fill="red")  # 输出的线条
        textLable14 = Label(self.root, text="结果输出:", bg='red')
        textLable14.pack()
        self.canvas.create_window(45, 425, width=100, height=20, window=textLable14)  # 在画布上嵌入
        self.resultText = Text(self.root, bg='#778899', bd=4, font=("微软雅黑", 12))  # 文本
        scroll = Scrollbar(self.root)  # 滚动条
        scroll.pack(side=RIGHT, fill=Y)
        self.resultText.pack(side=LEFT, fill=Y)
        scroll.config(command=self.resultText.yview)
        self.resultText.config(yscrollcommand=scroll.set)
        self.canvas.create_window(990, 585, width=20, height=290, window=scroll)  # 在画布上嵌入
        self.canvas.create_window(500, 585, width=1000, height=300, window=self.resultText)  # 在画布上嵌入


    def Frame6(self):
        """ 用户输入数据面板 """
        global entryUrl, entryUserName, entryPassWord, entryCaptchaUrl, entryXpathUserName, entryXpathPassWord, entryXpathCaptcha, entryXpathSubmit, entryProxy, entryChromeDriver
        self.canvas.create_rectangle(280, 46, 988, 340, outline='red')  # 爆破模式的矩形边框
        textLable15 = Label(self.root, text="用户输入", font=("微软雅黑", 10), bg='red')
        textLable15.pack()
        self.canvas.create_window(320, 47, width=60, height=25, window=textLable15)  # 在画布上嵌入
        """ 输入：探测目标 """
        LabelUrl = Label(self.root, text="目标URL:", font=("微软雅黑", 10), anchor="w", bg='red')
        LabelUrl.pack()
        self.canvas.create_window(380, 77, width=150, height=20, window=LabelUrl)  # 在画布上嵌入
        entryUrl = Entry(self.root, fg="#1E90FF")
        entryUrl.pack()
        self.canvas.create_window(645, 77, width=300, height=20, window=entryUrl)  # 在画布上嵌入
        buttonSeletFileUrl = Button(self.root, text="选择文件", font=("微软雅黑", 10), anchor="w", bg='white', command=lambda: self.commandSelectFile(entryUrl, self.urlFile))
        buttonSeletFileUrl.pack()
        self.canvas.create_window(767, 77, width=60, height=20, window=buttonSeletFileUrl)  # 在画布上嵌入
        """ 输入：用户名 """
        LabelUserName = Label(self.root, text="用户名:", font=("微软雅黑", 10), anchor="w", bg='red')
        LabelUserName.pack()
        self.canvas.create_window(380, 105, width=150, height=20, window=LabelUserName)  # 在画布上嵌入
        entryUserName = Entry(self.root, fg="#1E90FF")
        entryUserName.pack()
        self.canvas.create_window(645, 105, width=300, height=20, window=entryUserName)  # 在画布上嵌入
        buttonSeletFileUserName = Button(self.root, text="选择文件", font=("微软雅黑", 10), anchor="w", bg='white', command=lambda: self.commandSelectFile(entryUserName, self.usernameFile))
        self.canvas.create_window(767, 105, width=60, height=20, window=buttonSeletFileUserName)  # 在画布上嵌入
        """ 输入：密码 """
        LabelPassWord = Label(self.root, text="密码:", font=("微软雅黑", 10), anchor="w", bg='red')
        LabelPassWord.pack()
        self.canvas.create_window(380, 133, width=150, height=20, window=LabelPassWord)  # 在画布上嵌入
        entryPassWord = Entry(self.root, fg="#1E90FF")
        entryPassWord.pack()
        self.canvas.create_window(645, 133, width=300, height=20, window=entryPassWord)  # 在画布上嵌入
        buttonSeletFilePassWord = Button(self.root, text="选择文件", font=("微软雅黑", 10), anchor="w", bg='white', command=lambda: self.commandSelectFile(entryPassWord, self.passwordFile))
        buttonSeletFilePassWord.pack()
        self.canvas.create_window(767, 133, width=60, height=20, window=buttonSeletFilePassWord)  # 在画布上嵌入
        """ 输入：验证码url """
        LabelCaptchaUrl = Label(self.root, text="验证码URL:", font=("微软雅黑", 10), anchor="w", bg='red')
        LabelCaptchaUrl.pack()
        self.canvas.create_window(380, 161, width=150, height=20, window=LabelCaptchaUrl)  # 在画布上嵌入
        entryCaptchaUrl = Entry(self.root, fg="#1E90FF")
        entryCaptchaUrl.pack()
        self.canvas.create_window(645, 161, width=300, height=20, window=entryCaptchaUrl)  # 在画布上嵌入
        """ 输入：用户名的xpath """
        LabelXpathUserName = Label(self.root, text="用户名的xpath:", font=("微软雅黑", 10), anchor="w", bg='red')
        LabelXpathUserName.pack()
        self.canvas.create_window(380, 189, width=150, height=20, window=LabelXpathUserName)  # 在画布上嵌入
        entryXpathUserName = Entry(self.root, fg="#1E90FF")
        entryXpathUserName.pack()
        self.canvas.create_window(645, 189, width=300, height=20, window=entryXpathUserName)  # 在画布上嵌入
        """ 输入：密码的xpath """
        LabelXpathPassWord = Label(self.root, text="密码的xpath:", font=("微软雅黑", 10), anchor="w", bg='red')
        LabelXpathPassWord.pack()
        self.canvas.create_window(380, 217, width=150, height=20, window=LabelXpathPassWord)  # 在画布上嵌入
        entryXpathPassWord = Entry(self.root, fg="#1E90FF")
        entryXpathPassWord.pack()
        self.canvas.create_window(645, 217, width=300, height=20, window=entryXpathPassWord)  # 在画布上嵌入
        """ 输入：验证码的xpath """
        LabelXpathCaptcha = Label(self.root, text="验证码的xpath:", font=("微软雅黑", 10), anchor="w", bg='red')
        LabelXpathCaptcha.pack()
        self.canvas.create_window(380, 245, width=150, height=20, window=LabelXpathCaptcha)  # 在画布上嵌入
        entryXpathCaptcha = Entry(self.root, fg="#1E90FF")
        entryXpathCaptcha.pack()
        self.canvas.create_window(645, 245, width=300, height=20, window=entryXpathCaptcha)  # 在画布上嵌入
        """ 输入：提交按钮的xpath """
        LabelXpathSubmit = Label(self.root, text="提交的xpath:", font=("微软雅黑", 10), anchor="w", bg='red')
        LabelXpathSubmit.pack()
        self.canvas.create_window(380, 272, width=150, height=20, window=LabelXpathSubmit)  # 在画布上嵌入
        entryXpathSubmit = Entry(self.root, fg="#1E90FF")
        entryXpathSubmit.pack()
        self.canvas.create_window(645, 272, width=300, height=20, window=entryXpathSubmit)  # 在画布上嵌入
        """ 输入：代理ip的选项 """
        LabelProxy = Label(self.root, text="代理设置:", font=("微软雅黑", 10), anchor="w", bg='red')
        LabelProxy.pack()
        self.canvas.create_window(380, 300, width=150, height=20, window=LabelProxy)  # 在画布上嵌入
        entryProxy = Entry(self.root, fg="#1E90FF")
        entryProxy.pack()
        self.canvas.create_window(645, 300, width=300, height=20, window=entryProxy)  # 在画布上嵌入
        buttonSeletFileProxy = Button(self.root, text="选择文件", font=("微软雅黑", 10), anchor="w", bg='white', command=lambda: self.commandSelectFile(entryProxy, self.proxyFile))
        buttonSeletFileProxy.pack()
        self.canvas.create_window(767, 300, width=60, height=20, window=buttonSeletFileProxy)  # 在画布上嵌入
        """ 输入：chromedriver设置 """
        LabelChromeDriver = Label(self.root, text="chromedriver路径:", font=("微软雅黑", 10), anchor="w", bg='red')
        LabelChromeDriver.pack()
        self.canvas.create_window(380, 328, width=150, height=20, window=LabelChromeDriver)  # 在画布上嵌入
        entryChromeDriver = Entry(self.root, fg="#1E90FF")
        entryChromeDriver.pack()
        self.canvas.create_window(645, 328, width=300, height=20, window=entryChromeDriver)  # 在画布上嵌入
        buttonSeletFileChromedriver = Button(self.root, text="选择文件", font=("微软雅黑", 10), anchor="w", bg='white', command=lambda: self.commandSelectFile(entryChromeDriver, self.chromedriverFile))
        buttonSeletFileChromedriver.pack()
        self.canvas.create_window(767, 328, width=60, height=20, window=buttonSeletFileChromedriver)  # 在画布上嵌入


    def Frame7(self):
        """ 开始按钮、清空按钮 """
        buttonStart = Button(self.root, text="开始", font=("微软雅黑", 15), bg='green', command=self.commandButtonStart)
        buttonStart.pack()
        self.canvas.create_window(680, 380, width=80, height=55, window=buttonStart)  # 在画布上嵌入
        buttonCancel = Button(self.root, text="停止", font=("微软雅黑", 15), bg='green', command=self.commandButtonCancel)
        buttonCancel.pack()
        self.canvas.create_window(790, 380, width=80, height=55, window=buttonCancel)  # 在画布上嵌入
        buttonClear = Button(self.root, text="清空", font=("微软雅黑", 15), bg='green', command=self.commandButtonClear)
        buttonClear.pack()
        self.canvas.create_window(900, 380, width=80, height=55, window=buttonClear)  # 在画布上嵌入


    def frameExplain(self):
        """ 说明菜单栏设置 """
        top = Toplevel()
        top.title('说明')
        text = Text(top, width=70, height=20, fg='red', font=("微软雅黑", 12))
        text.insert("insert", "\n1、只支持chrome浏览器，官网下载：https://www.google.cn/chrome/。\n同时需要下载"
                              "chromedrover.exe驱动，官网地址：https://chromedriver.chromium.org/downloads  (注意下载相对应版本，否则工具无法运行。)\n\n"
                              "2、遇到需有验证码登入框爆破，需要提前在config.json填好<快识别>账号密码,官网注册：http://www.kuaishibie.cn/。\n来一波推荐"
                              "码哈哈：084a0c65a86c4cd3a812bf8f1c139aec\n\n"
                              "3、爆破之前，先尝试登入错误5左右，观察是否会出现验证码。有的网站只有登入错误达到一定次数才会出现验证码，所以记得好好查看"
                              "是否存在，别爆破了个寂寞。\n\n"
                              "4、对于登入错误达到次数封ip情况，本工具支持配置自己的代理ip池进行爆破。\n\n"
                              "5、爆破的结果保存在result.txt里。\n\n"
                              "6、对于批量ip爆破情况，本工具自带存活检测。")
        text.pack()


    def frameAbout(self):
        """ 说明菜单栏设置 """
        top = Toplevel()
        top.title('关于')
        text = Text(top, width=50, height=20, fg='red', font=("微软雅黑", 12))
        text.insert("insert", "\n1、开发本工具是因为在渗透测试的弱口令检测阶段，遇到复杂的前端js加密情况，"
                              "分析加密过程耗时耗力，心想不如直接来个多线程的模拟登入，简单又省力，于是诞生了此工具。\n\n"
                              "2、python语言开发，使用的selenium库, 借助chromedriver.exe模拟鼠标点击登入，无视前端的js加密，多线程"
                              "爆破速度毫不逊色。"
                              "\n\n3、本工具为第一版，后续版本地址：https://github.com/kracer127/seBruteGUI\n\n"
                              "3、工具问题或有好的建议，唯一QQ:0x91b8bb99")
        text.pack()


    def commandSelectFile(self, entry, List):
        """ 爆破模式的选择响应事件 """
        filename = tkinter.filedialog.askopenfilename()
        if filename != '':
            entry.delete(0, END)
            List.append(filename)
            entry.insert("insert", filename)
        else:
            entry.insert("insert", "")


    def informationProcess(self):
        """ 对用户的输入进行处理 """
        if self.modeValue.get() != ' ':
            self.startFlag = True
            if self.threadNum.get() != None:
                self.threadNumFile.append(self.threadNum.get())
                self.allUserInput.append(self.threadNumFile)
            if self.urlFile == []:
                if entryUrl.get() != '':
                    self.url = entryUrl.get()
                    self.urlFile.append(self.url.strip())
                else:
                    self.startFlag = False
                    self.resultText.insert(END, "[-] 没有检测到<目标url>, 请重新输入后再使用！\n")
                    tkinter.messagebox.showerror('错误', "请输入目标url ！")
            if self.usernameFile == []:
                if entryUserName.get() != '':
                    self.username = entryUserName.get()
                    self.usernameFile.append(self.username.strip())
                else:
                    self.startFlag = False
                    self.resultText.insert(END, "[-] 没有检测到<用户名>, 请重新输入后再使用！\n")
                    tkinter.messagebox.showerror('错误', "请输入用户名 ！")
            if self.passwordFile == []:
                if entryPassWord.get() != '':
                    self.password = entryPassWord.get()
                    self.passwordFile.append(self.password.strip())
                else:
                    self.startFlag = False
                    self.resultText.insert(END, "[-] 没有检测到<密码>, 请重新输入后再使用！\n")
                    tkinter.messagebox.showerror('错误', "请输入密码 ！")
            if entryCaptchaUrl.get() != '':
                if entryXpathCaptcha.get() != '':
                    self.captchaUrl = entryCaptchaUrl.get()
                    self.captchaXpath = entryXpathCaptcha.get()
                    self.captchaFile.append(self.captchaUrl.strip())
                    self.captchaFile.append(self.captchaXpath.strip())
                else:
                    self.startFlag = False
                    self.resultText.insert(END, "[-] 没有检测到<验证码的xpath>, 请重新输入后再使用！\n")
                    tkinter.messagebox.showerror('错误', "请输入验证码的xpath ！")
            if entryXpathUserName.get() == '':
                self.startFlag = False
                self.resultText.insert(END, "[-] 没有检测到<用户名的xpath>, 请重新输入后再使用！\n")
                tkinter.messagebox.showerror('错误', "请输入用户名的xpath ！")
            else:
                self.usernameXpath = entryXpathUserName.get()
                self.usernameFile.append(self.usernameXpath.strip())
            if entryXpathPassWord.get() == '':
                self.startFlag = False
                self.resultText.insert(END, "[-] 没有检测到<密码的xpath>, 请重新输入后再使用！\n")
                tkinter.messagebox.showerror('错误', "请输入密码的xpath ！")
            else:
                self.passwordXpath = entryXpathPassWord.get()
                self.passwordFile.append(self.passwordXpath.strip())
            if entryXpathSubmit.get() == '':
                self.startFlag = False
                self.resultText.insert(END, "[-] 没有检测到<提交按钮的xpath>, 请重新输入后再使用！\n")
                tkinter.messagebox.showerror('错误', "请输入提交按钮的xpath ！")
            else:
                self.submitXpath = entryXpathSubmit.get()
                self.submitFile.append(self.submitXpath.strip())
            if self.proxyFile == []:
                if entryProxy.get() != '':
                    self.proxy = entryProxy.get()
                    self.proxyFile.append(self.proxy.strip())
            if self.chromedriverFile == []:
                if entryChromeDriver.get() != '':
                    self.chromedriver = entryChromeDriver.get()
                    self.chromedriverFile.append(self.chromedriver)
                else:
                    self.startFlag = False
                    self.resultText.insert(END, "[-] 没有检测到<chromedrover.exe路径>, 请重新输入后再使用！\n")
                    tkinter.messagebox.showerror('错误', "请配置chromedrover.exe路径 ！")
        else:
            self.startFlag = False
            tkinter.messagebox.showerror('错误', "请选择爆破模式！")


    def informationResult(self):
        """ 用户输入的最终处理结果 """
        try:
            self.allUserInput.append(self.urlFile)
            self.allUserInput.append(self.usernameFile)
            self.allUserInput.append(self.passwordFile)
            self.allUserInput.append(self.captchaFile)
            self.allUserInput.append(self.submitFile)
            self.allUserInput.append(self.proxyFile)
            self.allUserInput.append(self.chromedriverFile)
        except Exception as e:
            self.resultText.insert(END, "\033[1;31m[-] 处理用户的输入过程出错, 建议重启软件！\033[0m\n")


    def commandButtonStart(self):
        """ 按下开始按钮后的响应事件 """
        global threadStopFlag
        self.informationProcess()  # 提前判断用户的输入
        if self.startFlag == True:
            self.informationResult()
            choiceMode = self.modeValue.get()
            tkinter.messagebox.showinfo('提示', "初始化成功，爆破任务开启！")
            self.resultText.delete(0.0, END)
            threadStopFlag = False
            if choiceMode == 'mode1':
                """ 如果是爆破模式一 """
                sunpro1 = Thread(target=processOneIp(self.resultText, self.allUserInput).startMoreThread())
                sunpro1.setDaemon(True)
                sunpro1.start()
            else:
                """ 如果是爆破模式二 """
                sunpro2 = Thread(target=processManyIp(self.resultText, self.allUserInput).startMoreThread())
                sunpro2.setDaemon(True)
                sunpro2.start()
            """ 清空数据列表，方便下一次的重载 """
            self.threadNumFile.clear()
            self.urlFile.clear()
            self.usernameFile.clear()
            self.passwordFile.clear()
            self.captchaFile.clear()
            self.submitFile.clear()
            self.proxyFile.clear()
            self.chromedriverFile.clear()
            self.allUserInput.clear()
        else:
            self.threadNumFile.clear()
            self.urlFile.clear()
            self.usernameFile.clear()
            self.passwordFile.clear()
            self.captchaFile.clear()
            self.submitFile.clear()
            self.proxyFile.clear()
            self.chromedriverFile.clear()
            self.allUserInput.clear()


    def commandButtonCancel(self):
        global threadStopFlag
        try:
            threadStopFlag = True
            tkinter.messagebox.showinfo('提示', "正在停止爆破任务！")
            """ 清空所有数据 """
            self.threadNumFile.clear()
            self.urlFile.clear()
            self.usernameFile.clear()
            self.passwordFile.clear()
            self.captchaFile.clear()
            self.submitFile.clear()
            self.proxyFile.clear()
            self.chromedriverFile.clear()
            self.allUserInput.clear()
        except Exception as e:
            self.startFlag = False
            self.resultText.insert(END, "[-] 停止任务出错，建议重启后再使用！\n")
            tkinter.messagebox.showerror('错误', "停止任务出错！")


    def commandButtonClear(self):
        try:
            entryUrl.delete(0, END)
            entryUserName.delete(0, END)
            entryPassWord.delete(0, END)
            entryCaptchaUrl.delete(0, END)
            entryXpathUserName.delete(0, END)
            entryXpathPassWord.delete(0, END)
            entryXpathCaptcha.delete(0, END)
            entryXpathSubmit.delete(0, END)
        except Exception as e:
            self.startFlag = False
            self.resultText.insert(END, "[-] 清空输入数据出错，建议重启后再使用！\n")
            tkinter.messagebox.showerror('提示', "清空输入数据出错！")


GUI().run()


if not os.path.exists("result.txt"):
    with open("result.txt", 'a+', encoding='utf-8') as f1:
        text = '很遗憾，没有一个爆破成功！'
        f1.write(text)