from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base

# Association table for the many-to-many relationship between User and PollOption (via Vote)
# This is not strictly necessary as Vote is a model itself, but good for explicit understanding
# vote_association_table = Table(
#     'vote_association',
#     Base.metadata,
#     Column('user_id', Integer, ForeignKey('users.id')),
#     Column('poll_option_id', Integer, ForeignKey('poll_options.id'))
# )

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True)
    passwordHash = Column(String(255))

    polls = relationship("Poll", back_populates="creator")
    votes = relationship("Vote", back_populates="voter")

class Poll(Base):
    __tablename__ = "polls"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(255), index=True)
    isPublished = Column(Boolean, default=False)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now())
    creator_id = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", back_populates="polls")
    options = relationship("PollOption", back_populates="poll", cascade="all, delete-orphan")

class PollOption(Base):
    __tablename__ = "poll_options"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255))
    poll_id = Column(Integer, ForeignKey("polls.id"))

    poll = relationship("Poll", back_populates="options")
    votes = relationship("Vote", back_populates="poll_option", cascade="all, delete-orphan")

class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    poll_option_id = Column(Integer, ForeignKey("poll_options.id"))

    voter = relationship("User", back_populates="votes")
    poll_option = relationship("PollOption", back_populates="votes")
