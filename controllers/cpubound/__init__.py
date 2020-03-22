from namespaces import ns
from flask_restplus import Api, Namespace

api = Namespace('cpubound')
if 'cpubound' not in ns:
    ns['cpubound'] = api 

from .primemachine import *
from .factorialmachine import *