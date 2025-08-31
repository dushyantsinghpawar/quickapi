from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator


# ---------- Items ----------
class ItemCreate(BaseModel):
    name: str
    description: str | None = None


class ItemOut(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime

    class Config:
        from_attributes = True  # pydantic v2


# ---------- Auth / Users ----------
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)

    @field_validator("password")
    @classmethod
    def strong_password(cls, v: str):
        import re

        if len(v) < 12:
            raise ValueError("Password must be at least 12 characters.")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must include a lowercase letter.")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must include an uppercase letter.")
        if not re.search(r"\d", v):
            raise ValueError("Password must include a digit.")
        if not re.search(r"[^\w\s]", v):
            raise ValueError("Password must include a symbol.")
        common = {
            "password",
            "123456",
            "qwerty",
            "letmein",
            "iloveyou",
            "admin",
            "welcome",
            "monkey",
            "dragon",
        }
        if v.lower() in common:
            raise ValueError("Password is too common.")
        return v


class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PasswordChange(BaseModel):
    old_password: str
    new_password: str = Field(min_length=12, max_length=128)

    @field_validator("new_password")
    @classmethod
    def strong_password(cls, v: str):
        import re

        if len(v) < 12:
            raise ValueError("Password must be at least 12 characters.")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must include a lowercase letter.")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must include an uppercase letter.")
        if not re.search(r"\d", v):
            raise ValueError("Password must include a digit.")
        if not re.search(r"[^\w\s]", v):
            raise ValueError("Password must include a symbol.")
        common = {
            "password",
            "123456",
            "qwerty",
            "letmein",
            "iloveyou",
            "admin",
            "welcome",
            "monkey",
            "dragon",
        }
        if v.lower() in common:
            raise ValueError("Password is too common.")
        return v


# ---------- ML (Iris) ----------
class IrisIn(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


class IrisOut(BaseModel):
    label: str
    probabilities: dict[str, float]
