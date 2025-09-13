from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from . import models, schemas

# User CRUD
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    # In a real application, you would hash the password here
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, name=user.name, passwordHash=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Poll CRUD
def get_poll(db: Session, poll_id: int):
    return db.query(models.Poll).options(joinedload(models.Poll.options)).filter(models.Poll.id == poll_id).first()

def get_poll_with_vote_counts(db: Session, poll_id: int):
    poll = db.query(models.Poll).options(joinedload(models.Poll.options)).filter(models.Poll.id == poll_id).first()
    if not poll:
        return None

    # Get vote counts for each option
    option_vote_counts = db.query(
        models.PollOption.id,
        func.count(models.Vote.id).label("vote_count")
    ).join(models.Vote, models.PollOption.id == models.Vote.poll_option_id, isouter=True)
    option_vote_counts = option_vote_counts.filter(models.PollOption.poll_id == poll_id)
    option_vote_counts = option_vote_counts.group_by(models.PollOption.id).all()

    vote_counts_map = {option_id: count for option_id, count in option_vote_counts}

    # Attach vote counts to poll options
    for option in poll.options:
        option.votes_count = vote_counts_map.get(option.id, 0)

    return poll

def create_poll(db: Session, poll: schemas.PollCreate, creator_id: int):
    db_poll = models.Poll(question=poll.question, isPublished=poll.isPublished, creator_id=creator_id)
    db.add(db_poll)
    db.commit()
    db.refresh(db_poll)

    for option_data in poll.options:
        db_option = models.PollOption(**option_data.model_dump(), poll_id=db_poll.id)
        db.add(db_option)
    db.commit()
    db.refresh(db_poll)
    return db_poll

# Vote CRUD
def create_user_vote(db: Session, vote: schemas.VoteCreate, user_id: int):
    # Check if the user has already voted for this poll (assuming one vote per user per poll)
    # This logic needs to be refined based on whether a user can change their vote or vote on multiple options
    # For simplicity, let's assume one vote per user per poll for now.
    
    # First, find the poll_id from the poll_option_id
    poll_option = db.query(models.PollOption).filter(models.PollOption.id == vote.poll_option_id).first()
    if not poll_option:
        return None # Option not found

    # Check if the user has already voted in this poll
    existing_vote = db.query(models.Vote)
    existing_vote = existing_vote.join(models.PollOption)
    existing_vote = existing_vote.filter(
        models.Vote.user_id == user_id,
        models.PollOption.poll_id == poll_option.poll_id
    ).first()

    if existing_vote:
        # User already voted in this poll, update their vote
        existing_vote.poll_option_id = vote.poll_option_id
        db.commit()
        db.refresh(existing_vote)
        return existing_vote
    else:
        # Create a new vote
        db_vote = models.Vote(user_id=user_id, poll_option_id=vote.poll_option_id)
        db.add(db_vote)
        db.commit()
        db.refresh(db_vote)
        return db_vote
