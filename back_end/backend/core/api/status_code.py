"""
保存返回值的状态码和返回信息
"""


class HttpStatusCode:
    """
    HTTP 状态码
    """
    RET_SUCCESS = 200
    RET_GENERAL_ERROR = 400
    RET_AUTH_FAILED = 401
    RET_PERM_DENIED = 403
    RET_OTHER_ERROR = 405


class RetStatusCode:
    """
    细分的json中传输的状态码
    """
    STAT_SUCCESS = 20000

    STAT_INVALID_JSON = 40001
    STAT_DATA_INVALID = 40002
    STAT_USERNAME_DUPLICATED = 40003
    STAT_USER_NON_EXIST = 40004
    STAT_ENTITY_NON_EXIST = 40005
    STAT_ENTITY_DUPLICATED = 40006

    STAT_LOGIN_REQUIRED = 40101
    STAT_AUTH_INVALID = 40103

    STAT_PERM_DENIED = 40301

    STAT_GENERAL_OTHER_ERR = 40500


class RetMessage:
    """
    json中返回的信息
    """
    MSG_SUCCESS = "Operation succeed"

    MSG_METHOD_INVALID = "Method is invalid"
    MSG_DATA_INVALID = "Data is invalid"
    MSG_USERNAME_DUPLICATED = "Duplicated username"
    MSG_USER_NON_EXIST = "User does not exists"
    MSG_ENTITY_NON_EXIST = "Entity does not exists"

    MSG_LOGIN_SUCCESS = "Login succeeded"
    MSG_LOGIN_LOGIN_REQUIRED = "Token is invalid"
    MSG_LOGIN_JSON_INVALID = "JSON is invalid"
    MSG_LOGIN_AUTH_INVALID = "Username or password is invalid"
    MSG_PERM_STAFF_NEEDED = "Permission denied"

    MSG_UNKNOWN_ERROR = "Unknown Error"
