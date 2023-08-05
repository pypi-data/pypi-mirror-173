from sqlalchemy import Boolean, Column, ForeignKey, Integer, String


class UsersModels:

    def __init__(self, bbs_app):

        self.bbs_app = bbs_app

        class User(self.bbs_app.Base):
            __tablename__ = "users"

            id = Column(Integer, primary_key=True, index=True)
            username = Column(String, unique=True, index=True)
            password = Column(String)

        self.bbs_app.models.User = User
        # TODO: set a namespace here to avoid conflicts

        # end of __init__()
