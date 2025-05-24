from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dbs import models, database
from dbs.hash import hash_password
from pydantic import BaseModel, EmailStr, constr
from typing import Optional, Annotated


PasswordType = Annotated[str, constr(min_length=8)]

class AdminCreate(BaseModel):
    company_name: str
    company_code: str
    admin_email: EmailStr
    password: Optional[PasswordType] = None

class AdminUpdate(BaseModel):
    company_name: Optional[str] = None
    admin_email: Optional[EmailStr] = None
    password: Optional[PasswordType] = None
    is_active: Optional[bool] = None

class AdminResponse(BaseModel):
    id: int
    company_name: str
    company_code: str
    admin_email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True

router = APIRouter(prefix="/admin", tags=["Admin"])

def get_db():
    db = database.sessionlocal()
    try:
        yield db
    finally:
        db.close()



# ✅ Create admin
@router.post("/", response_model=AdminResponse)
def create_admin(data: AdminCreate, db: Session = Depends(get_db)):
    existing = db.query(models.CompanyAdmin).filter(
        (models.CompanyAdmin.admin_email == data.admin_email) |
        (models.CompanyAdmin.company_code == data.company_code)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email or company code already exists")
    
    new_admin = models.CompanyAdmin(
        company_name=data.company_name,
        company_code=data.company_code,
        admin_email=data.admin_email,
        password_hash=hash_password(data.password)
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin



# ✅ Update admin
@router.put("/{admin_id}", response_model=AdminResponse)
def update_admin(admin_id: int, data: AdminUpdate, db: Session = Depends(get_db)):
    admin = db.query(models.CompanyAdmin).get(admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    if data.company_name:
        admin.company_name = data.company_name
    if data.admin_email:
        admin.admin_email = data.admin_email
    if data.password:
        admin.password_hash = hash_password(data.password)
    if data.is_active is not None:
        admin.is_active = data.is_active

    db.commit()
    db.refresh(admin)
    return admin



# ✅ Delete admin
@router.delete("/{admin_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin(admin_id: int, db: Session = Depends(get_db)):
    admin = db.query(models.CompanyAdmin).get(admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    db.delete(admin)
    db.commit()
    return
