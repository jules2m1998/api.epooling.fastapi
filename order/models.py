from utils import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, Boolean
from config import Base


class Order(BaseModel, Base):
    __tablename__ = 'order'

    is_accepted = Column(Boolean, default=False)
    is_delivered_agent = Column(Boolean, default=False)
    is_delivered_client = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey('user.id'))
    announce_id = Column(Integer, ForeignKey('announce.id'))

    user = relationship('User', single_parent=True, uselist=False)
    announce = relationship('Announce', single_parent=True, uselist=False)
