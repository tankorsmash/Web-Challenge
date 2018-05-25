import json
import arrow
import base64
import pathlib
import requests
import operator


try:
    from udemy_config import UDEMY_CLIENT_ID, UDEMY_CLIENT_SECRET
except ImportError:
    missing_path = pathlib.Path("./udemy_config.py")
    print("ERR: add UDEMY_CLIENT_ID and UDEMY_CLIENT_SECRET to {path}".format(path=missing_path.absolute()))


UDEMY_COURSE_ID = 1178124 #haven't confirmed this yet, got it from '.introduction-asset a[data-course-id]' on the linked Udemy page
API_DATE_FORMAT = "YYYY-MM-DD HH:mm:ss ZZ"

session = requests.session()
b64hash = base64.b64encode(
    "{cid}:{secret}".format(
        cid=UDEMY_CLIENT_ID,
        secret=UDEMY_CLIENT_SECRET
    ).encode()
)
session.headers.update({
    "Authorization" : "Basic {}".format(b64hash)
})

BASE_URL = "https://www.udemy.com/api-2.0/courses/{course_id}/".format(course_id=UDEMY_COURSE_ID)

def _format_api_url(path):
    return BASE_URL+path

def _format_api_fields(fields):
    """
    Formats the course fields into querystring
    >>> params = _format_api_fields({'ratings': '@min'})
    >>> print(params)
    >>> "fields[rating]=@min"
    """

    params = {}
    for name, data in fields.items():
        params["fields[{}]".format(name)] = data

    return params

def get_ratings_count():
    """
    get total ratings count from api
    """

    #cheat because we're only looking for the count from the response
    params = _format_api_fields({"course_review": "id"})
    params.update({
        'page': 1,
        'page_size': 1,
    })
    resp = session.get(
        _format_api_url("reviews/"),
        params=params,
        timeout=3
    )
    json = resp.json()

    return json['count']


def get_all_ratings():
    """
    returns list of (udemy id, created, rating) rating tuples
    """

    ratings_count = get_ratings_count()
    print ("found {} ratings, getting them all now".format(ratings_count))

    all_ratings = []

    rating_getter = operator.itemgetter("id", "created", "rating")

    page_idx = 1
    while len(all_ratings) < ratings_count:
        params = _format_api_fields({"course_review": "rating,created"})
        params.update({
            'page': page_idx,
            'page_size': 1000,
        })

        resp = session.get(
            _format_api_url("reviews/"),
            params=params,
            timeout=15
        )
        resp_json = resp.json()

        all_ratings.extend(map(rating_getter, resp_json.get('results', [])))
        print("done page {}".format(page_idx))
        page_idx += 1

    print("got all {} ratings", len(all_ratings))

    print("saving to disk for later")
    with open("_cached_all_ratings.json", "w") as f:
        json.dump(all_ratings, f)

    return all_ratings


if __name__ == "__main__":
    print("getting ratings")
    get_all_ratings()
    print("done")
