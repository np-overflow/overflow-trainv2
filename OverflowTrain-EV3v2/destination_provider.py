import requests
import time

URL = "https://overflow-robotics-api.herokuapp.com"

class DestinationProvider:
    def __init__(self):
        pass

    def get_next_destination(self, retry_delay=4):
        sent_waiting_message = False
        while True:
            try:
                res = requests.get(URL)
                if res.status_code == 200:
                    return res.json()
                elif res.status_code == 404:
                    if not sent_waiting_message:
                        print("Waiting for next destination...")
                        sent_waiting_message = True
                else:
                    raise Exception

            except:
                print("No connection to '" + URL + "'! Try again!")

            time.sleep(retry_delay)