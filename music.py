import requests
import urllib
from selenium import webdriver
import time
import os
import sys
import re
from selenium.webdriver.chrome.options import Options

def validateTitle(title):
    '''
        处理文件名中的特殊字符
    '''
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title

def download(music_name):
    url = "http://music.wandhi.com/?name={}".format(urllib.parse.quote(music_name))
    url += "&type={}"
    web_list = ["netease", "qq", "kugou", "kuwo", "xiami", "baidu", "1ting", "migu", "lizhi", "qingting", "ximalaya",
                "kg", "5singyc", "5singfc"]

    options = webdriver.ChromeOptions()

    # 设置Chrome无界面启动运行
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('lang=zh_CN.UTF-8')
    options.add_argument(
        "user-agent='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'")
    driver = webdriver.Chrome(options=options)

    is_download = False
    for net in web_list:
        # print(url.format(net))
        driver.get(url.format(net))
        btn = driver.find_element_by_id("j-src-btn")
        time.sleep(2)
        href = btn.get_attribute("href")
        j_name = btn.get_attribute("download")
        print(j_name)
        # print(href)
        if href is not None:
            reseponse = requests.get(href)
            targetPath = "/Users/david/Music/music_down/"
            if not os.path.exists(targetPath):
                os.makedirs(targetPath)
            with open( os.path.join(targetPath,validateTitle(j_name)), "wb") as f:
                f.write(reseponse.content)
                is_download = True
            break

    driver.quit()
    return is_download, j_name


if __name__ == '__main__':
    music_name = sys.argv[1]
    flag, name = download(music_name)
    if flag:
        print("歌曲:" + name + "  ---下载成功")
    else:
        print("歌曲:" + name + "  ---下载失败")
