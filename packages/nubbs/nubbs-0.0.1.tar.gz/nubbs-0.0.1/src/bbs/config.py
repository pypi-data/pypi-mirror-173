from pydantic import BaseModel


class ExtensionConfigBase(BaseModel):
    extension: str
    route_prefix: str
    uri: str


class BBSConfigBase(BaseModel):
    uri: str
    # plugins: list[str] = ["users"]
    extensions: dict = {
            "boards_default": {
                "extension": "bbs.ext.boards.BoardsExtension",
                "route_prefix": "/boards"
            },
            "users_default": {
                "extension": "bbs.ext.users.UsersExtension",
                "route_prefix": "/users"
            },
        }