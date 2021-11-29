import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

from datetime import timedelta, date

dayArray = []
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(30 * n)

start_date = date(2021, 1, 1)
end_date = date(2021, 11, 2)
for single_date in daterange(start_date, end_date):
    if(int(single_date.strftime("%Y%m%d")) > int(datetime.today().strftime("%Y%m%d"))):
        continue
    dayArray.append(single_date.strftime("%Y%m%d"))
print(dayArray)
titlePushArrays = []
for date in dayArray:
    for page in range(1, 20):
        if(page==3 or page==9):
            continue
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=pnt&date='+str(date)+'&tg='+str(page),headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')
        movies = soup.select('#old_content > table > tbody > tr')
        if(page >0 and page < 6):
            genre = '1'
        elif(page >= 6 and page <10):
            genre = '2'
        elif(page >=10 and page < 15):
            genre = '3'
        else:
            genre = '4'
        for movie in movies:
            a_tag = movie.select_one('td.title > div > a')
            if a_tag is not None:
                title = a_tag.text
                if title in titlePushArrays:
                    continue
                titlePushArrays.append(title)
                score = movie.select_one('td.point').text
                data = requests.get(
                    'https://search.naver.com/search.naver?where=nexearch&sm=tab_jum&query='+title+'정보', headers=headers)
                soup = BeautifulSoup(data.text, 'html.parser')
                try:
                    dec = soup.select_one('.intro_box').text
                    img_url = soup.select_one('div.detail_info > a > img')['src']
                    url = soup.select_one('div.detail_info > a')['href']
                except Exception as e:
                    continue
                doc = {'title': title,
                       'score': score,
                       'dec': dec,
                       'img_url': img_url,
                       'url': url,
                       'genre': genre}
                # print(title,score,doc,url,img_url,genre)
                db.teamproject4.insert_one(doc)
