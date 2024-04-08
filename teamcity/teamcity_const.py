from enum import Enum

URL_BUILD_DETAIL = "builds/{}"
URL_TRIGGER_BUILD = "buildQueue"


class AuthMethod(Enum):
    """Auth method."""
    TOKENS = 'tokens'
    USER = 'user'
    GUEST = 'guest'
    LOGGED_IN = 'logged_in'


class RequestMethod(Enum):
    """Request method."""
    GET = 'GET'
    POST = 'POST'


class RequestReturnType(Enum):
    """Request return type."""
    JSON = 'json'
    TEXT = 'text'
    FILE = 'file'
    NONE = 'none'
