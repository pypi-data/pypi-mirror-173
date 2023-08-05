from selenium.common.exceptions import *
from urllib.error import URLError

# --- Exceptions Python ---- #
class EmailOuLoginIncorretoException(Exception):
    pass
# --- Exceptions Python ---- #


# --- Exceptions urllib Base ---- #
class ErroNaURLUrllib(URLError):
    pass


