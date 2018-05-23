import arrow
import pathlib
import requests

try:
    from udemy_config import UDEMY_CLIENT_ID, UDEMY_CLIENT_SECRET
except ImportError:
    missing_path = pathlib.Path("./udemy_config.py")
    print("ERR: add UDEMY_CLIENT_ID and UDEMY_CLIENT_SECRET to {path}".format(path=missing_path.absolute()))


UDEMY_COURSE_ID = 1178124 #haven't confirmed this yet, got it from '.introduction-asset a[data-course-id]' on the linked Udemy page
API_DATE_FORMAT = "YYYY-MM-DD HH:mm:ss ZZ"

session = requests.session()

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

def get_latest_reviews():
    # resp = session.get(_format_api_url("reviews/"), params=_format_api_fields({"ratings": "@min"})

    #API key hasn't been confirmed yet, so let's make up a response type
    # plus flattery gets you everywhere
    return {
        'timestamp': arrow.utcnow().format(API_DATE_FORMAT),
        'results': [
            {'rating': 5.00},
            {'rating': 5.00},
            {'rating': 5.00},
            {'rating': 5.00},
        ]
    }
