from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

# https://docs.sqlalchemy.org/en/14/core/metadata.html#sqlalchemy.schema.Column


class BoardsModels:

    def __init__(self, bbs_app):

        self.bbs_app = bbs_app

        class Board(self.bbs_app.Base):
            __tablename__ = "boards"

            # id = Column(Integer, primary_key=True, index=True)
            boardname = Column(String, primary_key=True, unique=True,
                               index=True, nullable=False)

        self.bbs_app.models.Board = Board
        # TODO: set a namespace here to avoid conflicts

        # end of __init__()
