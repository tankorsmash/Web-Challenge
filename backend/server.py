import arrow
import statistics

from flask import Flask, jsonify

import udemy_api

from database import init_database, create_bulk_ratings, calc_ratings_over_time
from models import Rating, MODEL_DATE_FORMAT_ARROW

server = Flask(__name__)

def format_averages_for_chartjs(averages):
    """
    takes the averages dict and turns it into
    date labels, and two axes of data (count, avg)
    """
    date_labels = []
    average_axis = []
    count_axis = []

    for date, axes in averages.items():
        date_labels.append(date)
        average_axis.append(axes.get('rating_average', -1))
        count_axis.append(axes.get('rating_count', -1))

    return date_labels, average_axis, count_axis


@server.route('/ratings')
def ratings():
    #WIP only get data if non exists in database
    #TODO make it autoupdate every hour
    if (Rating.select().count() == 0):
        all_ratings = udemy_api.get_all_ratings()
        create_bulk_ratings(all_ratings)

    print("getting ratings from DB")
    date_labels, average_axis, count_axis = format_averages_for_chartjs(calc_ratings_over_time())
    print("returning data")
    return jsonify({
        "chart_data": {
            "date_labels": date_labels,
            "average_axis": average_axis,
            "count_axis": count_axis,
        }
    })

if __name__ == "__main__":

    init_database()
    server.run(host='0.0.0.0', port=9000, debug=True)
