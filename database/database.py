import sqlalchemy.exc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from . import models


class Database:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        models.Base.metadata.create_all(bind=self.engine)
        self.maker = sessionmaker(bind=self.engine)
        self._purge_db()

    def _get_or_create(self, session, model, filter_field, **data):
        instance = session.query(model).filter_by(**{filter_field: data[filter_field]}).first()
        if instance is None:
            instance = model(**data)
            session.add(instance)
        return instance

    def _add_comments(self, session, data):
        result = []
        for comment in data:
            # author = self._get_or_create(
            #     session,
            #     models.Author,
            #     "url",
            #     name=comment["user"]["full_name"],
            #     url=comment["user"]["url"],
            #     id=comment["user"]["id"],
            # )
            # del comment['user']
            # comment_rec = self._get_or_create(session, models.Comment, "id", **comment, author=author)
            comment_rec = self._get_or_create(session, models.Comment, "id", **comment)
            result.append(comment_rec)
            result.extend(self._add_comments(session, comment["replies"]))
        return result

    def add_post(self, data):
        session = self.maker()
        post = self._get_or_create(session, models.Post, 'url', **data['post_data'])
        author = self._get_or_create(session, models.Author, 'url', **data['author_data'])
        post.author = author
        tags = [self._get_or_create(session, models.Tag, 'url', **tag_data) for tag_data in data['tags_data']]
        post.tags.extend(tags)
        post.comments.extend(self._add_comments(session, data['comments_data']))

        try:
            session.add(post)
            session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            session.rollback()
            print(e)
        finally:
            session.close()

    def _purge_db(self):
        session = self.maker()

        try:
            session.query(models.Post).delete()
            session.query(models.Author).delete()
            session.query(models.tag_post).delete()
            session.query(models.Tag).delete()
            session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            session.rollback()
        finally:
            session.close()
