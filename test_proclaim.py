import redis
import unittest

from proclaim import Proclaim

class User(object):
    def __init__(self, **entries):
        self.__dict__.update(entries)

jim = User(id=1, username='jim@test.com')
bob = User(id=23, username='bob@test.com')
joan = User(id=40, username='joan@test.com')

class TestProclaim(unittest.TestCase):

    def setUp(self):
        self.redis = redis.Redis(host='localhost', port=6379)
        self.proclaim = Proclaim(self.redis)
        self.proclaim.define_group("a", jim, joan)
        self.proclaim.define_group("b", jim, joan, bob)
        
    def test_groups(self):
        assert len(self.proclaim.groups["b"]) == 3
        assert jim.id in self.proclaim.groups["a"]

    def test_active_group(self):
        self.proclaim.active_group("f1", "b")
        assert self.proclaim.is_active("f1", jim)
        
    def test_deactivate_group(self):
        self.proclaim.deactivate_group("f1", "b")
        assert not self.proclaim.is_active("f1", jim)
        
    def test_activate_user(self):
        self.proclaim.activate_user("f2", joan)
        assert self.proclaim.is_active("f2", joan)

    def test_deactivate_user(self):
        self.proclaim.deactivate_user("f2", joan)
        assert not self.proclaim.is_active("f2", joan)

    def test_activate_percentage(self):
        self.proclaim.activate_percentage("f3", 25)
        assert self.proclaim.is_active("f3", jim)
        assert self.proclaim.is_active("f3", joan)
        assert not self.proclaim.is_active("f3", bob)

    def test_deactivate_percentage(self):
        self.proclaim.deactivate_percentage("f3", 25)
        assert not self.proclaim.is_active("f3", jim)
