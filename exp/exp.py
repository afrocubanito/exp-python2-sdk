import signal
import sys
import logging
import traceback

from logging.handlers import RotatingFileHandler

from . import network
from . import authenticator
from . import api
from . import exceptions


""" List of all instances of Exp. """
instances = []


""" Configure the logger. """
file_handler_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

file_handler = RotatingFileHandler('debug.log', mode='a', maxBytes=5*1024*1024, backupCount=5, encoding=None, delay=0)
file_handler.setFormatter(file_handler_formatter)
file_handler.setLevel(logging.DEBUG)

stream_handler_formatter = logging.Formatter('EXP/%(levelname)-10s: %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(stream_handler_formatter)
stream_handler.setLevel(logging.INFO)

logger = logging.getLogger('exp')
#logger.addHandler(file_handler)
#logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


""" Terminate all running instances when Ctrl-C is pressed. """
signal.signal(signal.SIGINT, lambda signal, frame: stop())


def start (enable_network=True, host='https://api.goexp.io', **options):

  """ Validate SDK options """
  options['host'] = host
  options['enable_network'] = enable_network
  if options.get('type') is 'user' or ((options.get('username') or options.get('password') or options.get('organization')) and not options.get('type')):
    options['type'] = 'user'
    if not options.get('username'):
      raise exceptions.RuntimeError('Please specify the username.')
    if not options.get('password'):
      raise exceptions.RuntimeError('Please specify the password.')
    if not options.get('organization'):
      raise exceptions.RuntimeError('Please specify the organization.')
  elif options.get('type') is 'device' or ((options.get('secret') or options.get('allow_pairing')) and not options.get('type')):
    options['type'] = 'device'
    if not options.get('uuid') and not options.get('allow_pairing'):
      raise exceptions.RuntimeError('Please specify the device uuid.')
    if not options.get('secret') and not options.get('allow_pairing'):
      raise exceptions.RuntimeError('Please specify the device secret.')
  elif options.get('type') is 'consumer_app' or (options.get('api_key') and not options.get('type')):
    options['type'] = 'consumer_app'
    if not options.get('uuid'):
      raise exceptions.RuntimeError('Please specify the consumer app uuid.')
    if not options.get('api_key'):
      raise exceptions.RuntimeError('Please specify the consumer app api key.')
  else:
    raise exceptions.RuntimeError('Please specify authentication type.')

  """ Generate wrapper and SDK instance """
  sdk = Sdk(**options)
  if options['enable_network']:
    sdk.network.start()
  exp = Exp(sdk)
  instances.append(exp)
  return exp


def stop ():
  """ Stop all running SDK instances. """
  [exp.stop() for exp in instances[:]]


class Sdk (object):
  """ Wrapper to hold SDK modules. """

  def __init__(self, **options):
    self.options = options
    self.authenticator = authenticator.Authenticator(self)
    self.api = api.Api(self)
    self.network = network.Network(self)
    self.logger = logger
    self.exceptions = exceptions


class Exp (object):

  def __init__(self, sdk):
    self._sdk_ = sdk

  @property
  def _sdk(self):
    if not self._sdk_:
      raise exceptions.RuntimeError('This SDK instance is stopped.')
    return self._sdk_


  """ Runtime """

  def stop (self):
    if self in instances:
      instances.remove(self)
    self._sdk.network.stop()
    self._sdk_ = None # Remove internal references to SDK modules. All calls will now throw runtime error.

  def get_auth (self):
    return self._sdk.authenticator.get_auth()


  """ Naked API """

  def get (self, *args, **kwargs):
    return self._sdk.api.get(*args, **kwargs)

  def post (self, *args, **kwargs):
    return self._sdk.api.post(*args, **kwargs)

  def patch (self, *args, **kwargs):
    return self._sdk.api.patch(*args, **kwargs)

  def put (self, *args, **kwargs):
    return self._sdk.api.put(*args, **kwargs)

  def delete (self, *args, **kwargs):
    return self._sdk.api.delete(*args, **kwargs)

  """ Network """

  @property
  def is_connected(self):
    return self._sdk.network.is_connected

  def get_channel(self, *args, **kwargs):
    return self._sdk.network.get_channel(*args, **kwargs)




"""

                    # def get_device (*args, **kwargs):
                    #   return api.Device.get(*args, **kwargs)

                    #   def find_devices (*args, **kwargs):
                    #     return api.Device.find(*args, **kwargs)

                    #     def create_device (*args, **kwargs):
                    #       return api.Device.create(*args, **kwargs)


                    #       def get_thing (*args, **kwargs):
                    #         return api.Thing.get(*args, **kwargs)

                    #         def find_things (*args, **kwargs):
                    #           return api.Thing.find(*args, **kwargs)

                    #           def create_thing (*args, **kwargs):
                    #             return api.Thing.create(*args, **kwargs)


                    #             def get_experience (*args, **kwargs):
                    #               return api.Experience.get(*args, **kwargs)

                    #               def find_experiences (*args, **kwargs):
                    #                 return api.Experience.find(*args, **kwargs)

                    #                 def create_experience (*args, **kwargs):
                    #                   return api.Experience.create(*args, **kwargs)


                    #                   def get_location (*args, **kwargs):
                    #                     return api.Location.get(*args, **kwargs)

                    #                     def find_locations (*args, **kwargs):
                    #                       return api.Location.find(*args, **kwargs)

                    #                       def create_location (*args, **kwargs):
                    #                         return api.Location.create(*args, **kwargs)


                    #                         def get_data (*args, **kwargs):
                    #                           return api.Data.get(*args, **kwargs)

                    #                           def find_data (*args, **kwargs):
                    #                             return api.Data.find(*args, **kwargs)

                    #                             def create_data (*args, **kwargs):
                    #                               return api.Data.create(*args, **kwargs)


                    #                               def get_feed (*args, **kwargs):
                    #                                 return api.Feed.get(*args, **kwargs)

                    #                                 def find_feeds (*args, **kwargs):
                    #                                   return api.Feed.find(*args, **kwargs)

                    #                                   def create_feed (*args, **kwargs):
                    #                                     return api.Feed.create(*args, **kwargs)


                    #                                     def get_content (*args, **kwargs):
                    #                                       return api.Content.get(*args, **kwargs)

                    #                                       def find_content (*args, **kwargs):
                    #                                         return api.Content.find(*args, **kwargs)

"""
