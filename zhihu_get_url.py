import time
from selenium import webdriver
import warnings
warnings.filterwarnings("ignore")


url='https://weibo.com/1901sdu?is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page=2#feedtop'
driver=webdriver.Chrome()
driver.get(url)
time.sleep(5)
#print("获取网页")

# 获取搜索结果第
# page = driver.page_source
#page = driver.page_source
#print(page)#1页商品详情页面的超链接

#mainpage=driver.find_element_by_class_name("TopicIndex-contentMain").get_attribute('innerHTML')
#print(mainpage)

f=open("zhihu_urls.csv",'a',encoding='utf-8')
ls=['链接','题目','话题']
f.write(",".join(ls)+"\n")

for topicmodule in driver.find_element_by_class_name("TopicIndex-contentMain").find_elements_by_class_name("TopicIndexModule"):

    topic=topicmodule.find_element_by_class_name("TopicIndexModule-title").text

    for item in topicmodule.find_elements_by_class_name("TopicIndexModule-item"):
        topic_info=[]
        href=item.find_element_by_tag_name("a").get_attribute("href")
        title=item.find_element_by_tag_name("a").text

        topic_info.append(href)
        topic_info.append(title)
        topic_info.append(topic)
        print(topic_info)

        f.write(",".join(topic_info) + "\n")

f.close()
driver.quit()
print("爬取知乎话题成功")




