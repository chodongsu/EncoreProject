from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests


def crawler(maxpage,query,s_date,e_date):
    s_from = s_date.replace(".","")
    e_to = e_date.replace(".","")
    page = 1
    maxpage_t =(int(maxpage)-1)*10+1 # 11= 2페이지 21=3페이지 31=4페이지 ...81=9페이지 , 91=10페이지, 101=11페이지
    f = open("C:/Users/Playdata/Documents/moonju/contents_text.csv", 'w', encoding='utf-8')
    while page < maxpage_t:
        print(page)
        url = "https://search.naver.com/search.naver?where=news&query=" + query + "&sort=0&ds=" + s_date + "&de=" + e_date + "&nso=so%3Ar%2Cp%3Afrom" + s_from + "to" + e_to + "%2Ca%3A&start=" + str(page)
        req = requests.get(url)
        print(url)
        cont = req.content
        soup = BeautifulSoup(cont, 'html.parser')
        #print(soup)
        for urls in soup.select("._sp_each_url"):
            try :
                #print(urls["href"])
                if urls["href"].startswith("https://news.naver.com"):
                    #print(urls["href"])
                    news_detail = get_news(f,urls["href"])
                        # pdate, pcompany, title, btext
            except Exception as e:
                print(e)
                continue
        page += 10
    f.close()


def get_news(f,url):

    #웹 드라이버
    driver = webdriver.Chrome('./chromedriver.exe')
    driver.implicitly_wait(5)
    driver.get(url)

    # 클린봇 옵션 해제 후 추출해주도록 한다.
    # cleanbot  = driver.find_element_by_css_selector('a.u_cbox_cleanbot_setbutton')
    # cleanbot.click()
    # time.sleep(1)
    # cleanbot_disable = driver.find_element_by_xpath("//input[@id='cleanbot_dialog_checkbox_cbox_module']")
    # cleanbot_disable.click()
    # time.sleep(1)
    # cleanbot_confirm = driver.find_element_by_css_selector('div.u_cbox_layer_cleanbot_extrabutton')
    # cleanbot_confirm.click()
    # time.sleep(1)

    #더보기 계속 클릭하기
    while True:
        try:
            btn_more = driver.find_element_by_css_selector('a.u_cbox_btn_more')
            btn_more.click()
            # time.sleep(1)
        except:
            break

    #날짜 추출
    news_date = driver.find_element_by_css_selector('span.t11')
    news_date = news_date.text[:11]

    #기사제목 추출
    article_head = driver.find_elements_by_css_selector('#articleTitle')
    # print("기사 제목 : " + article_head[0].text)

    #좋아요 수 추출
    like_count = driver.find_elements_by_css_selector('em.u_cbox_cnt_recomm ')

    # # 성비와 연령대 추출
    # per = driver.find_elements_by_css_selector('span.u_cbox_chart_per')
    # print("남자 성비 : " + per[0].text)
    # print("여자 성비 : " + per[1].text)
    # print("10대 : " + per[2].text)
    # print("20대 : " + per[3].text)
    # print("30대 : " + per[4].text)
    # print("40대 : " + per[5].text)
    # print("50대 : " + per[6].text)
    # print("60대 이상 : " + per[7].text)

    #댓글추출
    contents = driver.find_elements_by_css_selector('span.u_cbox_contents')
    # for content in contents:
    #     print(content.text)

    #좋아요 수 10개 미만 제거
    like = []
    cont = []
    for i in range(len(like_count)):
        if int(like_count[i].text) >= 10 :
            like.append(like_count[i].text)
            cont.append(contents[i].text)

    for i in range(0, len(like)):
        f.write("{}, {}, {}, {}\n".format(news_date, article_head[0].text, cont[i], like[i]))


def main():
    maxpage = "2"
    query = "공공 의대 확대"
    s_date = "2020.08.07"
    e_date = "2020.08.09"
    crawler(maxpage,query,s_date,e_date) #검색된 네이버뉴스의 기사내용을 크롤링합니다.

main()

