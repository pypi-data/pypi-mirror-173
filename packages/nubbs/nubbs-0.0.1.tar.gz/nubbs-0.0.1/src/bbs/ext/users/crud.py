from sqlalchemy.orm import Session

from ...core import BBS


class UsersCRUD:

    def __init__(self, bbs_app: BBS):

        self.bbs_app = bbs_app

        models = self.bbs_app.models
        schemas = self.bbs_app.schemas

        def register_crud_function(f):
            setattr(self, f.__name__, f)

        @register_crud_function
        def get_user(db: Session, user_id: int):
            User = models.User

            return (
                db
                .query(User)
                .filter(User.id == user_id)
                .first()
            )

        @register_crud_function
        def get_user_by_username(db: Session, username: str):
            User = models.User

            return (
                db .query(User)
                .filter(User.username == username)
                .first()
            )

        @register_crud_function
        def get_users(db: Session, skip: int = 0, limit: int = 100):
            User = models.User

            return (
                db
                .query(User)
                .offset(skip)
                .limit(limit)
                .all()
            )

        @register_crud_function
        def create_user(db: Session, user: schemas.UserCreate):
            User = models.User

            db_user = User(username=user.username,
                           password=user.password)

            db.add(db_user)
            db.commit()
            db.refresh(db_user)

            return db_user
