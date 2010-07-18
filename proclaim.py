
import redis

redis = redis.Redis()

class Proclaim(object):
	def __init__(self, redis):
		self.redis = redis
		self.groups = { "all": set() }

	def active_group(self, feature, group):
		self._activate(feature, group)
		
	def deactivate_group(self, feature, group):
		self._deactivate(feature, group)
		
	def deactivate_all(self, feature):
		self.redis.del(group_key(feature))
		self.redis.del(user_key(feature))
		self.redis.del(percentage_key(feature))
		
	def activate_user(self, feature, user):
		self._activate(feature, user)
		
	def deactivate_user(self, feature, user):
		self._deactivate(feature, user)
		
	def define_group(group, *arg):
		self.groups[str(group)] = set(*arg)
		
	def is_active(self, feature, user):
		if self._user_in_active_group(feature, user) or
			self._user_active(feature, user) or
			self._user_within_active_percentage(feature, user):
			return true
	
	def activate_percentage(self, feature, percentage):
		self.redis.set(_percentage_key(feature), percentage)
		
	def deactivate_percentage(self, feature, percentage):
		self.redis.del(_percentage_key(feature), percentage)
		
	def _activate(self, feature, target):
		self.redis.sadd(_group_key(feature), target)
		
	def _deactivate(self, feature, target):
		self.redis.srem(_group_key(feature), target)

	def _key(self, name):
		return "feature:%s" % name
		
	def _group_key(name):
		return "%s:groups" % (_key(name))
		
	def _user_key(name):
		return "%s:users" % (_key(name))
		
	def _percentage_key(name):
		return "%s:percentage" % (_key(name))
	
	def _user_in_active_group(self, feature, user):
		active_groups = self.redis.smembers(_group_key(feature))
		for grp in active_groups:
			if user in groups[grp]:
				return True
		return False
	
	def _user_active(self, feature, user):
		self.redis.sismember(_user_key(feature), user.id)
		
	def _user_within_active_percentage(feature, user):
		percentage = self.redis.get(_percentage_key(feature))
		if not percentage:
			return None
		user.id % (100 / int(percentage)) == 0
		