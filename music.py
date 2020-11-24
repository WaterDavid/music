import requests
import urllib
from selenium import webdriver
import time
import os
import sys
import re
import random
from selenium.webdriver.chrome.options import Options
from lxml import etree
import threading


def validateTitle(title):
    '''
        处理文件名中的特殊字符
    '''
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title


class downLoadMusic():

    def __init__(self):

        self.web_list = ["netease", "qq", "kugou"]

        self.options = webdriver.ChromeOptions()

        # 设置Chrome无界面启动运行
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('lang=zh_CN.UTF-8')
        self.options.add_argument(
            "user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'")
        self.driver = webdriver.Chrome(options=self.options)

    def download(self, music_name):
        print(music_name)
        for net in self.web_list:
            url = "http://www.youtap.xin/?name={}&type={}".format(urllib.parse.quote(music_name), net)
            try:
                is_download, j_name = self.down(url)
                if is_download:
                    print("歌曲:" + music_name + "-->" + j_name + "  ---下载成功")
                    break
                else:
                    print("歌曲:" + music_name + "-->" + net + "  ---下载失败")
            except Exception as e:
                print("error:", e)
        return None

    def save_file(self, href, j_name):
        reseponse = requests.get(href)
        targetPath = "../music_down/"
        if not os.path.exists(targetPath):
            os.makedirs(targetPath)
        with open(os.path.join(targetPath, validateTitle(j_name)), "wb") as f:
            f.write(reseponse.content)

    def down(self, url):
        is_download = False
        for i in range(3):
            # print(url.format(net))
            self.driver.get(url)
            # if i > 0:
            #     print(url + "重试第" + str(i) + "次")
            count = 0
            time.sleep(2*(i+1))
            while True:
                btn = self.driver.find_element_by_id("j-submit")
                if btn.text != '正在搜索相关音乐...' or count >= 7:
                    break
                count += 1
                time.sleep(count)

            btn = self.driver.find_element_by_id("j-src-btn")
            href = btn.get_attribute("href")
            j_name = btn.get_attribute("download")

            if href is not None:
                print('name:', j_name)
                print('href', href)
                threading.Thread(target=self.save_file, args=(href, j_name,)).start()
                is_download = True
                break
            else:
                continue

        return is_download, j_name

    def quit(self):
        self.driver.quit()
        self.driver = webdriver.Chrome(options=self.options)


def func_down_load(names):
    ms = downLoadMusic()
    for i in names:
        # print(i)
        ms.download(i)

def loadFromHtml():
    html = etree.parse('./html.html', etree.HTMLParser())
    result = etree.tostring(html)
    # print(result.decode('UTF-8'))
    result = html.xpath('//b/@title')

    items = []
    for item in result:
        if not item.isspace():
            items.append(item.strip())
        if len(items) >= len(result)//10:
            threading.Thread(target=func_down_load, args=(items,)).start()
            items = []
    if items:
        threading.Thread(target=func_down_load, args=(items,)).start()

def loadFromText():
    with open('./names.txt','r',encoding='utf-8') as f:
        result = f.readlines()

    items = []
    for item in result:
        if not item.isspace():
            items.append(item.strip())
        if len(items) >= len(result)//10:
            threading.Thread(target=func_down_load, args=(items,)).start()
            # print(len(items), items)
            # items = []
    if items:
        threading.Thread(target=func_down_load, args=(items,)).start()
        # print(len(items),items)
if __name__ == '__main__':
    pass
    # loadFromHtml()
    # loadFromText()
