import arrow
import random
import warnings

import peewee
from peewee import (
    SqliteDatabase, Model, CharField, DateField, FloatField
)
from playhouse.sqlite_udf import register_all

from models import Rating, RatingAggregate, MODEL_DATE_FORMAT_ARROW


def create_bulk_ratings(rows):
    fields = [Rating.udemy_id, Rating.created, Rating.rating_score]

    count = len(rows)
    print('creating {} rows'.format(count))
    database = SqliteDatabase('ratings.db')
    with database.atomic():
        step_range = 250 #scale down as needed
        for step in range(0, count, step_range):
            Rating.insert_many(
                rows[step:step+step_range],
                fields=fields
            ).execute()

    print('done creating rows')

def get_date_filter_expr(date_filter):
    if date_filter == 'all':
        #TODO figure out neutral peewee expression
        return Rating.created > arrow.now().shift(years=-10).datetime
    elif date_filter == 'year':
        return Rating.created > arrow.now().shift(years=-1).datetime
    elif date_filter == 'month':
        return Rating.created > arrow.now().shift(months=-1).datetime
    elif date_filter == 'week':
        return Rating.created > arrow.now().shift(weeks=-1).datetime
    elif date_filter == 'day':
        return Rating.created > arrow.now().shift(days=-1).datetime

    raise Exception('Unknown date_filter {}'.format(date_filter))

def get_averages_over_time_sql(date_filter='all'):
    """
    returns ( year-month-day-hour, num_ratings, total_rating ) for that hour
    to be processed elsewhere
    """
    date_expr = get_date_filter_expr(date_filter)

    ratings = Rating.select(
        peewee.fn.strftime('%Y-%m-%d-%H', Rating.created),
        peewee.fn.Count(Rating.rating_score),
        peewee.fn.Sum(Rating.rating_score)
    ) \
    .where(date_expr) \
    .order_by(Rating.created) \
    .group_by(
        peewee.fn.strftime('%Y-%m-%d-%H', Rating.created)
    ).tuples()

    ratings = list(map(lambda data: RatingAggregate(*data), ratings))

    return ratings

def _get_averages_over_time(all_ratings):
    """
    for each RatingAggregate, check if its up to the min datetime
    if it is:
       calc some stats, break
    if not:
      add its count and sum to the running count
      loop
    """

    TUPLE_DATETIME_FORMAT = 'YYYY-MM-DD-HH'
    start_time = arrow.get(all_ratings[0][0], TUPLE_DATETIME_FORMAT )
    end_time = arrow.utcnow()

    averages_by_hour = dict()

    rating_idx = 0
    current_count = 0
    current_sum = 0
    for current_hour, next_hour in arrow.Arrow.interval('day', start_time, end_time):
        while rating_idx < len(all_ratings):
            rating = all_ratings[rating_idx]

            rating_created = arrow.get(rating[0], TUPLE_DATETIME_FORMAT)
            if rating_created > next_hour:
                if current_count:
                    averages_by_hour[current_hour.format(MODEL_DATE_FORMAT_ARROW)] = {
                        'rating_average': current_sum/current_count,
                        'rating_count': current_count
                    }
                break

            #keep on iterating through the ratings
            current_count += rating.rating_count
            current_sum += rating.rating_sum

            rating_idx += 1

    return averages_by_hour

def calc_ratings_over_time(date_filter='all'):
    rating_aggregates = get_averages_over_time_sql(date_filter=date_filter)
    return _get_averages_over_time(rating_aggregates)

def init_database():
    database = SqliteDatabase('ratings.db')
    register_all(database)

    database.connect()
    database.create_tables([Rating])
