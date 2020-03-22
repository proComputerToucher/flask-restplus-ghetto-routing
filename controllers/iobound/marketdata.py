from controllers.iobound import api
from flask_restplus import reqparse, inputs, Resource
from werkzeug.exceptions import BadRequest
import pandas as pd
import os, sys, datetime, json

dir = os.path.abspath('.\controllers\iobound\AMD_Historical.csv')
# read historical csv and clean up the columns
amd_df = pd.read_csv(dir)
amd_df['Ticker'] = 'AMD'
amd_df.rename(columns=lambda c: c.strip(), inplace=True)
amd_df.rename(columns={'Close/Last': 'Close'}, inplace=True)
amd_df['Date'] = pd.to_datetime(amd_df['Date'])
amd_df = amd_df.sort_values('Date')
amd_df['Volume'] = pd.to_numeric(amd_df['Volume'])
amd_df['Close'] = amd_df['Close'].map(lambda x: x.replace('$', '').strip())
amd_df['Open'] = amd_df['Open'].map(lambda x: x.replace('$', '').strip())
amd_df['High'] = amd_df['High'].map(lambda x: x.replace('$', '').strip())
amd_df['Low'] = amd_df['Low'].map(lambda x: x.replace('$', '').strip())
numeric_cols = ['Volume', 'Close', 'Open', 'High', 'Low']


# route parameters
parser = reqparse.RequestParser()
parser.add_argument('start_date', type=inputs.datetime_from_iso8601, required=True)
parser.add_argument('end_date', type=inputs.datetime_from_iso8601)


@api.route('/marketdata', endpoint='what_does_endpoint_do')
@api.expect(parser)
class MarketData(Resource):    
    def datetime_handler(self, x):
        if isinstance(x, datetime.datetime):
            return x.isoformat()
        raise TypeError('Unknown type')

    def get(self):
        args = parser.parse_args()
        start_date = args['start_date']
        end_date = args['end_date']

        if start_date > end_date:
            raise BadRequest('start_date cannot be a later date than end_date...dummy')

        mask = amd_df['Date'] >= start_date
        if end_date:
            mask = (amd_df['Date'] >= start_date) & (amd_df['Date'] <= end_date)
        
        mkt_value = amd_df.loc[mask]

        result = {
            'columns': [],
            'data': []
        }

        if len(mkt_value) > 0:            
            result['columns'].extend(list(mkt_value.columns.values))
            a = [v.tolist() for v in list(mkt_value.values)]
            result['data'].extend(a)
        
        return json.dumps(result, default=self.datetime_handler)
        
