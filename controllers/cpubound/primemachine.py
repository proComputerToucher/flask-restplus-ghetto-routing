import math, json
from itertools import islice
from flask_restplus import Resource, Api, Namespace, reqparse
from controllers.cpubound import api

def is_prime(n):
    if n <= 1:
        return False
    elif n == 2:
        return True
    elif n % 2 == 0:
        return False
    
    i = 3
    while i <= math.sqrt(n):
        if n % i == 0:
            return False
        i += 2
    
    return True

def prime_generator():
    i = 1
    while True:
        i += 1
        if is_prime(i):
            yield i

parser = reqparse.RequestParser()
parser.add_argument('to', type=int, required=True)

@api.route('/primegen')
@api.expect(parser)
class PrimeGenerator(Resource):
    @api.param('to', 'Generate prime up to this number')
    def get(self):
        args = parser.parse_args()
        to = args['to']        
        primes = list([x for x in islice(prime_generator(), to)])
        return json.dumps(primes)
