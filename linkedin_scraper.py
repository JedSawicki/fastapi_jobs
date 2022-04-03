from typing import Optional
import time
import random
from requests_html import HTMLSession


class Scraper:
    def __init__(self):
        self.domain = f'https://pl.linkedin.com/jobs/'
        self.linkedin_items_list = []

    def linkedin_worker(self, key1: str, key2: Optional[str], key3: Optional[str]) -> object:
        keys_array = [key1, key2, key3]
        experimental_domain = f'https://pl.linkedin.com/jobs/search?keywords={key1}'
        for key in keys_array[1:]:
            if key is not None:
                experimental_domain = experimental_domain + f'%20{key}'
        print(experimental_domain)
        s = HTMLSession()
        r = s.get(str(experimental_domain))
        urllist = []

        jobs = r.html.find('section.two-pane-serp-page__results-list')

        for j in jobs:
            names = j.find('span.screen-reader-text')
            for name in names:
                # dictionary method
                index = names.index(name)
                # unpack href set
                (href, ) = j.find('a.base-card__full-link')[index].absolute_links
                item = {
                    'name': j.find('span.screen-reader-text')[index].text.strip(),
                    'company_name': j.find('h4.base-search-card__subtitle')[index].text.strip(),
                    'href': href,
                    'location': j.find('span.job-search-card__location')[index].text.strip(),
                    'offer_root': 'linkedIn'
                }
                urllist.append(item)

        return urllist

    def no_fluff_jobs_worker(self, technology: str, seniority: Optional[str], second_tech: Optional[str], page: Optional[int] = 0) -> object:
        # url = f'https://nofluffjobs.com/pl/praca-it/python?criteria=seniority%3Djunior&page=2'
        url = f'https://nofluffjobs.com/pl/praca-it/{technology}?page={page}'
        if seniority is not None:
            url = f'https://nofluffjobs.com/pl/praca-it/{technology}?criteria=seniority%3D{seniority}&page={page}'
        if second_tech is not None:
            url = f'https://nofluffjobs.com/pl/praca-it/{technology}?criteria=seniority%3D{seniority}%20requirement%3D{second_tech}&page={page}'
        if second_tech is not None and seniority is None:
            url = f'https://nofluffjobs.com/pl/praca-it/{technology}?page={page}&criteria=requirement%3D{second_tech}'
                    
        print(url)
        s = HTMLSession()
        r = s.get(str(url))
        urllist = []
        try:
            jobs = r.html.find('div.list-container.ng-star-inserted')

            for j in jobs:
                # a for hrefs
                items = j.find('a')
                # elements for text
                for idx, elem in enumerate(items):
                    name = elem.text.split('\n')
                    if idx % 2 == 0:
                        href = 'https://nofluffjobs.com' + elem.attrs['href']
                        item = {'name': name[0], 'company_name': name[1], 'href': href, 'offer_root': 'NoFluffJobs'}
                        urllist.append(item)
        except IndexError:
            print('No text found')
        return urllist
    
    def indeed_jobs_worker(self, key1: str, key2: Optional[str], key3: Optional[str]) -> object:
        keys_array = [key1, key2, key3]
        experimental_domain = f'https://pl.indeed.com/jobs?q={key1}'
        for key in keys_array[1:]:
            if key is not None:
                experimental_domain = experimental_domain + f'%20{key}'
        print(experimental_domain)
        s = HTMLSession()
        r = s.get(str(experimental_domain))
        urllist = []

        try:
            jobs = r.html.find('div.mosaic-zone')

            for j in jobs:
                # a for hrefs
                items = j.find('a.tapItem')
                # elements for text
                for idx, elem in enumerate(items):
                    item = {'name': j.find('h2.jobTitle')[idx].text.strip(), 
                            'company_name': j.find('span.companyName')[idx].text.strip(), 
                            'href': 'https://pl.indeed.com' + elem.attrs['href'], 
                            'location': j.find('div.companyLocation')[idx].text.strip(),
                            'offer_root': 'Indeed'}
                    urllist.append(item)
        except IndexError:
            print('index error!')
        return urllist

    def jooble_jobs_worker(self, key1: str, key2: Optional[str], key3: Optional[str]) -> object:
        keys_array = [key1, key2, key3]
        experimental_domain = f'https://pl.jooble.org/SearchResult?ukw={key1}'
        for key in keys_array[1:]:
            if key is not None:
                experimental_domain = experimental_domain + f'%20{key}'
        print(experimental_domain)
        s = HTMLSession()
        r = s.get(str(experimental_domain))
        urllist = []

        try:
            jobs = r.html.find('div._5d258')

            for j in jobs:
                # a for hrefs
                items = j.find('article')
                # elements for text
                for idx, elem in enumerate(items):
                    (href, ) = j.find('a')[idx].absolute_links
                    item = { 'href': href, 
                            'name': j.find('a')[idx].text.strip(),
                            'company_name': j.find('div.efaa8')[idx].text.strip(),
                            'location': j.find('div._88a24')[idx].text.strip(),
                            'offer_root': 'Jooble'}
                    urllist.append(item)
        except IndexError:
            print('index error!')
            
        return urllist
    
    def grand_scraper(self, technology: str, seniority: Optional[str], second_tech: Optional[str]) -> object:
        print("Scraping...")
        start = time.time()
        linkedin_offers = self.linkedin_worker(technology, seniority, second_tech)
        nofluff_offers = self.no_fluff_jobs_worker(technology, seniority, second_tech)
        indeed_offers = self.indeed_jobs_worker(technology, seniority, second_tech)
        jooble_offers = self.jooble_jobs_worker(technology, seniority, second_tech)
        end = time.time()
        offers = (indeed_offers + nofluff_offers + linkedin_offers + jooble_offers)
        random.shuffle(offers)
        print(f'Scrap time: {end -start}')
        return offers

# jobs = Scraper()

# jobs.jooble_jobs_worker()
