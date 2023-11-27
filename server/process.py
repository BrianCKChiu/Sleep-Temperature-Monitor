from database import insert_temp_data
from datetime import datetime


def handle_request(ip_addr: str, request: str):
   

    # if temp data exists
    if "temp" in request:
        insert_temp_data(ip_addr, request['client_id'], datetime.now(), request["temp"])
