import pathlib
import requests

try:
    from udemy_config import UDEMY_CLIENT_ID, UDEMY_CLIENT_SECRET
except ImportError:
    missing_path = pathlib.Path("./udemy_config.py")
    print("ERR: add UDEMY_CLIENT_ID and UDEMY_CLIENT_SECRET to {path}".format(path=missing_path.absolute()))

UDEMY_COURSE_ID = 1178124 #haven't confirmed this yet, got it from '.introduction-asset a[data-course-id]' on the linked Udemy page
