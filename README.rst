===============
tornado-api-kit
===============

A collection of routines for building web APIs on top of Tornado web server.

--------
Features
--------

* Automatic support multiple response formats (JSON, JSONP, XML)
* Pluggable authentication
* Error handling

-------------
Example usage
-------------

.. code-block:: python

  import apikit

  # Returning objects as response (only basic JSON-encodable types supported):
  class MyApiHander(apikit.ApiHandler):
      def get(self):
          self.write_response({'result' : 'sucess',
	                       'x' : 1, y : [1,2,3]})
  
  # Authentication:
  class MyProtectedResourceBase(apikit.ProtectedResource):
      def authenticate(self, callback):
          if self.get_argument('password') != '12345':
	      raise tornado.web.HTTPError(403, "Incorrect or missing password!")
	  callback()

  class MyProtectedResource(MyProtectedResourceBase):
      def get(self):
          ...



------------
Installation
------------
 
::

  $ pip install tornado-api-kit
