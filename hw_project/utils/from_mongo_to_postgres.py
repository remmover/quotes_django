import os

from pymongo import MongoClient
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hw_project.settings")
django.setup()

from quotes.models import Quote, Tag, Author  # noqa

client = MongoClient("mongodb+srv://remmover:password@cluster0.uhuxtdj.mongodb.net/")

db = client.mein

authors = db.authors.find()

for author in authors:
    Author.objects.get_or_create(
        fullname=author['fullname'],
        born_date=author['born_date'],
        born_location=author['born_location'],
        description=author['description']
    )
quotes = db.quotes.find()

for quote in quotes:
    # print(quote)
    tags = []
    for tag in quote['tags']:
        t, *_ = Tag.objects.get_or_create(name=tag)
        tags.append(t)
    # print(tags)

    exists_quote = bool(len(Quote.objects.filter(text=quote['text'])))

    if not exists_quote:
        author = db.authors.find_one({'_id': quote['author']})
        a = Author.objects.get(fullname=author['fullname'])
        q = Quote.objects.create(
            text=quote['text'],
            author=a
        )

        for tag in tags:
            q.tags.add(tag)