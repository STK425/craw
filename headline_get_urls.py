# -*- coding = utf-8 -*-
# @Time : 2020/10/12 21:08
# @Author : 冰阔落
# @File : txt.py
# @Software : PyCharm
# encoding: utf-8
# time: 2020/3/23 16:11

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from pyquery import PyQuery as pq
import pandas as pd
import re

# 让网页不加载图片
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2}
chrome_options.add_experimental_option("prefs",prefs)

browser = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(browser, 10)

urls_list = []
title_list = []
time_list = []
urls = 'https://www.toutiao.com/search/?keyword=%E5%B1%B1%E4%B8%9C%E5%A4%A7%E5%AD%A6'

# 根据page翻页
def search():
    # 解决加载超时出错
    try:
        browser.get(urls)
        sleep(1)
        # 等待加载出页面信息加载出来
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div > div.y-box.container >'
                                                             ' div.y-left.index-middle > div.feedBox > div > div'))
        )
    except TimeoutError:
        return search()


# 获取网页信息
def get_urls():
    try:
        # 拉动滚轴使页面加载底端的页面元素
        for i in range(8):
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            sleep(2)
        # 等待最后一个商品加载出来
        # 获取网页源码
        html = browser.page_source
        doc = pq(html)
        # id是#
        items = doc('.articleCard').items()
        # enumerate()枚举计算，记录新闻的链接
        for index, i in enumerate(items):
            urls_list.append('https://www.toutiao.com' + i('.link.title').attr('href'))
            title_list.append(i('.J_title').text())
            time_list.append((i('.lbtn').text()))
    except:
        get_urls()



def main():
    search()
    get_urls()
    dframe = pd.DataFrame({'网址': urls_list, '标题':title_list, '时间戳': time_list})
    dframe.to_csv('headline_urls.csv', index=False, sep=',', encoding='utf_8_sig')


if __name__ == '__main__':
    main()
