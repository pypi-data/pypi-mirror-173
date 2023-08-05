from sqlalchemy.orm import Session

from ...core import BBS

class BoardsCRUD:

    def __init__(self, bbs_app: BBS):

        self.bbs_app = bbs_app

        models = self.bbs_app.models
        schemas = self.bbs_app.schemas

        def register_crud_function(f):
            setattr(self, f.__name__, f)

        @register_crud_function
        def get_board(db: Session, board_id: str):
            Board = models.Board

            return (
                db
                .query(Board)
                .filter(Board.boardname == board_id)
                .first()
            )

        @register_crud_function
        def get_board_by_boardname(db: Session, boardname: str):
            Board = models.Board

            return (
                db .query(Board)
                .filter(Board.boardname == boardname)
                .first()
            )

        @register_crud_function
        # def get_boards(self, db: Session, skip: int = 0, limit: int = 100):
        def get_boards(db: Session, skip: int = 0, limit: int = 100):
            Board = models.Board

            return (
                db
                .query(Board)
                .offset(skip)
                .limit(limit)
                .all()
            )

        @register_crud_function
        def create_board(db: Session, board: schemas.BoardCreate):
            Board = models.Board

            db_board = Board(boardname=board.boardname)

            db.add(db_board)
            db.commit()
            db.refresh(db_board)

            return db_board
