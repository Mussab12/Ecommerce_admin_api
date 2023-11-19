from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session
from db import database


db_dependency=Annotated[Session,Depends(database.get_db)]        
