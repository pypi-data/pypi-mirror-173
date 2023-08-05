"""Queue Worker Meta information.
   Navigator Session allows us to store user-specific data into session object.
"""

__title__ = 'qworker'
__description__ = ('QueueWorker is asynchronous Task Queue implementation built on to of Asyncio.'
                   'Can you spawn distributed workers to run functions inside workers.')
__version__ = '1.3.1'
__author__ = 'Jesus Lara'
__author_email__ = 'jesuslarag@gmail.com'
__license__ = 'MIT'

def get_version() -> tuple: # pragma: no cover
   """
   Get nav-auth version as tuple.
   """
   return tuple(x for x in __version__.split('.')) # pragma: no cover
