from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
import pandas


def crawler(maxpage,query):
    page = 1
    f = open("C:/Users/Playdata/Documents/moonju/daum_crawling.csv", 'w', encoding='utf-8')
    while page <= int(maxpage):
        url = "https://search.daum.net/search?w=news&sort=recency&q=" + query + "&cluster=n&DA=STC&dc=STC&pg=1&r=1&p=" + str(page) + "&rc=1&at=more&sd=&ed=&period=1"
        req = requests.get(url)
        #print(req)
        cont = req.content
        soup = BeautifulSoup(cont, 'html.parser')
        #print(soup)
        for urls in soup.select("a.f_nb"):
            try :
                #print(urls["href"])
                if urls["href"].startswith("http://v.media.daum.net"):
                    #print(urls["href"])
                    news_detail = get_news(f,urls["href"])
                        # pdate, pcompany, title, btext
            except Exception as e:
                print(e)
                continue
        page += 1
    f.close()


def get_news(f,url):

    #웹 드라이버
    driver = webdriver.Chrome('./chromedriver.exe')
    driver.implicitly_wait(3)
    driver.get(url)

    #더보기 계속 클릭하기
    while True:
        try:
            btn_more = driver.find_element_by_css_selector('div.alex_more > .link_fold')
            btn_more.click()
            time.sleep(1)
        except:
            break

    #날짜 추출
    news_date = driver.find_element_by_css_selector('.num_date')
    news_date = news_date.text[:11]
    # print(news_date)

    #기사제목 추출
    article_head = driver.find_element_by_css_selector('.tit_view')
    print("기사 제목 : " + article_head.text)

    #좋아요 수 추출
    like_count = driver.find_elements_by_css_selector('div.box_reply > span.comment_recomm > button.btn_recomm > span.num_txt')
    # for like in like_count :
        # print(like.text)

    #댓글추출
    contents = driver.find_elements_by_css_selector('.desc_txt')
    # for content in contents:
        # print(content.text)

    #좋아요 수 10개 미만 제거
    like = []
    cont = []
    for i in range(len(like_count)):
        if int(like_count[i].text) >= 10 :
            like.append(like_count[i].text)
            cont.append(contents[i].text)

    for i in range(0, len(like)):
        f.write(news_date + "," + article_head.text + "," + cont[i] + "," + like[i] + "\n")

def main():
    maxpage = "2"
    query = "공공 의대 확대"
    crawler(maxpage,query) #검색된 네이버뉴스의 기사내용을 크롤링합니다.

main()

