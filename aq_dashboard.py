from flask import Flask
import openaq
from flask_sqlalchemy import SQLAlchemy



APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '< Time {} --- Value {} >'.format(self.datetime, self.value)

@APP.route('/')
def root():
    """Base view."""
    results = get_results()
    return results

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    results = body['results']
    for result in results:
        db_record = Record(datetime=result['date']['utc'], value=result['value'])
        DB.session.add(db_record)
    DB.session.commit()
    return 'Data refreshed!'

   
def get_results():
    # api = openaq.OpenAQ()
    # status, body = api.measurements(city='Los Angeles', parameter='pm25')
    # results = body['results']
    # tuples = [(result['date']['utc'], result['value']) for result in results]

    tuples = Record.query.filter(Record.value >= 10).all()
    return str(tuples)