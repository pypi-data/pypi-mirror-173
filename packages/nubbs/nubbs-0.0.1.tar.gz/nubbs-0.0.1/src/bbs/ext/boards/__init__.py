from fastapi import FastAPI
from fastapi import APIRouter
# from fastapi import Depends, HTTPException

# from sqlalchemy.orm import Session

from ... import L
from ...core import BBS
from ...extensionbase import BBSExtensionBase

from .config import BoardsConfig
from .crud import BoardsCRUD
from .models import BoardsModels
from .routes import BoardsRoutes
from .schemas import BoardsSchemas


class BoardsExtension(BBSExtensionBase):

    api: FastAPI
    bbs_app: BBS
    config: BoardsConfig
    # config_class = BoardsConfig
    crud: BoardsCRUD
    extension: str
    models: BoardsModels
    # schemas: BoardsSchemas
    route_prefix: str
    router: APIRouter

    def __init__(self, uri, config, *args, **kwargs):

        boards_config_data = {
            "uri": uri,
            "extension": config['extension'],
            "route_prefix": "/boards"
        }

        boards_config = BoardsConfig(**boards_config_data|config)
        L("boards_config_dict", boards_config.dict())

        super().__init__(uri=uri, config=boards_config, *args, **kwargs)

        self.models = BoardsModels(bbs_app=self.bbs_app)
        self.schemas = BoardsSchemas(bbs_app=self.bbs_app)
        self.crud = BoardsCRUD(bbs_app=self.bbs_app)
        self.routes = BoardsRoutes(bbs_app=self.bbs_app, crud=self.crud,
                                   router=self.router, schemas=self.schemas)

        # schemas = self.schemas


        # @self.router.post("/", response_model=schemas.Board)
        # def create_board(board: schemas.BoardCreate,
        #                 db: Session = Depends(self.bbs_app.get_db)):
        #
        #     db_board = \
        #         self.crud.get_board_by_boardname(db, boardname=board.boardname)
        #     if db_board:
        #         raise HTTPException(status_code=400,
        #                             detail="Boardname already registered")
        #     return self.crud.create_board(db=db, board=board)
        #
        # @self.router.get("/", response_model=list[schemas.Board])
        # def read_boards(skip: int = 0, limit: int = 100,
        #                db: Session = Depends(self.bbs_app.get_db)):
        #     boards = self.crud.get_boards(db, skip=skip, limit=limit)
        #     return boards
        #
        # @self.router.get("/{board_id}", response_model=schemas.Board)
        # def read_board(board_id: int,
        #               db: Session = Depends(self.bbs_app.get_db)):
        #     db_board = self.crud.get_board(db, board_id=board_id)
        #     if db_board is None:
        #         raise HTTPException(status_code=404, detail="Board not found")
        #     return db_board

        # end of __init__


