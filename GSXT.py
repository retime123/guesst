# -*-coding:utf-8-*-
__author__ = 'retime123'
import requests
import re,os,sys
import StringIO
# from io import StringIO#python3导入方式
from PIL import Image
import random
import math
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
import selenium
import pandas as pd

reload(sys)
sys.setdefaultencoding('utf-8')


my_url = "http://www.gsxt.gov.cn/index"


class crack_picture(object):
    def __init__(self, img_url1, img_url2):
        # 缓存两个图片
        self.img1, self.img2 = self.picture_get(img_url1, img_url2)

    def picture_get(self, img_url1, img_url2):
        hd = {"Host": "static.geetest.com",
              "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
        img1 = StringIO.StringIO(self.repeat(img_url1, hd).content)
        img2 = StringIO.StringIO(self.repeat(img_url2, hd).content)
        # 返回stringIO对象
        return img1, img2

    def repeat(self, url, hd):
        times = 10
        while times > 0:
            try:
                ans = requests.get(url, headers=hd)
                return ans
            except:
                times -= 1

    def pictures_recover(self):
        xpos = self.judge(self.picture_recover(self.img1, 'img1.jpg'), self.picture_recover(self.img2, 'img2.jpg')) - 6
        print('=====',xpos)
        # 坐标
        return self.darbra_track(xpos)

    def picture_recover(self, img, name):
        a = [39, 38, 48, 49, 41, 40, 46, 47, 35, 34, 50, 51, 33, 32, 28, 29, 27, 26, 36, 37, 31, 30, 44, 45, 43, 42, 12,
             13, 23, 22, 14, 15, 21, 20, 8, 9, 25, 24, 6, 7, 3, 2, 0, 1, 11, 10, 4, 5, 19, 18, 16, 17]
        # 使用pil进行处理,返回PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=312x116对象
        im = Image.open(img)
        im_new = Image.new("RGB", (260, 116))
        for row in range(2):
            for column in range(26):

                right = a[row * 26 + column] % 26 * 12 + 1
                down = 58 if a[row * 26 + column] > 25 else 0
                for w in range(10):
                    for h in range(58):
                        ht = 58 * row + h
                        wd = 10 * column + w
                        im_new.putpixel((wd, ht), im.getpixel((w + right, h + down)))
        im_new.save(name)
        return im_new

    def darbra_track(self, distance):
        return [[distance, 0.5, 1]]
        # crucial trace code was deleted

    def diff(self, img1, img2, wd, ht):
        rgb1 = img1.getpixel((wd, ht))
        rgb2 = img2.getpixel((wd, ht))
        tmp = reduce(lambda x, y: x + y, map(lambda x: abs(x[0] - x[1]), zip(rgb1, rgb2)))
        return True if tmp >= 200 else False

    def col(self, img1, img2, cl):
        for i in range(img2.size[1]):
            if self.diff(img1, img2, cl, i):
                return True
        return False

    def judge(self, img1, img2):
        for i in range(img2.size[0]):
            if self.col(img1, img2, i):
                return i
        return -1


class gsxt(object):
    def __init__(self, br_name="phantomjs"):
        # 传入chrome浏览器,调用get_webdriver()方法
        self.br = self.get_webdriver(br_name)
        # self.br.save_screenshot("10.png")
        # 调用显式超时时间,最长超时时间为15秒，每1秒扫描一次页面
        self.wait = WebDriverWait(self.br, 15, 1.0)
        self.br.set_page_load_timeout(8)
        self.br.set_script_timeout(8)

    # 执行页面搜索
    def input_params(self, name):
        # self.br.implicitly_wait(30)# 没起作用
        # 延时
        self.br.set_page_load_timeout(30)
        self.br.set_script_timeout(30)

        self.br.get(my_url)
        # self.br.save_screenshot("index.png")# 主页图片

        element = self.wait_for(By.ID, "keyword")
        element.send_keys(name)
        time.sleep(1.1)
        element = self.wait_for(By.ID, "btn_query")
        element.click()
        time.sleep(1.1)

    def drag_pic(self):
        '''提取图片url'''
        return (self.find_img_url(self.wait_for(By.CLASS_NAME, "gt_cut_fullbg_slice")),
                self.find_img_url(self.wait_for(By.CLASS_NAME, "gt_cut_bg_slice")))

    def wait_for(self, by1, by2):
        return self.wait.until(EC.presence_of_element_located((by1, by2)))

    def find_img_url(self, element):
        try:
            # 替换，将结尾为webp的扩展名替换为jpg
            return re.findall('url\("(.*?)"\)', element.get_attribute('style'))[0].replace("webp", "jpg")
        except:
            return re.findall('url\((.*?)\)', element.get_attribute('style'))[0].replace("webp", "jpg")

    def emulate_track(self, tracks):
        # 模拟滑动
        '''
        move_by_offset(xoffset, yoffset) ——鼠标从当前位置移动到某个坐标
        move_to_element(to_element) ——鼠标移动到某个元素
        move_to_element_with_offset(to_element, xoffset, yoffset) ——移动到距某个元素（左上角坐标）多少距离的位置
        '''
        time.sleep(1)
        element = self.br.find_element_by_class_name("gt_slider_knob")
        # click_and_hold(on_element=None) ——点击鼠标左键，不松开
        # perform() ——执行链中的所有动作
        # move_to_element(to_element) ——鼠标移动到某个元素
        ActionChains(self.br).move_to_element(to_element=element).perform()
        ActionChains(self.br).click_and_hold(on_element=element).perform()
        time.sleep(1)
        su = random.randint(10,40)
        for x, y, t in tracks:
            print (x, y, t, su)
            # ActionChains(self.br).move_by_offset(xoffset=x / 2, yoffset=y+20).perform()
            # time.sleep(random.uniform(0, 0.5))
            # ActionChains(self.br).move_by_offset(xoffset=x / 2 - 20, yoffset=y).perform()
            # time.sleep(random.uniform(0, 0.5))
            # ActionChains(self.br).move_by_offset(xoffset=20, yoffset=y).perform()
            # # time.sleep(random.uniform(0, 0.5))
            # # ActionChains(self.br).move_by_offset(xoffset=10, yoffset=y).perform()
            # # time.sleep(random.uniform(0, 0.5))
            # # ActionChains(self.br).move_by_offset(xoffset=10, yoffset=y).perform()
            if x > 100:
                if su > 30:
                    ActionChains(self.br).move_by_offset(xoffset=x - x/3, yoffset=y).perform()
                    time.sleep(random.uniform(0, 0.5))
                    ActionChains(self.br).move_by_offset(xoffset=x/3 - 20, yoffset=y).perform()
                    time.sleep(random.uniform(0, 0.5))
                    ActionChains(self.br).move_by_offset(xoffset=-su, yoffset=y).perform()
                    time.sleep(random.uniform(0, 0.5))
                    ActionChains(self.br).move_by_offset(xoffset=su/2, yoffset=y).perform()
                    time.sleep(random.uniform(0, 0.5))
                    ActionChains(self.br).move_by_offset(xoffset=su/2, yoffset=y).perform()
                    time.sleep(random.uniform(0, 0.5))
                    ActionChains(self.br).move_by_offset(xoffset=12, yoffset=y).perform()
                    time.sleep(random.uniform(0, 0.4))
                    ActionChains(self.br).move_by_offset(xoffset=2, yoffset=y).perform()
                    time.sleep(random.uniform(0, 0.3))
                    ActionChains(self.br).move_by_offset(xoffset=6, yoffset=y).perform()
                else:
                    ActionChains(self.br).move_by_offset(xoffset=x - x / 4, yoffset=y).perform()
                    time.sleep(random.uniform(0, 0.5))
                    ActionChains(self.br).move_by_offset(xoffset=x / 4 - 30, yoffset=y).perform()
                    time.sleep(random.uniform(0, 0.5))
                    ActionChains(self.br).move_by_offset(xoffset=-su, yoffset=y).perform()
                    time.sleep(random.uniform(0, 0.5))
                    ActionChains(self.br).move_by_offset(xoffset=su / 2, yoffset=y).perform()
                    time.sleep(random.uniform(0, 0.5))
                    ActionChains(self.br).move_by_offset(xoffset=su / 2, yoffset=y).perform()
                    time.sleep(random.uniform(0, 0.5))
                    ActionChains(self.br).move_by_offset(xoffset=20, yoffset=y).perform()
                    time.sleep(random.uniform(0, 0.4))
                    ActionChains(self.br).move_by_offset(xoffset=4, yoffset=y).perform()
                    time.sleep(random.uniform(0, 0.3))
                    ActionChains(self.br).move_by_offset(xoffset=6, yoffset=y).perform()

            else:
                if su > 20 and su < 30:
                    ActionChains(self.br).move_by_offset(xoffset=x - x/3, yoffset=y).perform()
                    time.sleep(random.uniform(0, 0.5))
                    ActionChains(self.br).move_by_offset(xoffset=x/3 - 20, yoffset=y).perform()
                    time.sleep(random.uniform(0, 0.5))
                    ActionChains(self.br).move_by_offset(xoffset=-su, yoffset=y).perform()
                    time.sleep(random.uniform(0, 0.5))
                    ActionChains(self.br).move_by_offset(xoffset=su/2, yoffset=y).perform()
                    time.sleep(random.uniform(0, 0.5))
                    ActionChains(self.br).move_by_offset(xoffset=su/2, yoffset=y).perform()
                    time.sleep(random.uniform(0, 0.5))
                    ActionChains(self.br).move_by_offset(xoffset=13, yoffset=y).perform()
                    time.sleep(random.uniform(0, 0.4))
                    ActionChains(self.br).move_by_offset(xoffset=4, yoffset=y).perform()
                    time.sleep(random.uniform(0, 0.3))
                    ActionChains(self.br).move_by_offset(xoffset=3, yoffset=y).perform()
                else:
                    ActionChains(self.br).move_by_offset(xoffset=x / 2, yoffset=y).perform()
                    time.sleep(random.uniform(0, 0.5))
                    ActionChains(self.br).move_by_offset(xoffset=x / 2 - su, yoffset=y).perform()
                    time.sleep(random.uniform(0, 0.5))
                    ActionChains(self.br).move_by_offset(xoffset=-su, yoffset=y).perform()
                    time.sleep(random.uniform(0, 0.5))
                    ActionChains(self.br).move_by_offset(xoffset=su/2, yoffset=y).perform()
                    time.sleep(random.uniform(0, 0.4))
                    ActionChains(self.br).move_by_offset(xoffset=su * 2, yoffset=y).perform()
                    time.sleep(random.uniform(0, 0.3))
                    ActionChains(self.br).move_by_offset(xoffset=-su/2, yoffset=y).perform()

            ActionChains(self.br).click_and_hold().perform()
            time.sleep(t)

        time.sleep(0.3)
        # release(on_element=None) ——在某个元素位置松开鼠标左键
        ActionChains(self.br).release(on_element=element).perform()
        time.sleep(0.8)
        element = self.wait_for(By.CLASS_NAME, "gt_info_text")
        ans = element.text.encode("utf-8")
        print u'##结果',ans
        return ans

    def run(self):
        # list_com = [raw_input(u'输入公司名：')]
        for i in [u'招商银行']:
            self.hack_geetest(i)
            time.sleep(2)
        # 退出浏览器
        # self.quit_webdriver()

    def quit_webdriver(self):
        self.br.quit()

    def hack_geetest(self, company=u"招商银行"):
        flag = True
        self.input_params(company)
        while flag:
            # 获取图片地址
            img_url1, img_url2 = self.drag_pic()
            tracks = crack_picture(img_url1, img_url2).pictures_recover()
            tsb = self.emulate_track(tracks)
            if '通过' in tsb:
                time.sleep(2)
                self.br.save_screenshot("10.png")
                soup = BeautifulSoup(self.br.page_source, 'html.parser')
                with open('gsxt.txt', 'w') as f:
                    f.write('')
                for i, sp in enumerate(soup.find_all("a", attrs={"class": "search_list_item"})):
                    cc = self.br.get_cookies()
                    link = "http://www.gsxt.gov.cn" + sp.get('href')
                    self.get_detail(link)# 详细页的url可以直接访问

                    print (re.sub("\s+", "", sp.get_text().encode("utf-8")))
                    print sp.get_text()
                    with open('gsxt.txt','a+') as f:
                        f.write(link)
                        f.write(sp.get_text())
                time.sleep(2)
                break
            elif '吃' in tsb:
                time.sleep(5)
            else:
                self.input_params(company)

    def get_detail(self, link):
        driver = self.get_webdriver('phantomjs')
        driver.set_page_load_timeout(30)
        driver.set_script_timeout(30)
        driver.get(link)
        time.sleep(5)
        driver.save_screenshot("2eeee.png")
        driver.quit()

    def get_webdriver(self, name):
        if name.lower() == "phantomjs":
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.userAgent"] = (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36")
            # 需要改源码__init__，添加proxy=None,RemoteWebDriver.__init__，添加proxy=proxy
            proxy = Proxy(
                {
                    'proxyType': ProxyType.MANUAL,
                    'httpProxy': get_proxy_ip_port()
                }
            )
            driver = webdriver.PhantomJS(executable_path='E:\python_2\Scripts\phantomjs.exe',desired_capabilities=dcap,proxy=proxy)
            return driver

        elif name.lower() == "chrome":
            chromedriver = r"E:\python_2\Scripts\chromedriver.exe"
            chome_options = webdriver.ChromeOptions()
            chome_options.add_argument(('--proxy-server=' + get_proxy_ip_port()))
            driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chome_options)
            # driver = webdriver.Chrome(executable_path=chromedriver)
            return driver

        elif name.lower() == "firfox":
            firfoxdriver = r"E:\python_2\Scripts\geckodriver.exe"
            proxy = Proxy(
                {
                    'proxyType': ProxyType.MANUAL,
                    'httpProxy': get_proxy_ip_port()
                }
            )
            driver = webdriver.Firefox(executable_path=firfoxdriver,proxy=proxy)
            return driver

# 测试代理IP接口
def get_proxy_ip_port():
    url = ''
    resp = requests.get(url)
    if resp.status_code == 200:
        a = re.search(r'(.+?),',resp.text.strip()).group(1)
        proxy_ip = 'http://' + a
        print u'从代理API获取代理IP: {}'.format(proxy_ip)
        return  proxy_ip



if __name__ == "__main__":
    # print crack_picture("http://static.geetest.com/pictures/gt/fc064fc73/fc064fc73.jpg", "http://static.geetest.com/pictures/gt/fc064fc73/bg/7ca363b09.jpg").pictures_recover()
    # gsxt("chrome").run()
    # gsxt("firfox").run()# 驱动版本低了，先用chrome
    # gsxt().run()
    # get_proxy_ip_port()
    q = gsxt()
    a=q.get_webdriver("chrome")
    a.set_page_load_timeout(30)
    a.set_script_timeout(30)
    a.get('http://www.gsxt.gov.cn/%7Bbo0rkJxd81LiFSgqRenFkRm4Nz0De9XHzkO_pEXO-5fPSMx8KTux6SDdN06MFLJUb1knCHZQNYqrop69rGOz9PgE34NK4VCL_qZDqVs9b5Lb1CdBCQNs5dSZbvoLyN-Rq0CiVydfLcPeYUuPLceUwg-1505384030282%7D')
    a.save_screenshot("2eeee.png")
    a.quit()
