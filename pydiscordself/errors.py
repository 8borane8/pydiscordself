class EventNameNotFound(Exception):
    def __init__(self):
        print("Raised when the event name is not found")

class EventFunctionIsNotCallable(Exception):
    def __init__(self):
        print("Raised when the function is not callable")

class StatusNotFound(Exception):
    def __init__(self):
        print("Raised when the status argument is not a status")

class WsNotStarted(Exception):
    def __init__(self):
        print("Raised when the ws is off")

class RichPresenceSetUrlWrongType(Exception):
    def __init__(self):
        print("Raised when the url is set on the wrong type")

class RichPresenceMaxButtonLimitExcepted(Exception):
    def __init__(self):
        print("Raised when the buttons limit exepted")

class RichPresenceMaxAssetsLimitExcepted(Exception):
    def __init__(self):
        print("Raised when the assets limit exepted")

class RichPresenceMaxPartysLimitExcepted(Exception):
    def __init__(self):
        print("Raised when the partys limit exepted")