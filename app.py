from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

# Define the URL for your MySQL database
URL_DATABASE = 'mysql+pymysql://root:Sql#24,my()@localhost:3306/record'

# Create an engine to establish a connection to the database
engine = create_engine(URL_DATABASE, pool_pre_ping=True)

# Create a sessionmaker to create a Session instance
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a base class for declarative table definitions
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    
# Create the table in the database
Base.metadata.create_all(bind=engine)

class LoginRequest(BaseModel):
    userName: str
    password: str

class LoginResponse(BaseModel):
    userName: str
    userId: int
    token: str

class JwtMiddleware:
    def LoginDetails(self, username: str, password: str, db_conn_str: str) -> LoginResponse:
        # For demo purposes, returning a dummy LoginResponse
        return LoginResponse(userName=username, userId=1, token="dummy_token")

    def LoginDetailsXT(self, username: str, password: str, db_conn_str: str) -> LoginResponse:
        # For demo purposes, returning a dummy LoginResponse
        return LoginResponse(userName=username, userId=1, token="dummy_token")

class MySettingsModel(BaseModel):
    DBConn: str

class MySettingsService:
    @staticmethod
    def get_db_connection_string() -> str:
        return URL_DATABASE

class GlobalVariable:
    ClientID = ""  # Define ClientID variable

class CLogger:
    @staticmethod
    def LogError(message: str, exception: Exception):
        # Implement logging logic
        pass

app = FastAPI()

# CORS settings
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to provide a database session to route handlers
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Example route handler to save login details into the database
@app.post("/api/LoginDetails", response_model=List[LoginResponse], status_code=200)
async def login_details(obj: LoginRequest, db: SessionLocal = Depends(get_db)):
    try:
        # Save login details into the database
        login_details = User(username=obj.userName, password=obj.password)
        db.add(login_details)
        db.commit()

        # Perform login logic (for demo purposes, just returning dummy response)
        jwt_middleware = JwtMiddleware()
        login_response = jwt_middleware.LoginDetails(obj.userName.strip(), obj.password.strip(), MySettingsService.get_db_connection_string())
        if login_response is not None:
            return [login_response]
        else:
            raise HTTPException(status_code=400, detail="Invalid Credentials")
    except Exception as ex:
        CLogger.LogError("Something went wrong inside the LoginDetails Autcontroller", ex)
        raise HTTPException(status_code=500, detail="Internal server error")

# Example route handler to save login details XT into the database
@app.post("/api/LoginDetailsXT", response_model=List[LoginResponse], status_code=200)
async def login_details_xt(obj: LoginRequest, db: SessionLocal = Depends(get_db)):
    try:
        # Save login details into the database
        login_details = User(username=obj.userName, password=obj.password)
        db.add(login_details)
        db.commit()

        # Perform login XT logic (for demo purposes, just returning dummy response)
        jwt_middleware = JwtMiddleware()
        login_response = jwt_middleware.LoginDetailsXT(obj.userName.strip(), obj.password.strip(), MySettingsService.get_db_connection_string())
        if login_response is not None:
            return [login_response]
        else:
            raise HTTPException(status_code=400, detail="Invalid Credentials")
    except Exception as ex:
        CLogger.LogError("Something went wrong inside the LoginDetails Autcontroller", ex)
        raise HTTPException(status_code=500, detail="Internal server error")
