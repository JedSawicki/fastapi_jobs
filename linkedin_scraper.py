from typing import Optional

from requests_html import HTMLSession


class Scraper:
    def __init__(self):
        self.domain = f'https://pl.linkedin.com/jobs/'
        self.linkedin_items_list = []

    def custom_linkedin_worker(self, key1: str, key2: Optional[str], key3: Optional[str]) -> object:
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
                item = {
                    'name': j.find('span.screen-reader-text')[index].text.strip(),
                    'href': j.find('a.base-card__full-link')[index].absolute_links,
                    'company_name': j.find('h4.base-search-card__subtitle')[index].text.strip(),
                    'location': j.find('span.job-search-card__location')[index].text.strip()
                }
                urllist.append(item)

        print(urllist)
        return urllist

    def no_fluff_jobs_worker(self) -> object:
        url = f'https://nofluffjobs.com/pl/praca-it/python?criteria=seniority%3Djunior&page=2'
        s = HTMLSession()
        r = s.get(str(url))
        urllist = []

        jobs = r.html.find('div.list-container.ng-star-inserted')
        print(jobs)

        for j in jobs:
            # a for hrefs
            items = j.find('a')
            # elements for text
            names = j.find('nfj-posting-item-title.align-items-lg-center')
            # print(hrefs)

            for name in names:
                index = names.index(name)
                item = {'name': names[index].text, 'href': items[index].absolute_links}
                urllist.append(item)





        return urllist


jobs = Scraper()

jobs.no_fluff_jobs_worker()
