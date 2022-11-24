from enum import Enum

URL_BUILD_DETAIL = "builds/{}"
URL_TRIGGER_BUILD = "buildQueue"


class AUTH_METHOD(Enum):
    """Auth method."""
    TOKENS = 'tokens'
    USER = 'user'
    GUEST = 'guest'
    LOGGED_IN = 'logged_in'
