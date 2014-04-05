import json
import datetime
from hammock import Hammock

API = Hammock('http://holly.local/api')
API_HEADERS = {'Content-type': 'application/json'}


def send_status_message(message_from, message_body):
    post_data = json.dumps({
        'date': datetime.datetime.utcnow().isoformat(),
        'from': message_from,
        'messagebody': message_body
    })
    response = API.system.messages.POST(data=post_data, headers=API_HEADERS)
    if response.status_code != 201:
        # TODO: if this logging fails, send an email to me
        return False
    return True


def send_bulk_movement_log_data(motion_data_list):
    post_data = json.dumps({'movement_data': motion_data_list})
    response = API.indoor.movement.bulk.POST(data=post_data, headers=API_HEADERS)
    if response.status_code != 201:
        send_status_message('Nova5', 'Sending of bulk indoor movement data failed.')
        return False
    return True


def send_bulk_system_temperature_data(temperature_data_list):
    post_data = json.dumps({'temperature_data': temperature_data_list})
    response = API.system.temperature.bulk.POST(data=post_data, headers=API_HEADERS)
    if response.status_code != 201:
        send_status_message('Nova5', 'Sending of bulk system temperature data failed.')
        return False
    return True
