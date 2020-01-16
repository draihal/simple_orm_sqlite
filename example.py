from orm import Database

db = Database('db.sqlite')


class BlogPost(db.Model):
    title = str  # text, int or float
    date = int
    text = str

    def __init__(self, title, date, text):
        self.title = title
        self.date = date
        self.text = text


post = BlogPost('Some title', 42, 'Some text...').save()
print(post.text)  # Some text...
print(BlogPost.manager().get(id=1))  # {'id': 1, 'title': 'Some title', 'date': 42, 'text': 'Some text...'}
post.text = 'Some another text...'
post.update()
print(post.text)  # Some another text...
db.commit()
post.delete()
db.commit()
objects = BlogPost.manager(db)
objects.save(BlogPost('Another title', 13, 'Some info'))
print(objects.get(2))  # {'id': 2, 'title': 'Another title', 'date': 13, 'text': 'Some info'}
db.close()
print(list(objects.all()))  # []
