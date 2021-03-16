# -*- coding = utf-8 -*-
# @Time : 2021/3/8 21:35
# @Author : 冰阔落
# @File : baidu_get_url.py
# @Software : PyCharm

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
urls = 'https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&rsv_dl=ns_pc&word=%E5%B1%B1%E4%B8%9C%E5%A4%A7%E5%AD%A6&x_bfe_' \
       'rqs=03E80000001&x_bfe_tjscore=0.100000&tngroupname=organic_news&newVideo=12&pn='

# 根据page翻页
def next_page(page):
    # 解决加载超时出错
    try:
        browser.get(urls+str(page))
        sleep(1)
        # 等待加载出底部页面信息加载出来
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#page > div'))
        )
    except TimeoutError:
        return next_page()


# 获取网页信息
def get_urls():
    try:
        # 拉动滚轴使页面加载底端的页面元素
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        sleep(2)
        # 等待最后一个商品加载出来
        # 获取网页源码
        html = browser.page_source
        doc = pq(html)
        # id是#
        items = doc('.news-title_1YtI1').items()
        # enumerate()枚举计算，记录新闻的链接
        for index, i in enumerate(items):
            urls_list.append(i(' a').attr('href'))
            if len(i(' a').text()) == 0:
                title_list.append(" ")
            else:
                title_list.append(i(' a').text())
        items = doc('.news-source').items()
        # enumerate()枚举计算，记录新闻的时间戳
        for index, i in enumerate(items):
            time_list.append(i('.c-color-gray2').text())
    except:
        get_urls()


#def main():
#    for i in range(0, 18):
#        next_page(i * 10)
#        get_urls()
#    dframe = pd.DataFrame({'网址': urls_list, '标题':title_list, '时间戳': time_list})
#    dframe.to_csv('baidu_urls.csv', index=False, sep=',', encoding='utf_8_sig')


#if __name__ == '__main__':
#    main()
