from requests_html import HTMLSession


class Scraper:
    def __init__(self, tags):
        self.tag = tags
        self.links = f'https://pl.linkedin.com/jobs/{self.tag}'

    def linkedin_worker(self):
        s = HTMLSession()
        r = s.get(self.links)
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


# jobs = Scraper('junior-python-jobs')
#
# jobs.linkedin_worker()
