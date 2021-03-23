import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import warnings
import pandas as pd
warnings.filterwarnings("ignore")

urls='https://weibo.com/1901sdu?is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page={}#feedtop'
driver=webdriver.Chrome()
#driver = webdriver.Firefox()
#driver.get(url)
#time.sleep(5)
#wait = WebDriverWait(driver, 10)

time_list=[]
topic_list=[]
context_list=[]

# 获取page翻页，不同网页内容
def next_page(page):
    # 解决加载超时出错
    try:
        driver.get(urls.format(str(page)))
        #driver.get(urls)
        time.sleep(5)
        # 等待加载出底部页面信息加载出来
        # total = wait.until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, '#page > div'))
        # )
        for i in range(0,3):
            # 拉动滚轴使页面加载底端的页面元素
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(2)

    except TimeoutError:
        return print("TimeoutError")



# 获取网页信息
def get_infos():
    try:
        main=driver.find_element_by_class_name("WB_frame_c")
        #print(main)
        #page = driver.page_source
        #print(page)

        for wb in main.find_elements_by_class_name("WB_detail"):
            try:
               info=[]
               time1=wb.find_element_by_class_name("WB_from.S_txt2").find_element_by_tag_name("a").text #时间
               all_context=wb.find_element_by_class_name("WB_text.W_f14")
               topic=all_context.find_element_by_tag_name("a").text  #主题
               context=all_context.text.replace(",","--").split("#")[2][1:]  #内容

               time_list.append(time1)
               topic_list.append(topic)
               context_list.append(context)

               info.append(time1)
               info.append(topic)
               info.append(context)

               print(info)

            except Exception as err:
                print("未爬取成功：", err)
            else:
                pass

    except Exception as err:
        print("未爬取成功：",err)


def main():
    for i in range(1, 32):
       next_page(i)
       print("页数"+str(i))
       get_infos()

    dframe = pd.DataFrame({'时间': time_list, '主题': topic_list, '内容': context_list})
    dframe.to_csv('weibo_urls1.csv', index=False, sep=',', encoding='utf_8_sig')
    #f.close()
    driver.quit()
    print("爬取微博完成")


if __name__ == '__main__':
    main()