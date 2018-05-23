from flask import Flask, jsonify

import udemy_api

from models import Rating

server = Flask(__name__)

def get_all_ratings():
    ratings = Rating.select().dicts()
    return ratings


@server.route('/ratings')
def hello():
    ratings = get_all_ratings()
    ratings = ratings[:1000]
    return jsonify({
        "ratings": list(ratings)
    })

if __name__ == "__main__":
    server.run(host='0.0.0.0', port=9000, debug=True)
