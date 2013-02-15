import functools

import json

import tornado.web
import tornado.gen

import dict2xml

class ApiHandler(tornado.web.RequestHandler):
    def get_format(self):
        format = self.get_argument('format', None)
        if not format:
            accept = self.request.headers.get('Accept')
            if accept:
                if 'javascript' in accept:
                    format = 'jsonp'
                elif 'json' in accept:
                    format = 'json'
                elif 'xml' in accept:
                    format = 'xml'
        return format or 'json'
        

    def write_response(self, obj, nofail=False):
        format = self.get_format()
        if format == 'json':
            self.set_header("Content-Type", "application/javascript")
            self.write(json.dumps(obj))
        elif format == 'jsonp':
            self.set_header("Content-Type", "application/javascript")
            callback = self.get_argument('callback', 'callback')
            self.write('%s(%s);'%(callback, json.dumps(obj)))
        elif format == 'xml':
            self.set_header("Content-Type", "application/xml")
            self.write('<response>%s</response>'%dict2xml.dict2xml(obj))
        elif nofail:
            self.write(json.dumps(obj))
        else:
            raise tornado.web.HTTPError(400, 'Unknown response format requested: %s'%format)

    def write_error(self, status_code, exc_info=None, **kwargs):        
        errortext = 'Internal error'
        if exc_info:
            errortext = getattr(exc_info[1], 'log_message', errortext)
        
        self.write_response({'status' : 'error',
                             'code' : status_code,
                             'reason' : errortext},
                            nofail=True)

def protected(fn):
    def run_it(self, *args, **kwargs):
        callback = kwargs.pop('callback')
        ret = fn(self, *args, **kwargs)
        callback(ret)

    @functools.wraps(fn)    
    def wrapped(self, *args, **kwargs):
        yield tornado.gen.Task(self.authenticate)
            
        yield tornado.gen.Task(run_it, self, *args, **kwargs)

    return wrapped

class ProtectedResourceType(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(ProtectedResourceType, cls).__new__
        new_class = super_new(cls, name, bases, attrs)
        for method in ('get', 'post', 'put', 'delete'):
            if hasattr(new_class, method):
                setattr(new_class, method, tornado.web.asynchronous(
                        tornado.gen.engine(
                            protected(getattr(new_class, method))
                            )))
        new_class.authenticate = tornado.web.asynchronous(
            tornado.gen.engine(new_class.authenticate))
        return new_class


class ProtectedResource(ApiHandler):
    __metaclass__ = ProtectedResourceType
      
    def authenticate(self, callback):
        callback()
