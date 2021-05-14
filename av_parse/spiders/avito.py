import scrapy
import av_parse.spiders.xpaths as xp
from av_parse.items import Apartment, ApartmentLoader


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/chita']

    def _get_follow(self, response, callback, urls=None, xpath=None):
        if xpath is not None:
            urls = response.xpath(xpath)
        for url in urls:
            yield response.follow(url, callback=callback)

    def parse(self, response, *args, **kwargs):
        yield from self._get_follow(response, self.parse, xpath=xp.AVITO_START_PAGE_SELECTORS['apartments_cat'])
        yield from self._get_follow(response, self.parse, xpath=xp.AVITO_START_PAGE_SELECTORS['apartment_list'])
        yield from self._get_follow(response, self.advert_parse, xpath=xp.AVITO_START_PAGE_SELECTORS['apartment_page'])
        yield from self._get_follow(response, self.advert_parse, xpath=xp.AVITO_START_PAGE_SELECTORS['pagination'])

    def advert_parse(self, response):
        apartment_loader = ApartmentLoader(item=Apartment(), response=response)
        apartment_loader.add_value('url', response.url)
        for field, xpath in xp.AVITO_FLAT_ITEM_SELECTORS.items():
            apartment_loader.add_xpath(field, xpath)
        yield apartment_loader.load_item()
