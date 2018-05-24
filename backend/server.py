import arrow
import statistics

from flask import Flask, jsonify

import udemy_api

from models import Rating, MODEL_DATE_FORMAT_ARROW
from database import create_fake_data

server = Flask(__name__)

def get_all_ratings():
    ratings = Rating.select()
    return ratings

def get_floored_hour_of_rating(rating):
    try:
        return arrow.get(rating.created_at, MODEL_DATE_FORMAT_ARROW).floor("hour")
    except Exception as e:
        print(e)
        import ipdb; ipdb.set_trace()


def get_averages_over_time(ratings):
    """
    for each rating, check if its up to the min datetime
    if it is:
      add it to the mean calculation and continue
    if not:
      copy current average until the current rating's hour is reached
    """

    all_ratings = ratings[:25000]
    start_time = get_floored_hour_of_rating(all_ratings[0])
    end_time = arrow.utcnow()
    print('start', start_time.humanize(), 'end', end_time.humanize())

    ratings = []
    averages_by_hour = dict()

    rating_idx = 0
    for current_hour, next_hour in arrow.Arrow.interval('hour', start_time, end_time):
        while rating_idx < len(all_ratings):
            # print("rating idx", rating_idx)
            try:
                rating = all_ratings[rating_idx]
            except IndexError:
                print("breaking at", rating_idx)
                break

            rating_created_at = get_floored_hour_of_rating(rating)
            # print("rating created_at", rating_created_at.format(MODEL_DATE_FORMAT_ARROW), "vs next_hour", next_hour.format(MODEL_DATE_FORMAT_ARROW))
            if rating_created_at > next_hour:
                #calc mean for the current hour without including this rating
                if ratings:
                    averages_by_hour[current_hour.format(MODEL_DATE_FORMAT_ARROW)] = statistics.mean(ratings)
                break

            #keep on iterating through the ratings
            ratings.append(rating.rating_score)

            rating_idx += 1

    print("averages_by_hour:", len(averages_by_hour))
    return averages_by_hour



@server.route('/ratings')
def hello():
    if (Rating.select().count() == 0):
        create_fake_data(100000)

    ratings = get_all_ratings().order_by(Rating.created_at.asc())
    averages = get_averages_over_time(ratings)
    return jsonify({
        "ratings": list(averages.items())
    })

if __name__ == "__main__":
    server.run(host='0.0.0.0', port=9000, debug=True)
