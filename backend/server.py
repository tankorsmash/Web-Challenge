import arrow
import statistics

from flask import Flask, jsonify

import udemy_api

from database import init_database, create_bulk_ratings, calc_ratings_over_time
from models import Rating, MODEL_DATE_FORMAT_ARROW

server = Flask(__name__)

@server.route('/ratings')
def ratings():
    #WIP only get data if non exists in database
    #TODO make it autoupdate every hour
    if (Rating.select().count() == 0):
        all_ratings = udemy_api.get_all_ratings()
        create_bulk_ratings(all_ratings)

    print("getting ratings from DB")
    averages = calc_ratings_over_time()
    print("returning data")
    return jsonify({
        "ratings": list(averages.items())
    })

if __name__ == "__main__":

    init_database()
    server.run(host='0.0.0.0', port=9000, debug=True)
