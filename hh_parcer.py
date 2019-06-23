import requests
from bs4 import BeautifulSoup as bs
import unidecode

headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15'}

base_url = 'https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&specialization=1&page=0'


def hh_parcer(headers, base_url):
    jobs = []
    urls_q = []
    urls = []
    urls.append(base_url)
    session = requests.session()
    request = session.get(base_url, headers=headers, timeout=5)

    if request.status_code == 200:
        request = session.get(base_url, headers=headers, timeout=5)
        soup = bs(request.content.decode('utf-8', 'ignore'), 'lxml')
        try:
            pagination = soup.find_all('a', attrs={'data-qa': 'pager-page'})
            count = int(pagination[-1].text)
            for i in range(count-99):
                url = f'https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&specialization=1&page={i}'
                if url not in urls:
                    urls.append(url)
        except:
            pass

    for url in urls:
        request = session.get(url, headers=headers, timeout=5)
        soup = bs(request.content.decode('utf-8', 'ignore'), 'lxml')
        divs = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
        for div in divs:
            href = div.find('a', attrs={'class':'bloko-link HH-LinkModifier', 'data-qa': 'vacancy-serp__vacancy-title'})['href']
            urls_q.append({
                'url': href
            })
        print(urls_q)

    for url_q in urls_q:
        #print(url_q["url"])
        request = session.get(url_q["url"], headers=headers, timeout=5)
        soup = bs(request.content.decode('utf-8', 'ignore'), 'lxml')
        #divs = soup.find_all('div', attr={'class': 'bloko-column bloko-column_xs-4 bloko-column_s-8 bloko-column_m-8 bloko-column_l-11 bloko-column_container'})

        if soup.find('h1', attrs={'class': 'header', 'data-qa': 'vacancy-title', 'itemprop': 'title'}) is None:
            title = 'no value'
        else:
            title = soup.find('h1', attrs={'class': 'header', 'data-qa': 'vacancy-title', 'itemprop': 'title'}).text
            title = unidecode.unidecode(title)

        if soup.find('p', attrs={'class': 'vacancy-salary'}) is None:
            salary = 'no value'
        else:
            salary = soup.find('p', attrs={'class': 'vacancy-salary'}).text
            salary = unidecode.unidecode(salary)

        if soup.find('span', attrs={'data-qa':'vacancy-experience'}) is None:
            experince = 'no value'
        else:
            experince = soup.find('span', attrs={'data-qa':'vacancy-experience'}).text
            experince = unidecode.unidecode(experince)

        if soup.find('meta', attrs={'itemprop':'employmentType'}) is None:
            Emp_mode = 'no value'
        else:
            Emp_mode = soup.find('meta', attrs={'itemprop':'employmentType'}).text
            Emp_mode = unidecode.unidecode(Emp_mode)

        if soup.find('p', attrs={'class': 'vacancy-creation-time'}) is None:
            Vacancy_publication_DT = 'no value'
        else:
            Vacancy_publication_DT = soup.find('p', attrs={'class': 'vacancy-creation-time'}).text
            Vacancy_publication_DT = unidecode.unidecode(Vacancy_publication_DT)


        jobs.append({'title': title,
                     'salary': salary,
                     'experince': experince,
                     'Emp_mode': Emp_mode,
                     'Vacancy_publication_DT': Vacancy_publication_DT,
                     'company_url': company_url
                     })
    else:
        print('ERROOR@<?!@#@!$?>')

    return jobs




    #return jobs

jobs_p=hh_parcer(headers, base_url)

print(jobs_p)
