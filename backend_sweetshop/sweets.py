from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
import models, database, schemas
from jose import jwt, JWTError
from typing import List

router = APIRouter(prefix="/api/sweets", tags=["sweets"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(models.User).filter(models.User.username == username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# -----------------------
# Add Sweet (Admin only)
# -----------------------
@router.post("", response_model=schemas.SweetResponse)
def add_sweet(
    sweet: schemas.SweetCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Admin-only restriction
    if not getattr(current_user, "is_admin", 0):
        raise HTTPException(status_code=403, detail="Only admin users can add sweets")

    db_sweet = models.Sweet(
        name=sweet.name,
        category=sweet.category,
        price=sweet.price,
        quantity=sweet.quantity
    )
    db.add(db_sweet)
    db.commit()
    db.refresh(db_sweet)
    return db_sweet

# -----------------------
# List Sweets (All users)
# -----------------------
@router.get("", response_model=List[schemas.SweetResponse])
def list_sweets(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    sweets = db.query(models.Sweet).all()
    return sweets
    
@router.get("/search", response_model=List[schemas.SweetResponse])
def search_sweets(
    name: str = None,
    category: str = None,
    min_price: float = None,
    max_price: float = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.Sweet)

    if name:
        query = query.filter(models.Sweet.name.ilike(f"%{name}%"))
    if category:
        query = query.filter(models.Sweet.category.ilike(f"%{category}%"))
    if min_price is not None:
        query = query.filter(models.Sweet.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Sweet.price <= max_price)

    results = query.all()
    return results
    
@router.put("/{sweet_id}", response_model=schemas.SweetResponse)
def update_sweet(
    sweet_id: int,
    sweet: schemas.SweetCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if not getattr(current_user, "is_admin", 0):
        raise HTTPException(status_code=403, detail="Only admin users can update sweets")

    db_sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()
    if not db_sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")

    db_sweet.name = sweet.name
    db_sweet.category = sweet.category
    db_sweet.price = sweet.price
    db_sweet.quantity = sweet.quantity

    db.commit()
    db.refresh(db_sweet)
    return db_sweet
    
# Delete Sweet (Admin only)
@router.delete("/{sweet_id}")
def delete_sweet(
    sweet_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Only admin can delete
    if not getattr(current_user, "is_admin", 0):
        raise HTTPException(status_code=403, detail="Only admin users can delete sweets")

    db_sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()
    if not db_sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")

    db.delete(db_sweet)
    db.commit()
    return {"detail": "Sweet deleted successfully"}
    
# ------------------------
# Purchase Sweet (All users)
# ------------------------
@router.post("/{sweet_id}/purchase", response_model=schemas.SweetResponse)
def purchase_sweet(
    sweet_id: int,
    payload: dict,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    quantity = payload.get("quantity")
    if quantity is None or quantity <= 0:
        raise HTTPException(status_code=400, detail="Invalid purchase quantity")

    sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    if sweet.quantity < quantity:
        raise HTTPException(status_code=400, detail="Not enough quantity available")

    sweet.quantity -= quantity
    db.commit()
    db.refresh(sweet)
    return sweet

# ------------------------
# Restock Sweet (Admin only)
# ------------------------
@router.post("/{sweet_id}/restock", response_model=schemas.SweetResponse)
def restock_sweet(
    sweet_id: int,
    payload: dict,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if not getattr(current_user, "is_admin", 0):
        raise HTTPException(status_code=403, detail="Only admin users can restock sweets")

    quantity = payload.get("quantity")
    if quantity is None or quantity <= 0:
        raise HTTPException(status_code=400, detail="Invalid restock quantity")

    sweet = db.query(models.Sweet).filter(models.Sweet.id == sweet_id).first()
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")

    sweet.quantity += quantity
    db.commit()
    db.refresh(sweet)
    return sweet


