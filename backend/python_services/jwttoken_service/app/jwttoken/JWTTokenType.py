from enum import StrEnum


class JWTTokenType(StrEnum):
    ACCESS = 'ACCESS'
    REFRESH = 'REFRESH'
    