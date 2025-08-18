
import validators
import app.config as conf
import string
import secrets


CODE_CHARS = string.ascii_lowercase + string.ascii_uppercase + string.digits
CODE_LENGTH = 6

def ival_code(ival:int) -> str:
    res = []
    while ival > 0:
        ival, rem = divmod(ival, len(CODE_CHARS))
        res.append(CODE_CHARS[rem])
    res.reverse()
    return "".join(res).zfill(CODE_LENGTH)


def random_code():
    return "".join(secrets.choice(CODE_CHARS) for _ in range(CODE_LENGTH))


def is_valid_url(url:str) -> bool:
    return validators.url(url) is True


def make_short_url(code):
    return conf.SHORT_URL_BASE + "/" + code
