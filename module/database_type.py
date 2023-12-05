import enum

class Domain(enum.Enum):
    HTTP = 0
    HTTPS = 1

class Url(enum.Enum):
    SYSTEM = 0
    CUSTOM = 1