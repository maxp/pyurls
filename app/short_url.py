
import validators
import app.config as conf
import string


CODE_CHARS = string.ascii_lowercase + string.ascii_uppercase + string.digits

def ival_code(ival:int) -> str:
    res = []
    while ival > 0:
        ival, rem = divmod(ival, len(CODE_CHARS))
        res.append(CODE_CHARS[rem])
    return "".join(res).zfill(6)


def is_valid_url(url:str) -> bool:
    return validators.url(url) is True


def make_short_url(code):
    return conf.SHORT_URL_BASE + "/" + code

