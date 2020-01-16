import os
from random import random
from orm import Database
import unittest

db = Database('db.sqlite.test')


class Example(db.Model):
    random = float
    text = str

    def __init__(self, text):
        self.text = text
        self.random = random()


class TestORM(unittest.TestCase):
    def setUp(self):
        pass

    def test_create_and_update_test(self):
        test_example = Example('Hello World').save()
        assert(test_example.id == 1)
        test_example.text = 'Hello ORM'
        test_example.update()
        db.commit()
        test_example = Example.manager().get(id=1)
        assert(test_example.text == 'Hello ORM')
        test_example.delete()
        db.commit()

    def test_invalid_save_test(self):
        try:
            invalid_post = Example(None).save(type_check=False)
        except TypeError as e:
            assert(False)
        else:
            assert(True)

    def test_second_record(self):
        objects = Example.manager()
        objects.save(Example('Hello World'))
        assert(set(objects.get(2).public.keys()) == set(['id', 'text', 'random']))
        assert(isinstance(objects.get(2).random, float))
        db.close()
        assert(list(objects.all()) == [])


# os.remove('db.sqlite.test')


if __name__ == '__main__':
    unittest.main()
