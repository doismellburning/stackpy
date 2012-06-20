import httplib
import urllib
from StringIO import StringIO
import gzip

try:
    import simplejson as json
except ImportError:
    import json

DEBUG = True
DEBUG = False

class Stackpy:
    host = 'api.stackexchange.com'
    version = '2.0'
    site = None
    key = '7YoesYKhJ0cCBsoJc)JaRQ(('
    access_token = None

    def __init__(self):
        self.connection = httplib.HTTPSConnection(self.host, strict=True)

    def _api_fetch(self, endpoint, site=None, siteless=False, item_type=None,
              **kwargs):
        params = {}

        if not siteless:
            if not site:
                site = self.site
            if not site:
                site = 'stackoverflow'
            params['site'] = site

        params.update(kwargs)

        if self.key:
            params['key'] = self.key
        if self.access_token:
            params['access_token'] = self.access_token
            #TODO Barf if no key

        url = "/%s/%s?%s" % (self.version, endpoint, urllib.urlencode(params))
        self.connection.request('GET', url)
        response = self.connection.getresponse()
        #TODO Handle various forms of failure...
        data = response.read()
        data = self._decompress(data)
        data = json.loads(data)

        # If error_id we assume it's all dead Jim
        # TODO It may not be the case that error => total failure
        if 'error_id' in data:
            raise StackpyError(data['error_id'], data['error_name'],
                data['error_message'])

        data = Response(self, data, item_type)
        if data.backoff:
            #TODO Handle backoff
            print('Got backoff of %d - currently unhandled...' % data.backoff)

        return data

    def _decompress(self, data):
        #TODO Handle cases other than "blind gunzip"
        buf = StringIO(data)
        gzipfile = gzip.GzipFile(fileobj=buf)
        data = gzipfile.read()
        return data

    def sites(self, **kwargs):
        return self._api_fetch('/sites', siteless=True, item_type=Site, **kwargs)
    
    def users(self, ids=None, **kwargs):
        if ids is not None:
            if len(ids) == 0:
                return Response(self, {'items': []}, None)
            ids = _join_ids(ids)
            users = self._api_fetch('/users/%s' % ids, item_type=User, **kwargs)
        else:
            users = self._api_fetch("/users", item_type=User, **kwargs)

        return users

    def user_badges(self, user_ids, **kwargs):
        ids = _join_ids(user_ids)
        return self._api_fetch("/users/%s/badges" % ids, item_type=Badge, **kwargs)

    def me(self):
        #TODO Assert access_token
        return self._api_fetch('/me', item_type=User)

def _join_ids(ids):
    int_ids = [int(id_) for id_ in ids] #Convert to ints first, so we TypeError on invalid ids
    return ';'.join([str(id_) for id_ in ids])

class Base(object):
    def __init__(self, stackpy, data):
        self.stackpy = stackpy
        if DEBUG:
            self.data = data
            print(data)
        for key, value in data.iteritems():
            if key.startswith('_'):
                continue
            setattr(self, key, self._coerce(key, value))

    def _coerce(self, key, value):
        return value

class Response(Base):
    """ http://api.stackexchange.com/docs/wrapper """
    backoff = None

    def __init__(self, stackpy, data, item_type=None):
        super(Response, self).__init__(stackpy, data)
        # TODO Handle item_type being None / a type being included
        item_objs = [item_type(stackpy, item) for item in self.items]
        self.items = item_objs

class StackpyError(Exception):
    def __init__(self, error_id, name, description):
        self.error_id = error_id
        self.name = name
        self.description = description

    def __str__(self):
        return '(%d) %s: %s' % (self.error_id, self.name, self.description)


class User(Base):
    def _coerce(self, key, value):
        if key == 'badge_counts':
            return BadgeCount(self.stackpy, value)
        else:
            return value

    def badges(self, **kwargs):
        return self.stackpy.user_badges([self.user_id], **kwargs)

class BadgeCount(Base):
    pass

class Site(Base):
    pass

class Badge(Base):
    pass

def oauth_explicit_one(client_id, redirect_uri, scope=None, state=None):
    url = 'https://stackexchange.com/oauth'
    params = {'client_id': client_id, 'redirect_uri': redirect_uri}
    if scope is not None:
        params['scope'] = scope
    if state is not None:
        params['state'] = state
    return '%s?%s' % (url, urllib.urlencode(params))

def oauth_explicit_two(client_id, client_secret, code, redirect_uri):
    params = {'client_id': client_id, 'client_secret': client_secret,
              'code': code, 'redirect_uri': redirect_uri}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    connection = httplib.HTTPSConnection('stackexchange.com', strict=True)
    connection.request('POST', '/oauth/access_token', urllib.urlencode(params), headers)
    # Charles
    #connection = httplib.HTTPConnection('localhost:8888')
    #connection.request('POST', 'https://stackexchange.com/oauth/access_token', urllib.urlencode(params))
    response = connection.getresponse()
    return response.read()
