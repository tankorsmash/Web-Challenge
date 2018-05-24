import arrow
import random
import warnings

from peewee import (
    SqliteDatabase, Model, CharField, DateField, FloatField
)

from models import Rating, MODEL_DATE_FORMAT


def create_bulk_ratings(rows):
    fields = [Rating.udemy_id, Rating.created, Rating.rating_score]

    count = len(rows)
    print("creating {} rows".format(count))
    database = SqliteDatabase('ratings.db')
    with database.atomic():
        step_range = 250 #scale down as needed
        for step in range(0, count, step_range):
            Rating.insert_many(
                rows[step:step+step_range],
                fields=fields
            ).execute()

    print("done creating rows")

def init_database():
    database = SqliteDatabase('ratings.db')

    database.connect()
    database.create_tables([Rating])
