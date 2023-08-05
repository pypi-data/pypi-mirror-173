from pydantic import BaseModel


class UsersSchemas:

    def __init__(self, bbs_app):

        self.bbs_app = bbs_app

        class UserBase(BaseModel):
            username: str

        class UserCreate(UserBase):
            # username: str (from UserBase)
            password: str

        class User(UserBase):
            # username: str (from UserBase)
            id:  int

            class Config:
                orm_mode = True

            # items: list[Item] = []

        self.UserBase = UserBase
        self.UserCreate = UserCreate
        self.User = User

        self.bbs_app.schemas.UserBase = UserBase
        self.bbs_app.schemas.UserCreate = UserCreate
        self.bbs_app.schemas.User = User

# class UserBase(BaseModel):
#     username: str
#
#
# class UserCreate(UserBase):
#     # username: str (from UserBase)
#     password: str
#
#
# class User(UserBase):
#     # username: str (from UserBase)
#     id:  int
#
#     class Config:
#         orm_mode = True
#
#     # items: list[Item] = []
