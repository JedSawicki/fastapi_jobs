from typing import Optional

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


jobs = Scraper()

# jobs.no_fluff_jobs_worker()
