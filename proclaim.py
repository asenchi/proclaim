

class Proclaim(object):

    def __init__(self, redis):
        self.redis = redis
        self.groups = { "all": [] }

    def activate_group(self, feature, group):
        if group in self.groups:
            self.redis.sadd(_group_key(feature), group)

    def deactivate_group(self, feature, group):
        self.redis.srem(_group_key(feature), group)

    def deactivate_all(self, feature):
        self.redis.delete(_group_key(feature))
        self.redis.delete(_user_key(feature))
        self.redis.delete(_percentage_key(feature))

    def activate_user(self, feature, user):
        self.redis.sadd(_user_key(feature), user.id)

    def deactivate_user(self, feature, user):
        self.redis.srem(_user_key(feature), user.id)

    def define_group(self, group, *users):
        self.groups[group] = []
        for user in users:
            self.groups[group].append(user.id)

    def is_active(self, feature, user):
        if self._user_in_active_group(feature, user):
            return True
        if self._user_active(feature, user):
            return True
        if self._user_within_active_percentage(feature, user):
            return True
        return False

    def activate_percentage(self, feature, percentage):
        self.redis.set(_percentage_key(feature), percentage)

    def deactivate_percentage(self, feature, percentage):
        self.redis.delete(_percentage_key(feature), percentage)

    def _user_in_active_group(self, feature, user):
        if self.redis.exists(_group_key(feature)):
            active_groups = self.redis.smembers(_group_key(feature))
            if active_groups:
                for grp in active_groups:
                    if user.id in self.groups[grp]:
                        return True
        return False

    def _user_active(self, feature, user):
        if self.redis.sismember(_user_key(feature), user.id):
            return True
        return False

    def _user_within_active_percentage(self, feature, user):
        if self.redis.exists(_percentage_key(feature)):
            percentage = self.redis.get(_percentage_key(feature))
            if int(user.id) % 10 < int(percentage) / 10:
                return True
        return False

def _key(name):
    return "feature:%s" % name

def _group_key(name):
    return "%s:groups" % (_key(name))

def _user_key(name):
    return "%s:users" % (_key(name))

def _percentage_key(name):
    return "%s:percentage" % (_key(name))

