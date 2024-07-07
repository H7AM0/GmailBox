
import requests
import threading
from datetime import datetime

thread_local = threading.local()
SESSION_TIME_TO_LIVE = 600

session = None

def per_thread(key, construct_value, reset=False):
    if reset or not hasattr(thread_local, key):
        value = construct_value()
        setattr(thread_local, key, value)
    return getattr(thread_local, key)

def _get_req_session(reset=False):
    if SESSION_TIME_TO_LIVE:
        creation_date = per_thread('req_session_time', lambda: datetime.now(), reset)
        if (datetime.now() - creation_date).total_seconds() > SESSION_TIME_TO_LIVE:
            reset = True
            per_thread('req_session_time', lambda: datetime.now(), True)

    if SESSION_TIME_TO_LIVE == 0:
        return requests.sessions.Session()
    else:
        return per_thread('req_session', lambda: session if session else requests.sessions.Session(), reset)

def make_request(url: str, method: str = ["get","post"], headers: dict = None, json: dict = None, timeout: int = 60, response_type: str = ["json","cookies","text"]) -> dict:
    session = _get_req_session()
    response = session.request(
        method=method.lower(),
        url=url,
        headers=headers,
        timeout=timeout,
        json=json
    )

    if response_type == "text":
        return response.text
    elif response_type == "cookies":
        return response.cookies.get_dict()
    else:
        return response.json()
