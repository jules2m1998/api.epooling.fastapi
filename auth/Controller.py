from sqlalchemy.orm import Session
from auth.models import Account
from exception import not_found_404


class Controller:
    @staticmethod
    def get_username(db: Session, username: str) -> Account:
        _a = db.query(Account).filter(Account.username == username).first()
        if _a is None:
            raise not_found_404
        return _a
