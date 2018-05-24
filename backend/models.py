from peewee import (
    SqliteDatabase, Model, CharField, DateTimeField, FloatField
)

MODEL_DATE_FORMAT = "YYYY-MM-DD HH:MM:SS" #default peewee format
MODEL_DATE_FORMAT_ARROW = "YYYY-MM-DD HH:mm:SS" #default peewee format

database = SqliteDatabase('ratings.db')
class Rating(Model):
    rating_score = FloatField()
    username = CharField()
    created_at = DateTimeField(formats=[MODEL_DATE_FORMAT])

    class Meta:
        database = database
