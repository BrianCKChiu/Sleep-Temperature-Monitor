import json

from server.database import insert_temp_data
from .models.request import RequestParameters
from datetime import datetime


def handle_request(ip_addr: str, request: str):
    data: RequestParameters = json.load(request)

    # if temp data exists
    if "temp" in data:
        insert_temp_data(ip_addr, datetime.now(), data["temp"])
