import importlib

from fastapi import FastAPI

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import BBSConfigBase
from .config import ExtensionConfigBase

from .extensionbase import BBSExtensionBase

from . import L

# class Models: pass
# class Schemas: pass

class BBS:

    api: FastAPI
    config: BBSConfigBase
    extension_registry: list = list()
    extensions: dict = dict()
    # models: Models = Models()
    # schemas: Schemas = Schemas()
    uri: str

    def __init__(self, bbs_config: BBSConfigBase):

        self.api = FastAPI()
        self.config: BBSConfigBase = bbs_config

        class Models: pass
        self.models = Models()

        class Schemas: pass
        self.schemas = Schemas()

        SQLALCHEMY_DATABASE_URL = f"sqlite:///./{bbs_config.uri}.sqlite3"

        self.engine = create_engine(
            url=SQLALCHEMY_DATABASE_URL,
            connect_args={"check_same_thread": False}
        )

        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False,
                                         bind=self.engine)

        self.Base = declarative_base()

        self._register_extensions(self.config)

        self.Base.metadata.create_all(bind=self.engine)

        L("extension registry", self.extension_registry)
        L("EXTENSION CONFIG REGISTRY", self.extension_config_registry)
        L("extensions", self.extensions)

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def _register_extensions(self, bbs_config: BBSConfigBase):

        for extension_uri, extension_config in bbs_config.extensions.items():

            extension_str = extension_config['extension']
            extension_module_str, extension_class_str = \
                extension_str.rsplit('.', maxsplit=1)

            extension_module = importlib.import_module(extension_module_str)
            extension_class = getattr(extension_module, extension_class_str)

            self._instatiate_extension(extension_class=extension_class,
                                       extension_uri=extension_uri,
                                       extension_config=extension_config)

        self.extension_registry = BBSExtensionBase.__subclasses__()
        self.extension_config_registry = ExtensionConfigBase.__subclasses__()


    def _instatiate_extension(self, extension_class: BBSExtensionBase,
                              extension_uri: str,
                              extension_config: dict):

        extension_instance = extension_class(bbs_application=self,
                                             uri=extension_uri,
                                             config=extension_config)

        self.extensions.update({extension_uri: extension_instance})

        L("Including router at", extension_instance.router.prefix)
        self.api.include_router(extension_instance.router)

