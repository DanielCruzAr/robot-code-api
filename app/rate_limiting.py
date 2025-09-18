from slowapi import Limiter
from slowapi.util import get_remote_address

# TODO: Configure rate limiting as needed
limiter = Limiter(key_func=get_remote_address)