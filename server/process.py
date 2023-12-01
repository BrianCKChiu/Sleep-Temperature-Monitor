from database import insert_temp_data, insert_movement_data
from datetime import datetime


def handle_request(ip_addr: str, request: str):
    # if temp data exists
    if "temp" in request:
        insert_temp_data(ip_addr, request["client_id"], datetime.now(), request["temp"])
    elif "movement" in request:
        insert_movement_data(
            ip_addr,
            request["client_id"],
            datetime.now(),
            request["on_bed"],
            request["sleep_status"],
            request["overall_status"],
        )
