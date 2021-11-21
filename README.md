<h1 align="center" >SeBruteGUI</h1>

<h4 align="center" >登入框暴力破解</h3>
<p align="center">
    <a href="https://github.com/kracer127/SeBruteGUI"><img alt="SeBruteGUI" src="https://visitor-badge.glitch.me/badge?page_id=kracer127.SeBruteGUI"></a>
    <a href="https://github.com/kracer127/SeBruteGUI"><img alt="SeBruteGUI" src="https://img.shields.io/github/stars/kracer127/SeBruteGUI.svg"></a>
    <a href="https://github.com/kracer127/SeBruteGUI/releases"><img alt="SeBruteGUI" src="https://img.shields.io/github/release/kracer127/SeBruteGUI.svg"></a>
</p>


## 0x01 介绍
作者：kracer

定位：专注登入框暴力破解，无视复杂的前端js加密。

语言：python3开发

功能：使用selenium+chromedriver模拟浏览器点击登入，无视复杂的前端js加密。多线程快速破解，可批量IP检测弱口令。exe可执行文件加上GUI界面，简单操作，别再为分析js加密而头疼了。



## 0x02 安装使用

1、所需库安装

```python
pip3 install -r requirements.txt
```

2、使用

```python
>>python3 SeBruteGUI.py  开启GUI界面，亦或直接打开exe可执行文件。
```

3、说明

```python
文件夹：imgs文件夹 --- GUI的背景图片等。
文件：SeBruteGUI.py --- 主函数入口。
文件：commom.py --- 用户输入处理、网址存活检测及结果生成等。
文件：config.json --- 配置文件，chromedriver.exe路径、验证码识别模块的账号密码和ip代理池设置。
文件：processOneIp.py --- 单ip的爆破类。
文件：processManyIp.py --- 批量ip的爆破类。
```



## 0x03 效果展示

**1、程序打开：**

<img src=".\imgs\open.png" alt="operating" style="zoom:80%;" />

**2、程序运行：**

<img src=".\imgs\run.png" alt="result" style="zoom:80%;" />



## 0x04 一些说明:

1、使用前提条件：

​	① 安装好chrome浏览器，下载对应版本号的chromedriver.exe驱动。

​		chrome官网：https://www.google.cn/chrome/

​		chromedriver驱动官网：https://chromedriver.chromium.org/downloads

​	② 知道xpath路径怎么找：www.baidu.com

2、如何使用验证码识别模块：

​	① 到[快识别]([图片识别-打码平台-打码网站-识别验证码-图鉴网络科技有限公司](http://www.kuaishibie.cn/))官网注册账号，并充值购买<10块够你用啦>。

​	② 到config.json文件中填入您的账号密码 --- "captcha": ["账号","密码"]。

​	③ 注意：有的网站登入错误达到一定次数才会出现验证码，所以别粗心。

3、代理模块使用：

​	① 将自己的代理ip池保存为txt文件，在config.json的 "proxy": ["把路径填在这里"] 中填写。

​	② 或者在GUI界面中选择文件也可以，注意输入框只能填写单个代理ip。

​	③ 代理ip最好检测下有效性，软件的代理ip有效性检测还待优化。

4、当前为第一版本，用户的非正常操作容易导致软件无法运行，使用过程有问题欢迎给我留言。

5、程序可优化的地方还挺多，后续有时间再弄了。真诚地邀请各位大佬加入后续开发，一起学习进步，唯一QQ:0x91b8bb99。



**本项目仅供学习, 测试, 交流使用, 勿用于非法用途。**

​	**请使用者遵守《中华人民共和国网络安全法》，勿用于非授权测试，如作他用所承受的法律责任一概与**

**作者无关，下载使用即代表使用者同意上述观点**。

​	**喜欢❤️请收藏给一个star吧👍**

