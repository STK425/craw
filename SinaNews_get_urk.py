# -*- coding = utf-8 -*-
# @Time : 2021/3/15 21:35
# @Author : Mrz_orz
# @File : tieba_get_url.py
# @Software : Visual Studio

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
urls = 'https://search.sina.com.cn/?q=%e5%b1%b1%e4%b8%9c%e5%a4%a7%e5%ad%a6&c=news&from=channel&col=&range=all&source=&country=&size=10&stime=&etime=&time=&dpc=0&a=&ps=0&pf=0&page='

# 根据page翻页
def next_page(page):
    # 解决加载超时出错
    try:
        browser.get(urls+str(page))
        sleep(2)
        # 等待加载出底部页面信息加载出来
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
        items = doc('.box-result').items()
        # enumerate()枚举计算，记录新闻的链接
        for index, i in enumerate(items):
            urls_list.append(i(' a').attr('href'))
            if len(i(' a').text()) == 0:
                title_list.append(" ")
            else:
                title_list.append(i(' a').text())
            time_list.append((i('.fgray_time').text())[-20:])
    except:
        get_urls()


def main():
    for i in range(1, 21):
        next_page(i)
        get_urls()
    dframe = pd.DataFrame({'网址': urls_list, '标题':title_list, '时间戳': time_list})
    dframe.to_csv('SinaNews_urls.csv', index=False, sep=',', encoding='utf_8_sig')


if __name__ == '__main__':
    main()



