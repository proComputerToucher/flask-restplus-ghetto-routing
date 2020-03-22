from flask import Flask
from flask_restplus import Api
from namespaces import ns 
from controllers.cpubound import *
from controllers.iobound import *

app = Flask(__name__)
api = Api(app)

for namespace in ns:
    api.add_namespace(ns[namespace])

if __name__=='__main__':
    app.run(host='0.0.0.0')