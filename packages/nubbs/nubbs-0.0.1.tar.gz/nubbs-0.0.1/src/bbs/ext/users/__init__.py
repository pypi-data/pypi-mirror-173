from fastapi import FastAPI
from fastapi import APIRouter

from ... import L
from ...core import BBS
from ...extensionbase import BBSExtensionBase

from .config import UsersConfig
from .crud import UsersCRUD
from .models import UsersModels
from .routes import UsersRoutes
from .schemas import UsersSchemas


class UsersExtension(BBSExtensionBase):

    api: FastAPI
    bbs_app: BBS
    config: UsersConfig
    # config_class = UsersConfig
    crud: UsersCRUD
    extension: str
    models: UsersModels
    # schemas: UsersSchemas
    route_prefix: str
    router: APIRouter

    def __init__(self, uri, config, *args, **kwargs):

        users_config_data = {
            "uri": uri,
            "extension": config['extension'],
            "route_prefix": "/users"
        }

        users_config = UsersConfig(**users_config_data|config)
        L("users_config_dict", users_config.dict())

        super().__init__(uri=uri, config=users_config, *args, **kwargs)

        self.models = UsersModels(bbs_app=self.bbs_app)
        self.schemas = UsersSchemas(bbs_app=self.bbs_app)
        self.crud = UsersCRUD(bbs_app=self.bbs_app)
        self.routes = UsersRoutes(bbs_app=self.bbs_app, crud=self.crud,
                                  router=self.router, schemas=self.schemas)

        # end of __init__


