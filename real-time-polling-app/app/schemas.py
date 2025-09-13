from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List, Optional

# User Schemas
class UserBase(BaseModel):
    name: str = Field(..., max_length=255)
    email: EmailStr = Field(..., max_length=255)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

# PollOption Schemas
class PollOptionBase(BaseModel):
    text: str = Field(..., max_length=255)

class PollOptionCreate(PollOptionBase):
    pass

class PollOption(PollOptionBase):
    id: int
    poll_id: int
    votes_count: int = 0 # To be populated when retrieving poll results

    class Config:
        from_attributes = True

# Poll Schemas
class PollBase(BaseModel):
    question: str = Field(..., max_length=255)
    isPublished: bool = False

class PollCreate(PollBase):
    options: List[PollOptionCreate]

class Poll(PollBase):
    id: int
    createdAt: datetime
    updatedAt: Optional[datetime]
    creator_id: int
    options: List[PollOption] = []

    class Config:
        from_attributes = True

# Vote Schemas
class VoteBase(BaseModel):
    poll_option_id: int

class VoteCreate(VoteBase):
    pass

class Vote(VoteBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
