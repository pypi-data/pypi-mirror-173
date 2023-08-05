import logging
from rich.logging import RichHandler

DEBUG = True
DEFAULT_HOST = "127.0.0.1"  # localhost only
DEFAULT_PORT = 8000
PACKAGE_NAME = "bbs"

from functools import partial, partialmethod

logging.BBS = 5
logging.addLevelName(logging.BBS, 'BBS')
logging.Logger.bbs = partialmethod(logging.Logger.log, logging.BBS)
logging.bbs = partial(logging.log, logging.BBS)

handler_list = [RichHandler(rich_tracebacks=True)]

uv = logging.getLogger("uvicorn")
uv.handlers = [RichHandler(rich_tracebacks=True)]
uv.propagate = False

uvacc = logging.getLogger("uvicorn.access")
uvacc.handlers = [RichHandler(rich_tracebacks=True)]
uvacc.propagate = False

uverr = logging.getLogger("uvicorn.error")
uverr.handlers = [RichHandler(rich_tracebacks=True)]
uverr.propagate = False

LOGGER = logging.getLogger(__name__)
LOGGER.handlers = [RichHandler(rich_tracebacks=True)]
LOGGER.propagate = False
LOGGER.setLevel(logging.BBS)

def L(*args):
    LOGGER.bbs(" ".join([str(x) for x in args]))
















