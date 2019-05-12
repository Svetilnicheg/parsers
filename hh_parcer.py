import requests
from bs4 import BeautifulSoup as bs
import unidecode





headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Safari/605.1.15'}

base_url = 'https://hh.ru/search/vacancy?area=1&search_period=3&text=python&page=0'

def hh_parcer(headers,base_url):
    jobs = []
    session = requests.session()
    request = session.get(base_url,headers=headers, timeout=5)
    if request.status_code == 200:
        soup = bs(request.content.decode('utf-8', 'ignore'), 'html.parser')
        divs = soup.find_all('div',attrs={'data-qa':'vacancy-serp__vacancy'})
        for div in divs:
            title = div.find('a', attrs={'data-qa':'vacancy-serp__vacancy-title'}).text
            href = div.find('a', attrs={'data-qa':'vacancy-serp__vacancy-title'})['href']
            salary=div.find('', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
            if salary is None:
                salary='no value'
            else:
                salary=salary.text
                salary=unidecode.unidecode(salary)

            jobs.append({
             'title':title,
             'url':href,
             'salary':salary
            })
        print(jobs)
    else:
        print('ERROOR')

hh_parcer(headers,base_url)


