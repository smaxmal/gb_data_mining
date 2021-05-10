import scrapy
import hh_parse.spiders.xpaths as xp
from hh_parse.items import VacancyItem, VacancyLoader, EmployerItem, EmployerLoader


class HHSpider(scrapy.Spider):
    name = 'hh'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113']

    def _get_follow(self, response, callback, urls=None, xpath=None):
        if xpath is not None:
            urls = response.xpath(xpath)
        for url in urls:
            yield response.follow(url, callback=callback)

    def parse(self, response, *args, **kwargs):
        yield from self._get_follow(response, self.parse, xpath=xp.HH_START_PAGE_SELECTORS['page'])
        yield from self._get_follow(response, self.vacancy_parse, xpath=xp.HH_START_PAGE_SELECTORS['vacancy'])

    def vacancy_parse(self, response):
        vacancy_loader = VacancyLoader(item=VacancyItem(), response=response)
        vacancy_loader.add_value('url', response.url)
        for field, xpath in xp.HH_VACANCY_ITEM_SELECTORS.items():
            vacancy_loader.add_xpath(field, xpath)
        vacancy = vacancy_loader.load_item()
        yield vacancy

        yield from self._get_follow(response, self.employer_parse, urls=[vacancy['employer_url']])

    def employer_parse(self, response):
        employer_loader = EmployerLoader(item=EmployerItem(), response=response)
        employer_loader.add_value('url', response.url)
        for field, xpath in xp.HH_EMPLOYER_ITEM_SELECTORS.items():
            employer_loader.add_xpath(field, xpath)

        yield employer_loader.load_item()
        yield from self._get_follow(response, self.parse, xpath=xp.HH_START_PAGE_SELECTORS['employer_vacancies'])
