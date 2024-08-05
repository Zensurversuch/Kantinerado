from enum import Enum

API_MESSAGE_DESCRIPTOR = "response"

class get_api_messages(Enum):
    SUCCESS = "Erfolgreich: "
    WARNING = "Warnung: "
    ERROR = "Fehler: "