"""
Источник https://gb.ru/posts/
Необходимо обойти все записи в блоге и извлеч из них информацию следующих полей:
url страницы материала
Заголовок материала
Первое изображение материала (Ссылка)
Дата публикации (в формате datetime)
имя автора материала
ссылка на страницу автора материала
комментарии в виде (автор комментария и текст комментария)
Структуру сохраняем в MongoDB
"""

import time
import datetime
import typing

import requests
from urllib.parse import urljoin
from pymongo import MongoClient
import bs4


class GbBlogParse:
    def __init__(self, start_url, collection):
        self.time = time.time()
        self.start_url = start_url
        self.collection = collection
        self.done_urls = set()
        self.tasks = []
        start_task = self.get_task(self.start_url, self.parse_feed)
        self.tasks.append(start_task)
        self.done_urls.add(self.start_url)

    def _get_response(self, url, *args, **kwargs):
        if self.time + 0.9 < time.time():
            time.sleep(0.5)
        response = requests.get(url, *args, **kwargs)
        self.time = time.time()
        print(url)
        return response

    def _get_soup(self, url, *args, **kwargs):
        soup = bs4.BeautifulSoup(self._get_response(url, *args, **kwargs).text, "lxml")
        return soup

    def get_task(self, url: str, callback: typing.Callable) -> typing.Callable:
        def task():
            soup = self._get_soup(url)
            return callback(url, soup)

        if url in self.done_urls:
            return lambda *_, **__: None
        self.done_urls.add(url)
        return task

    def task_creator(self, url, tags_list, callback):
        links = set(
            urljoin(url, itm.attrs.get("href"))
            for itm in tags_list
            if itm.attrs.get("href")
        )
        for link in links:
            task = self.get_task(link, callback)
            self.tasks.append(task)

    def get_comment_thread(self, comment):
        comment = comment['comment']
        comment_dict = {
            'author_name': comment['user']['full_name'],
            'comment': comment['body']
        }
        replies = []
        for reply in comment['children']:
            replies.append(self.get_comment_thread(reply))

        comment_dict['replies'] = replies
        return comment_dict

    def parse_comments(self, url, commentable_id):
        comments_url =urljoin(url, f'/api/v2/comments?commentable_type=Post&commentable_id={commentable_id}')
        comments_list = self._get_response(comments_url).json()
        parsed_comments = []

        for comment in comments_list:
            parsed_comments.append(self.get_comment_thread(comment))

        return parsed_comments

    def parse_feed(self, url, soup):
        ul_pagination = soup.find("ul", attrs={"class": "gb__pagination"})
        list_ref = ul_pagination.find_all("a")
        self.task_creator(url, ul_pagination.find_all("a"), self.parse_feed)
        post_wrapper = soup.find("div", attrs={"class": "post-items-wrapper"})
        self.task_creator(
            url, post_wrapper.find_all("a", attrs={"class": "post-item__title"}), self.parse_post
        )

    def parse_post(self, url, soup):
        title_tag = soup.find("h1", attrs={"class": "blogpost-title"})
        image = img_src = soup.find(attrs={'class': 'blogpost-content'}).img
        img_src = None
        if image is not None:
            img_src = image['src']
        datetime_str = soup.find(attrs={'class': 'blogpost-date-views'}).time['datetime']
        post_datetime = datetime.datetime.strptime(datetime_str, '%Y-%m-%dT%X%z')
        author_row = soup.find(attrs={'class': 'row m-t'})
        author_name = author_row.find(attrs={'itemprop': 'author'}).text
        author_url = urljoin(url, author_row.a['href'])
        commentable_id = soup.find('comments')['commentable-id']
        comments = self.parse_comments(url, commentable_id)

        data = {
            "url": url,
            "title": title_tag.text,
            "post_img": img_src,
            "post_date": post_datetime,
            "author": {
                "name": author_name,
                "url": author_url
            },
            "comments": comments
        }
        return data

    def run(self):
        for task in self.tasks:
            task_result = task()
            if isinstance(task_result, dict):
                self.save(task_result)

    def save(self, data):
        self.collection.insert_one(data)


if __name__ == "__main__":
    collection = MongoClient()["gb_parse"]["gb_blog"]
    parser = GbBlogParse("https://gb.ru/posts", collection)
    parser.run()
