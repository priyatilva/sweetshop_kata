from sqlalchemy.orm import Session
import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        email=user.email,
        password=user.password  # NOTE: Later we'll hash passwords
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
