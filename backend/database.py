import arrow
import random

from peewee import (
    SqliteDatabase, Model, CharField, DateField, FloatField
)

from models import Rating, MODEL_DATE_FORMAT

database = SqliteDatabase('ratings.db')

database.connect()
database.create_tables([Rating])

def create_fake_data(count):
    fields = [Rating.rating_score, Rating.username, Rating.created_at]

    records = []
    for i in range(count):
        rating_score=round(random.uniform(0, 5))
        username="test_user"
        created_at=arrow.now().shift(hours=-random.randint(0, 24*7)).format(MODEL_DATE_FORMAT)

        records.append((rating_score, username, created_at))

    print("creating {} fake records".format(count))
    with database.atomic():
        step_range = 250 #scale down as needed
        for step in range(0, count, step_range):
            Rating.insert_many(records[step:step+step_range], fields=fields).execute()
    print("done creating fake records")

