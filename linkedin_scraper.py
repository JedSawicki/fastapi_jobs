from requests_html import HTMLSession


class Scraper:
    def __init__(self):
        self.domain = f'https://pl.linkedin.com/jobs/'


    def linkedin_worker(self, tag: str):
        s = HTMLSession()
        r = s.get(str(self.domain + tag))
        # r = s.get(str(self.experimental_domain))
        print(r.status_code)
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

    def custom_linkedin_worker(self, key1: str, key2: str, key3: str):
        s = HTMLSession()
        experimental_domain = f'https://pl.linkedin.com/jobs/search?keywords={key1}%20{key2}%20{key3}'
        r = s.get(str(experimental_domain))
        print(r.status_code)
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


jobs = Scraper()

jobs.linkedin_worker('junior-python-jobs')
