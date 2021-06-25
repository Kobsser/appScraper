""" STEP ONE """

import requests


def request_tg_code_get_random_hash(input_phone_number):
    """ requests Login Code
    and returns a random_hash
    which is used in STEP TWO """
    request_url = "https://my.telegram.org/auth/send_password"
    request_data = {
        "phone": input_phone_number
    }
    response_c = requests.post(request_url, data=request_data)
    try:
        json_response = True, response_c.json()
    except:
        json_response = False, response_c.text
    return json_response
