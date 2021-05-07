import scrapy
from pymongo import MongoClient
import re


class AutoyoulaSpider(scrapy.Spider):
    name = "autoyoula"
    allowed_domains = ["auto.youla.ru"]
    start_urls = ["https://auto.youla.ru/"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mdb_collection = MongoClient()["autoyoula_parse"]["cars"]

    def _get_follow(self, response, selector_str, callback):
        for itm in response.css(selector_str):
            url = itm.attrib["href"]
            yield response.follow(url, callback=callback)

    def parse(self, response, *args, **kwargs):
        yield from self._get_follow(
            response,
            ".TransportMainFilters_brandsList__2tIkv .ColumnItemList_column__5gjdt a.blackLink",
            self.brand_parse,
        )

    def brand_parse(self, response):
        yield from self._get_follow(
            response, ".Paginator_block__2XAPy a.Paginator_button__u1e7D", self.brand_parse
        )
        yield from self._get_follow(
            response,
            "article.SerpSnippet_snippet__3O1t2 a.SerpSnippet_name__3F7Yu.blackLink",
            self.car_parse,
        )

    def car_parse(self, response):
        data = {
            "url": response.url,
            "title": response.css(".AdvertCard_advertTitle__1S1Ak::text").extract_first(),
            "photos": [itm.attrib.get("src") for itm in response.css("figure.PhotoGallery_photo__36e_r img")],
            "specs": [
                {
                    "name": itm.css(".AdvertSpecs_label__2JHnS::text").extract_first(),
                    "value": itm.css(".AdvertSpecs_data__xK2Qx::text").extract_first()
                             or itm.css(".AdvertSpecs_data__xK2Qx a::text").extract_first()
                }
                for itm in response.css("div.AdvertCard_specs__2FEHc .AdvertSpecs_row__ljPcX")
            ],
            "description": response.css(".AdvertCard_descriptionInner__KnuRi::text").extract_first(),
            "author_url": AutoyoulaSpider.get_author_url(response)
        }
        self.mdb_collection.insert_one(data)

    @staticmethod
    def get_author_url(response):
        marker = "window.transitState = decodeURIComponent"
        for script in response.css("script"):
            try:
                if marker in script.css("::text").extract_first():
                    re_pattern = re.compile(r"youlaId%22%2C%22([a-zA-Z|\d]+)%22%2C%22avatar")
                    result = re.findall(re_pattern, script.css("::text").extract_first())
                    return (
                        response.urljoin(f"/user/{result[0]}").replace("auto.", "", 1)
                        if result
                        else None
                    )
            except TypeError:
                pass
