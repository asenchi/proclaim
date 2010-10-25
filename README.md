# Proclaim

Conditionally roll out features with Redis.

Based on James Golick's [rollout](http://github.com/jamesgolick/rollout).

## Usage

Activate 20% of users to view 'feature':

    >>> import redis
    >>> from proclaim import Proclaim
    >>> redis = redis.Redis()
    >>> pc = Proclaim(redis)
    >>> pc.activate_percentage("feature", 20)

Works with groups and users. User should have an 'id', Proclaim uses it to
verify whether user is 'active'.

## Copyright

Copyright © 2010 James Golick
Copyright © 2010 Curt Micol

See `LICENSE` for details.
