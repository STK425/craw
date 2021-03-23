import time
from selenium import webdriver
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
#url='https://search.sina.com.cn/?q=%e5%b1%b1%e4%b8%9c%e5%a4%a7%e5%ad%a6&c=news&by=&from=channel&t=&sort=time&range=all'
url='https://search.sina.com.cn/?q=%e5%b1%b1%e4%b8%9c%e5%a4%a7%e5%ad%a6&c=news&from=channel&col=&range=all&source=&country=&size=10&stime=&etime=&time=&dpc=0&a=&ps=0&pf=0&page={}'
driver=webdriver.Chrome()
driver.get(url)
time.sleep(5)


# f=open("xinlang_urls.csv",'a',encoding='utf-8')
# ls=['链接','内容','时间戳']
# f.write(",".join(ls)+"\n")

href_list=[]
topic_list=[]
time_list=[]

# 获取不同页数的网页信息
def next_page(page):
    # 解决加载超时出错
    try:
        driver.get(url.format(str(page)))
        time.sleep(1)
    except TimeoutError:
        return print("TimeoutError")

# 获取网页信息
def get_urls():
    try:
        # 拉动滚轴使页面加载底端的页面元素
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(2)

        #page = driver.page_source
        #print(page)
        for context in driver.find_elements_by_class_name("box-result.clearfix"):

            url=[]
            a=context.find_element_by_tag_name("a")
            href=a.get_attribute("href") #网页链接
            topic=a.text  #标题

            time1=context.find_element_by_tag_name("span").text
            time2=" ".join(time1.split(" ")[1:]) #时间
            # url.append(href)
            # url.append(topic)
            # url.append(time2)
            # print(url)

            href_list.append(href)
            topic_list.append(topic)
            time_list.append(time2)
            #f.write(",".join(url) + "\n")

    except Exception as err:
        print("未爬取成功：", err)

def main():
    for i in range(1, 100):
        next_page(i)
        print("爬取第{}页内容".format(i))
        get_urls()

    #f.close()

    dframe = pd.DataFrame({'链接': href_list, '主题': topic_list, '时间': time_list})
    dframe.to_csv('xinlang_urls1.csv', index=False, sep=',', encoding='utf_8_sig')
    driver.quit()
    print("爬取新浪新闻完成！")

if __name__ == '__main__':
    main()


