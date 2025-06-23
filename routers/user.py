from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from .auth import user_dependency,db_dependency
from dbs.models import Employee

router = APIRouter(
    prefix='/user',
    tags=['User']
)

class UserDetailsResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str


@router.get("/user_details/", status_code=status.HTTP_200_OK)
async def get_user_details(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Employee).filter(Employee.employeeID == user.get('id')).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserDetailsResponse(
        id=user_model.employeeID,
        first_name=user_model.firstName,
        last_name=user_model.lastName,
        email=user_model.email,
    )