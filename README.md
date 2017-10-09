# guesst
# python2.7！

http://www.gsxt.gov.cn/index
获得详细页的url和cookie，就可以拿数据了
可以尝试手机APP！！！

代码和方法只供学习交流使用！产生的一切责任，本人概不负责！！


验证码很让人头疼----极验，现在6.0版本来了，用这种方式实现，通过率只有一成！！
增加geetest_gsxt_selenium.py成功率有三四成！！！
极验的机器学习太强了!
还有一点是轨迹！！可以考虑使用已经成功的历史轨迹来作为当前的轨迹！！
感谢https://github.com/darbra/geetest


希望大家可以一起交流781816703@qq.com


## windows下配的环境（当时这个环境让人头疼）
## 安装python2.7
添加环境变量===我的电脑--右击‘属性’==高级系统设置==环境变量==PATH----‘python_2\Scipts’

解压phantomjs到python\Scripts下

安装PIL ====1.1.7

chromedriver.exe放到python\Scripts下
火狐geckodriver.exe


pip install selenium


程序：
# chrome
from selenium import webdriver

# chromedriver.exe模拟器可以看到chrome现象！
obj = webdriver.Chrome(executable_path=r"E:\python_2\Scripts\chromedriver.exe")

obj.get('https://www.baidu.com/')
obj.save_screenshot("1.png")  # 截图保存


# phantomjs
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置userAgent
dcap["phantomjs.page.settings.userAgent"] = (
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 ")

obj = webdriver.PhantomJS(executable_path='E:\python_2\Scripts\phantomjs.exe', desired_capabilities=dcap)  # 加载网址
obj.get('https://www.baidu.com/')
