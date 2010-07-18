
import redis
import unittest

import rollout

class TestRollout(unittest.TestCase):
	def setUp(self):
		redis = redis.Redis()
	def tearDown(self):
		del redis
		
	def test_activate_group(self):
		rollout.activate_group("testing", "admins")