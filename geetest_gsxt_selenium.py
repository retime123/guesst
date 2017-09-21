#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/3 0003 14:01
# @Author  : Lee
# @Site    : 
# @File    : geetest_gsxt_selenium.py
# @Software: PyCharm Community Edition
import requests
import re
import StringIO
from PIL import Image
import random
import math
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup


class crack_picture(object):
    def __init__(self, img_url1, img_url2):
        self.img1, self.img2 = self.picture_get(img_url1, img_url2)

    def picture_get(self, img_url1, img_url2):
        hd = {"Host": "static.geetest.com",
              "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
        img1 = StringIO.StringIO(self.repeat(img_url1, hd).content)
        img2 = StringIO.StringIO(self.repeat(img_url2, hd).content)
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
        return self.darbra_track(xpos)

    def picture_recover(self, img, name):
        a = [39, 38, 48, 49, 41, 40, 46, 47, 35, 34, 50, 51, 33, 32, 28, 29, 27, 26, 36, 37, 31, 30, 44, 45, 43, 42, 12,
             13, 23, 22, 14, 15, 21, 20, 8, 9, 25, 24, 6, 7, 3, 2, 0, 1, 11, 10, 4, 5, 19, 18, 16, 17]
        im = Image.open(img)
        im_new = Image.new("RGB", (260, 116))
        for row in range(2):
            for column in range(26):
                right = a[row * 26 + column] % 26 * 12 + 1
                if a[row * 26 + column] > 25:
                    down = 58
                else:
                    down = 0
                for w in range(10):
                    for h in range(58):
                        ht = 58 * row + h
                        wd = 10 * column + w
                        im_new.putpixel((wd, ht), im.getpixel((w + right, h + down)))
        im_new.save(name)
        return im_new

    def darbra_track(self, distance):
        t = 1.0 / distance
        list = [[0, 0.5, t], ]
        print(distance)
        for x in range(0, distance-1, 2):
            list.append([2, random.random()*5, t])
        return distance
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
        self.br = self.get_webdriver(br_name)
        self.br.set_window_size(width=800, height=600)
        self.wait = WebDriverWait(self.br, 20, 1.0)
        self.br.set_page_load_timeout(10)
        self.br.set_script_timeout(10)


    def input_params(self, name):
        self.br.get("http://www.gsxt.gov.cn/index")
        print (self.br.page_source)
        element = self.wait_for(By.ID, "keyword")
        element.send_keys(name)
        time.sleep(1.1)
        element = self.wait_for(By.ID, "btn_query")
        element.click()
        time.sleep(1.1)

    def drag_pic(self):
        return (self.find_img_url(self.wait_for(By.CLASS_NAME, "gt_cut_fullbg_slice")),
                self.find_img_url(self.wait_for(By.CLASS_NAME, "gt_cut_bg_slice")))

    def wait_for(self, by1, by2):
        return self.wait.until(EC.presence_of_element_located((by1, by2)))

    def find_img_url(self, element):
        try:
            return re.findall('url\("(.*?)"\)', element.get_attribute('style'))[0].replace("webp", "jpg")
        except:
            return re.findall('url\((.*?)\)', element.get_attribute('style'))[0].replace("webp", "jpg")

    def emulate_track(self, tracks):
        element = self.br.find_element_by_class_name("gt_slider_knob")
        action = ActionChains(self.br)
        action.click_and_hold(on_element=element).perform()
        # ActionChains(self.br).click_and_hold(on_element=element).perform()
        # for x, y, t in tracks:
        #     print x, y, t
        #     ActionChains(self.br).move_to_element_with_offset(
        #         to_element=element,
        #         xoffset=x + 22,
        #         yoffset=y + 22).perform()
        #     ActionChains(self.br).click_and_hold().perform()
        #     time.sleep(t)
        # time.sleep(0.24)
        # ActionChains(self.br).release(on_element=element).perform()
        print (tracks)
        if not tracks == 0:
            for i in range(tracks):
                action.move_by_offset(1, 0)
                print (1.2 / tracks)
                time.sleep(1.2 / tracks)
        action.release(on_element=element).perform()
        time.sleep(0.8)
        element = self.wait_for(By.CLASS_NAME, "gt_info_text")
        ans = element.text.encode("utf-8")
        print (ans)
        return ans

    def run(self):
        for i in [ u'交通银行', u'中国银行']:
            self.hack_geetest(i)
            time.sleep(1)
        self.quit_webdriver()

    def hack_geetest(self, company=u"招商银行"):
        flag = True
        self.input_params(company)
        while flag:
            img_url1, img_url2 = self.drag_pic()
            tracks = crack_picture(img_url1, img_url2).pictures_recover()
            tsb = self.emulate_track(tracks)
            if '通过' in tsb:
                time.sleep(1)
                soup = BeautifulSoup(self.br.page_source, 'html.parser')
                print(soup.select(".search_result"))
                for sp in soup.find_all("a", attrs={"class": "search_list_item"}):
                    print (re.sub("\s+", "", sp.get_text().encode("utf-8")))
                print (soup.select("form > input[type='hidden']"))
                print (soup.select("form > a"))

                    # print sp.get_text()
                break
            elif '吃' in tsb:
                time.sleep(5)
            else:
                self.input_params(company)

    def quit_webdriver(self):
        self.br.quit()

    def get_webdriver(self, name):
        if name.lower() == "phantomjs":
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.userAgent"] = (
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3080.5 Safari/537.36")
            # return webdriver.PhantomJS(desired_capabilities=dcap)
            return webdriver.PhantomJS(executable_path=r"D:\dirver\phantomjs-2.1.1-windows\bin\phantomjs.exe")

        elif name.lower() == "chrome":
            return webdriver.Chrome()


if __name__ == "__main__":
    # print crack_picture("http://static.geetest.com/pictures/gt/fc064fc73/fc064fc73.jpg", "http://static.geetest.com/pictures/gt/fc064fc73/bg/7ca363b09.jpg").pictures_recover()
    gsxt("chrome").run()
