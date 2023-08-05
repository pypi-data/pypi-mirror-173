from pydantic import BaseModel


class BoardsSchemas:

    def __init__(self, bbs_app):

        self.bbs_app = bbs_app

        class BoardBase(BaseModel):
            boardname: str

        class BoardCreate(BoardBase):
            # boardname: str (from BoardBase)
            pass

        class Board(BoardBase):
            # boardname: str (from BoardBase)
            pass

            class Config:
                orm_mode = True

            # items: list[Item] = []

        self.BoardBase = BoardBase
        self.BoardCreate = BoardCreate
        self.Board = Board

        self.bbs_app.schemas.BoardBase = BoardBase
        self.bbs_app.schemas.BoardCreate = BoardCreate
        self.bbs_app.schemas.Board = Board

