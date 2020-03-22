from namespaces import ns 
from flask_restplus import Namespace 

api = Namespace('iobound')
if 'iobound' not in ns:
    ns['iobound'] = api

from .marketdata import *