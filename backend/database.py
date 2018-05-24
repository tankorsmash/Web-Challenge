import arrow
import random
import peewee
import warnings

from playhouse.sqlite_udf import register_all

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

def get_averages_over_time_sql():
    """
    returns ( year-month-day-hour, num_ratings, total_rating ) for that hour
    to be processed elsewhere
    """
    ratings = Rating.select(
        peewee.fn.strftime("%Y-%m-%d-%H", Rating.created),
        peewee.fn.Count(Rating.rating_score),
        peewee.fn.Sum(Rating.rating_score)
    ).group_by(peewee.fn.strftime("%Y-%m-%d-%H", Rating.created)).tuples()

    return ratings


def init_database():
    database = SqliteDatabase('ratings.db')
    register_all(database)


    database.connect()
    database.create_tables([Rating])
