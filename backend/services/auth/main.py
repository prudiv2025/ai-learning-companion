"""
AI Learning Companion — Auth Service
Handles: Registration, Login, JWT, RBAC, Profile Management
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
import os

app = FastAPI(title="Auth Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = os.getenv("JWT_SECRET", "change-me-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

Role = Literal["student", "teacher", "parent", "admin"]

# ─── Models ────────────────────────────────────────────────────────────────────

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Role
    class_grade: Optional[int] = None        # For students (3–12)
    school_id: Optional[str] = None
    parent_email: Optional[EmailStr] = None  # For students under 13

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    role: Role
    user_id: str

class TokenData(BaseModel):
    user_id: str
    role: Role

# ─── Helpers ───────────────────────────────────────────────────────────────────

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + expires_delta
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_access_token(user_id: str, role: Role) -> str:
    return create_token(
        {"sub": user_id, "role": role, "type": "access"},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

def create_refresh_token(user_id: str, role: Role) -> str:
    return create_token(
        {"sub": user_id, "role": role, "type": "refresh"},
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

async def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        if user_id is None or role is None:
            raise credentials_exception
        return TokenData(user_id=user_id, role=role)
    except JWTError:
        raise credentials_exception

def require_role(*roles: Role):
    async def checker(current_user: TokenData = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {roles}"
            )
        return current_user
    return checker

# ─── Routes ────────────────────────────────────────────────────────────────────

@app.post("/auth/register", status_code=201)
async def register(user: UserRegister):
    """Register a new user (student/teacher/parent/admin)."""
    # TODO: Save to PostgreSQL via SQLAlchemy
    hashed_pw = hash_password(user.password)
    user_id = f"usr_{user.email.split('@')[0]}_{int(datetime.utcnow().timestamp())}"

    # COPPA check: require parent consent for under-13
    if user.role == "student" and user.class_grade and user.class_grade <= 5:
        if not user.parent_email:
            raise HTTPException(400, "Parent email required for students in Class 3–5 (COPPA compliance)")

    access_token = create_access_token(user_id, user.role)
    refresh_token = create_refresh_token(user_id, user.role)

    return {
        "success": True,
        "data": Token(
            access_token=access_token,
            refresh_token=refresh_token,
            role=user.role,
            user_id=user_id
        )
    }

@app.post("/auth/login", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login and receive JWT tokens."""
    # TODO: Fetch user from DB and verify password
    # Placeholder response
    user_id = "usr_demo_123"
    role: Role = "student"
    return {
        "success": True,
        "data": Token(
            access_token=create_access_token(user_id, role),
            refresh_token=create_refresh_token(user_id, role),
            role=role,
            user_id=user_id
        )
    }

@app.post("/auth/refresh")
async def refresh_token(refresh_token: str):
    """Issue new access token using refresh token."""
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(400, "Invalid token type")
        user_id = payload["sub"]
        role = payload["role"]
        return {
            "success": True,
            "data": {"access_token": create_access_token(user_id, role)}
        }
    except JWTError:
        raise HTTPException(401, "Invalid refresh token")

@app.get("/auth/me")
async def get_me(current_user: TokenData = Depends(get_current_user)):
    """Get current user profile."""
    return {"success": True, "data": current_user}

@app.get("/auth/health")
async def health():
    return {"status": "ok", "service": "auth"}
