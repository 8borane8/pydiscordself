
# PyDiscordSelf

pydiscordself est une librairie python pour la création de vos self bots qui est open source. Ce répo contient la documentation officielle de pydiscordself et quelques exemples ...


## Documentation

Exemple de code  
```python
from pydiscordself import SelfBot
import json

selfbot = SelfBot(json.load(open("config.json", "r"))["TOKEN"])


def on_ready(arg):
    print("{}#{} is ready".format(selfbot.get_current_user()["username"], selfbot.get_current_user()["discriminator"]))

selfbot.addEventListener("READY", on_ready)

selfbot.start()
```

### Events
Voici la liste de tous les évenements : 
```
    READY => 
    ERROR => 
    MESSAGE_CREATE => 
    MESSAGE_DELETE => 
    MESSAGE_DELETE_BULK => 
    MESSAGE_REACTION_ADD => 
    MESSAGE_REACTION_REMOVE => 
    MESSAGE_REACTION_REMOVE_ALL => 
    MESSAGE_REACTION_REMOVE_EMOJI => 
    MESSAGE_UPDATE => 
    THREAD_CREATE => 
    THREAD_UPDATE => 
    THREAD_DELETE => 
    THREAD_MEMBER_UPDATE => 
    THREAD_MEMBERS_UPDATE => 
    CHANNEL_CREATE => 
    CHANNEL_DELETE => 
    CHANNEL_UPDATE => 
    GUILD_CREATE => 
    GUILD_DELETE => 
    GUILD_EMOIJ_CREATE => 
    GUILD_EMOIJ_DELETE => 
    GUILD_EMOIJ_UPDATE => 
    GUILD_MEMBER_ADD => 
    GUILD_MEMBER_REMOVE => 
    GUILD_BAN_ADD => 
    GUILD_BAN_REMOVE => 
    PRESENCE_UPDATE => 
    VOICE_STATE_UPDATE => 
    USER_SETTINGS_UPDATE => 
    USER_SETTINGS_PROTO_UPDATE => 
    USER_NOTE_UPDATE => 
    MESSAGE_ACK => 
    GUILD_JOIN_REQUEST_CREATE => 
    GUILD_MEMBER_UPDATE => 
    SESSIONS_REPLACE => 
    INTERACTION_CREATE =>
    INTERACTION_FAILURE =>
```
