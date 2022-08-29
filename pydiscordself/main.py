import websocket
import json
import threading
import time
import requests
import datetime

from .errors import *

'''

A faire :
    Slash Commands
    Couper le code 
    Mettre des réations
    Modif la bio
    Vocal

A modif : 

Bug : 
    Rich Presence -> Bouttons

'''




class Activities:
    def __init__(self):
        self.GAME = 0
        self.STREAMING = 1
        self.LISTENING = 2
        self.WATCHING = 3
        self.CUSTOM = 4
        self.COMPETING = 5

class RichPresence:
    def __init__(self, type, name):
        self.type = type
        self.name = name
        self.buttons = []
        self.partys = []

    def set_url(self, url):
        if self.type != 1:
            raise RichPresenceSetUrlWrongType()
        self.url = url

    def add_button(self, button):
        if len(self.buttons) == 2:
            raise RichPresenceMaxButtonLimitExcepted()

        self.buttons.append(button)

    def set_emoji(self, emoji):
        self.emoji = emoji
    
    def set_assets(self, assets):
        self.assets = assets
    
    def set_state(self, state):
        self.state = state

    def set_details(self, details):
        self.details = details

    def add_party(self, party):
        if len(self.partys) == 2:
            raise RichPresenceMaxPartysLimitExcepted()

        self.partys.append(party)
    
    def set_created_at(self, created_at):
        self.created_at = created_at

    def set_timestamp(self, start = None, end = None):
        d = {}
        if start != None:
            d["start"] = start
        if end != None:
            d["end"] = end

        self.timestamp = d

    def compile(self):
        d = {
            "name": self.name,
            "type": self.type
        }

        for x in ["url", "buttons", "emoji", "assets", "partys", "created_at", "details", "state"]:
            if hasattr(self, x) and getattr(self, x) != []:
                d[x] = getattr(self, x)

        return d


class SelfBot:
    def __init__(self, token, intents = 3276799):
        self.token = token
        self.intents = intents

        self.run = False
        self.events = {
            "READY": [],
            "ERROR": [],
            "MESSAGE_CREATE": [],
            "MESSAGE_DELETE": [],
            "MESSAGE_DELETE_BULK": [],
            "MESSAGE_REACTION_ADD": [],
            "MESSAGE_REACTION_REMOVE": [],
            "MESSAGE_REACTION_REMOVE_ALL": [],
            "MESSAGE_REACTION_REMOVE_EMOJI": [],
            "MESSAGE_UPDATE": [],
            "THREAD_CREATE": [],
            "THREAD_UPDATE": [],
            "THREAD_DELETE": [],
            "THREAD_MEMBER_UPDATE": [],
            "THREAD_MEMBERS_UPDATE": [],
            "CHANNEL_CREATE": [],
            "CHANNEL_DELETE": [],
            "CHANNEL_UPDATE": [],
            "GUILD_CREATE": [],
            "GUILD_DELETE": [],
            "GUILD_EMOIJ_CREATE": [],
            "GUILD_EMOIJ_DELETE": [],
            "GUILD_EMOIJ_UPDATE": [],
            "GUILD_MEMBER_ADD": [],
            "GUILD_MEMBER_REMOVE": [],
            "GUILD_BAN_ADD": [],
            "GUILD_BAN_REMOVE": [],
            "PRESENCE_UPDATE": [],
            "VOICE_STATE_UPDATE": [],
            "USER_SETTINGS_UPDATE": [],
            "USER_SETTINGS_PROTO_UPDATE": [],
            "USER_NOTE_UPDATE": [],
            "MESSAGE_ACK": [],
            "GUILD_JOIN_REQUEST_CREATE": [],
            "GUILD_MEMBER_UPDATE": [],
            "SESSIONS_REPLACE": [],
            "INTERACTION_CREATE": [],
            "INTERACTION_FAILURE": []
        }

        self.debug = False

    def start(self):
        self.run = True
        self.ws = websocket.WebSocketApp("wss://gateway.discord.gg/?v=10&encording=json",
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        self.ws.run_forever()

    def on_error(self, ws, error):
        print("[{}][{}] {}".format(datetime.datetime.now(), "ERROR", error))

    def on_close(self, ws, one, two):
        print("[{}][{}] {}".format(datetime.datetime.now(), "INFOS", "Disconnected from discord api ..."))
        self.run = False

    def on_open(self, ws):
        print("[{}][{}] {}".format(datetime.datetime.now(), "INFOS", "Connecting to discord api ..."))

    def heartbeat(self, ws, interval):
        while True:
            time.sleep(interval / 1000)
            
            try:
                ws.send(json.dumps({
                    "op": 1,
                    "d": "null"
                }))
            except:
                break

    def on_message(self, ws, message):
        message = json.loads(message)
        if message["op"] == 10:
            threading.Thread(target=self.heartbeat, args=(ws, message["d"]["heartbeat_interval"])).start()
            ws.send(json.dumps({
                "op": 2,
                "d": {
                    "token": self.token,
                    "intents": self.intents,
                    "properties": {
                        "os": "discord-self.py",
                        "browser": "discord-self.py",
                        "device": "discord-self.py"
                    }
                }
            }))

        elif message["op"] == 0:
            if self.debug:
                print("{} => {}\n\n".format(message["t"], message["d"]))
            for event in self.events[message["t"]]:
                event(message["d"])

    def update_status(self, status = "online", activities = [], afk=False):
        if status not in ["online", "dnd", "idle", "invisible", "offline"]:
            raise StatusNotFound()

        activity = {
            "op": 3,
            "d": {
                "since": 0,
                "activities": activities,
                "status": status,
                "afk": afk
            }
        }

        self.ws.send(json.dumps(activity))

    def send_message(self, channel_id, content):
        return requests.post("https://discord.com/api/v10/channels/{}/messages".format(channel_id),
            headers={ "Authorization": self.token },
            json={ "content": content }
        ).json()

    def delete_message(self, channel_id, message_id):
        requests.delete("https://discord.com/api/v10/channels/{}/messages/{}".format(channel_id, message_id),
            headers={ "Authorization": self.token }
        )

    def edit_message(self, channel_id, message_id, content):
        return requests.patch("https://discord.com/api/v10/channels/{}/messages/{}".format(channel_id, message_id),
            headers={ "Authorization": self.token },
            json={ "content": content }
        ).json()

    def addEventListener(self, event_name, function):
        if event_name in self.events.keys():
            if callable(function):
                self.events[event_name].append(function)
            else:
                raise EventFunctionIsNotCallable()
        else:
            raise EventNameNotFound()

    def get_user(self, id):
        return requests.get("https://discord.com/api/v10/users/{}".format(id),
            headers={ "Authorization": self.token }
        ).json()

    def get_current_user(self):
        return requests.get("https://discord.com/api/v10/users/@me".format(id),
            headers={ "Authorization": self.token }
        ).json()