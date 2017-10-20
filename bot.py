import websocket
import json
import requests
import urllib
import os


# Suppress InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

###VARIABLES THAT YOU NEED TO SET MANUALLY IF NOT ON HEROKU#####
try:
        MESSAGE = os.environ['WELCOME-MESSAGE']
        TOKEN = os.environ['SLACK-TOKEN']
        UNFURL = os.environ['UNFURL-LINKS']
except:
        MESSAGE = 'Manually set the Message if youre not running through heroku or have not set vars in ENV'
        TOKEN = 'Manually set the API Token if youre not running through heroku or have not set vars in ENV'
        UNFURL = 'FALSE'
        ###############################################################


def parse_join(message):
        m = json.loads(message)
        if m['type'] == "team_join":
                x = requests.get(
                        "https://slack.com/api/im.open",
                        params=dict(
                                token=TOKEN,
                                user=m["user"]["id"]
                        )
                )
                x = x.json()
                x = x["channel"]["id"]
                xx = requests.post(
                        "https://slack.com/api/chat.postMessage",
                        data=dict(
                                token=TOKEN,
                                channel=x,
                                text=MESSAGE,
                                parse="full",
                                as_user=True,
                                unfurl_links=(UNFURL.lower() == "true")
                        )
                )
        elif m['type'] == 'message' and m['text'] == '!welcome':
                x = m["channel"]
                xx = requests.post(
                        "https://slack.com/api/chat.postMessage",
                        data=dict(
                                token=TOKEN,
                                channel=x,
                                text=MESSAGE,
                                parse="full",
                                as_user=True,
                                unfurl_links=(UNFURL.lower() == "true")
                        )
                )


#Connects to Slacks and initiates socket handshake
def start_rtm():
        r = requests.get(
                "https://slack.com/api/rtm.start?token="+TOKEN, verify=False
        )
        r = r.json()
        r = r["url"]
        return r


def on_message(ws, message):
        parse_join(message)


def on_error(ws, error):
        print "SOME ERROR HAS HAPPENED", error


def on_close(ws):
        print '\033[91m'+"Connection Closed"+'\033[0m'


def on_open(ws):
        print "Connection Started - Auto Greeting new joiners to the network"


if __name__ == "__main__":
        r = start_rtm()
        ws = websocket.WebSocketApp(r, on_message = on_message, on_error = on_error, on_close = on_close)
        #ws.on_open
        ws.run_forever()
