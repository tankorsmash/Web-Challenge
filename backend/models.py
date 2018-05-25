import collections
from peewee import (
    SqliteDatabase, Model, IntegerField, DateTimeField, FloatField
)

MODEL_DATE_FORMAT = 'YYYY-MM-DD HH:MM:SS' #default peewee format
MODEL_DATE_FORMAT_ARROW = 'YYYY-MM-DD HH:mm:SS' #default peewee format

database = SqliteDatabase('ratings.db')

# we pull this data out from the database to easily count the hourly change in rating
RatingAggregate = collections.namedtuple('RatingAggregate', ['datetime_hour', 'rating_count', 'rating_sum'])

class Rating(Model):
    rating_score = FloatField()
    udemy_id = IntegerField()
    created = DateTimeField(formats=[MODEL_DATE_FORMAT])

    class Meta:
        database = database
