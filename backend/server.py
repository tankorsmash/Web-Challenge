import arrow
import statistics

from flask import Flask, jsonify, request

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
        date_labels.append(arrow.get(date).format('YYYY-MM-DD'))
        average_axis.append(round(axes.get('rating_average', -1), 2))
        count_axis.append(axes.get('rating_count', -1))

    return date_labels, average_axis, count_axis

def clean_and_update_ratings(clean=True):
    """
    wipes database, requeries API and creates db rows

    In a full project, instead of dangerously wiping all Rating data,
     I'd leave them there and compare the new data to the old, and
     only add the ones I haven't added already.
    """
    if clean:
        print('deleting all Ratings')
        Rating.delete().execute()

    print('fetching from API Ratings')
    all_ratings = udemy_api.get_all_ratings()
    print('adding rows')
    create_bulk_ratings(all_ratings)
    print('done clean_and_update_ratings')

@server.route('/refresh_ratings', methods=['POST'])
def refresh_ratings():
    #use POST only to make sure we're deliberately purging the DB
    if (not request.json.get('do_refresh')):
        return jsonify({
            'success': False,
            'message': 'No do_refresh param, no action taken',
        })

    clean_and_update_ratings()
    return jsonify({
        'success': True,
        'message': 'Cleaned and updated',
    })

@server.route('/fetch_ratings')
def fetch_ratings():
    #if the DB is empty, fetch the data
    if (Rating.select().count() == 0):
        clean_and_update_ratings(clean=False)

    print('getting ratings from DB')
    date_labels, average_axis, count_axis = format_averages_for_chartjs(calc_ratings_over_time())
    print('returning data')

    current_average = udemy_api.get_current_average()
    return jsonify({
        'chart_data': {
            'date_labels': date_labels,
            'average_axis': average_axis,
            'count_axis': count_axis,
        },
        'current_average': current_average,
    })

if __name__ == '__main__':
    init_database()
    server.run(host='0.0.0.0', port=9000, debug=True)
