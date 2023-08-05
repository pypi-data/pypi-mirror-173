from fastapi import FastAPI
from fastapi import APIRouter

from .config import ExtensionConfigBase

# import core
# from .core import BBS

BBS = None


class BBSExtensionBase:

    api: FastAPI
    bbs_app: BBS
    config: ExtensionConfigBase
    extension: str
    extension_module: str
    extension_class: str
    route_prefix: str
    router: APIRouter
    uri: str

    def __init__(self, bbs_application: BBS,
                 uri: str,
                 config: ExtensionConfigBase,
                 *args, **kwargs):

        self.bbs_app = bbs_application
        self.api = bbs_application.api
        self.config = config

        self.extension = config.extension
        self.extension_module, self.extension_class = \
            self.extension.rsplit('.', maxsplit=1)

        self.route_prefix = config.route_prefix
        self.router = APIRouter(prefix=self.route_prefix,
                                tags=[self.config.uri])
        self.uri: str = uri

    def __call__(self, *args, **kwargs):
        # so that PyCharm stops complaining.
        pass