import json
from itertools import islice
from flask_restplus import Resource, Api, Namespace, reqparse
from controllers.cpubound import api 


def memoize_factorial(f):
    memory = {}

    def inner(num):
        if num not in memory:
            memory[num] = f(num)
        return memory[num]
    return inner 

@memoize_factorial
def facto(num):
    if num == 1:
        return 1
    else:
        return num * facto(num - 1)

def factorial_generator():
    n = 1
    while True:
        yield facto(n)
        n += 1
    

def validate(s):
    if s.isdigit():
        s = int(s)
        if isinstance(s, int) and s >= 0 and s < 50:
            return s
    
    raise Exception(f'value {s} is too large to compute')



parser = reqparse.RequestParser()
parser.add_argument('to', type=validate, required=True)

@api.route('/factogen')
@api.expect(parser)
class FactorialGenerator(Resource):
    @api.param('to', 'Generate list of factorials up to this number')
    def get(self):
        args = parser.parse_args()
        to = args['to']
        factos = list([x for x in islice(factorial_generator(), to)])
        return json.dumps(factos)

