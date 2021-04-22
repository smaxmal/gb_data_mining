"""
Источник: https://5ka.ru/special_offers/
Задача организовать сбор данных,
необходимо иметь метод сохранения данных в .json файлы
результат: Данные скачиваются с источника, при вызове метода/функции сохранения в файл скачанные данные сохраняются
в Json вайлы, для каждой категории товаров должен быть создан отдельный файл
и содержать товары исключительно соответсвующие данной категории.
пример структуры данных для файла:
нейминг ключей можно делать отличным от примера

{
"name": "имя категории",
"code": "Код соответсвующий категории (используется в запросах)",
"products": [{PRODUCT}, {PRODUCT}........] # список словарей товаров соответсвующих данной категории
}
"""

import json
import time
from pathlib import Path
import requests


class NumAttemptsExceeded(Exception):
    def __init__(self):
        super().__init__(f'Maximum number of attempts to get a valid response exceeded')


class BaseParser:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
    }
    params = {}

    def __init__(self, start_url: str, dir: str = 'Response'):
        self.star_url = start_url
        self.save_path = self._get_save_path(dir)

    def _get_response(self, url: str = None, max_attempts: int = 3, *args, **kwargs):
        if url is None:
            url = self.star_url

        attempt = 0
        while attempt < max_attempts:
            response = requests.get(url, *args, **kwargs)
            if response.status_code == 200:
                return response
            time.sleep(3)
            attempt += 1
        raise NumAttemptsExceeded

    def _save(self, data: dict, file_path):
        file_path.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')

    def _get_save_path(self, dir_name):
        save_path = Path(__file__).parent.joinpath(dir_name)
        if not save_path.exists():
            save_path.mkdir()
        return save_path


class Parse_5ka(BaseParser):

    def __init__(self, start_url: str, dir: str = 'Response'):
        super().__init__(start_url, dir)

    def _parse_categories(self):
        cat_url = "https://5ka.ru/api/v2/categories/"
        response = self._get_response(cat_url, headers=self.headers)
        return response.json()

    def _parse_products(self, url: str):
        page = 1
        self.params['page'] = str(page)
        while page:
            time.sleep(0.1)
            print(f'category: {self.params.get("categories")}, page: {page}\n')
            response = self._get_response(url, headers=self.headers, params=self.params)
            data = response.json()
            if data["next"] is not None:
                page += 1
                self.params['page'] = str(page)
            else:
                page = 0

            for product in data["results"]:
                yield product

    def run(self):
        try:
            cat_dict = {}
            categories = self._parse_categories()
            for cat in categories:
                cat_dict['name'] = cat['parent_group_name']
                cat_dict['code'] = cat['parent_group_code']
                cat_dict['products'] = []
                self.params['categories'] = cat_dict['code']

                for product in self._parse_products(self.star_url):
                    cat_dict['products'].append(product)

                if len(cat_dict['products']) > 0:
                    cat_file = self.save_path.joinpath(f"{cat_dict['code']}.json")
                    self._save(cat_dict, cat_file)
        except NumAttemptsExceeded as e:
            print(e)


if __name__ == "__main__":
    dir = "categories"
    url = "https://5ka.ru/api/v2/special_offers/"
    parser = Parse_5ka(url, dir)
    parser.run()
