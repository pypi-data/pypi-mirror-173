from fastapi import Depends, HTTPException
''
from sqlalchemy.orm import Session

class BoardsRoutes:

    def __init__(self, bbs_app, crud, router, schemas):

        self.bbs_app = bbs_app

        @router.post("/", response_model=schemas.Board)
        def create_board(board: schemas.BoardCreate,
                         db: Session = Depends(self.bbs_app.get_db)):

            db_board = \
                crud.get_board_by_boardname(db, boardname=board.boardname)
            if db_board:
                raise HTTPException(status_code=400,
                                    detail="Boardname already registered")
            return crud.create_board(db=db, board=board)

        @router.get("/", response_model=list[schemas.Board])
        def read_boards(skip: int = 0, limit: int = 100,
                        db: Session = Depends(self.bbs_app.get_db)):
            boards = crud.get_boards(db, skip=skip, limit=limit)
            return boards

        @router.get("/{board_id}", response_model=schemas.Board)
        def read_board(board_id: str,
                       db: Session = Depends(self.bbs_app.get_db)):
            # db_board = crud.get_board(db, board_id=board_id)
            db_board = crud.get_board(db, board_id=board_id)
            if db_board is None:
                raise HTTPException(status_code=404, detail="Board not found")
            return db_board
