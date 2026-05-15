from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List

class UserRegister(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime
    class Config:
        from_attributes = True

class MatchRequest(BaseModel):
    patient_age:        int   = Field(ge=18, le=100)
    patient_weight:     float = Field(ge=30, le=200)
    patient_bmi:        float = Field(ge=10, le=60)
    patient_blood_type: str   = Field(pattern="^(A|B|AB|O)[+-]?$")
    donor_age:          int   = Field(ge=18, le=80)
    donor_weight:       float = Field(ge=30, le=200)
    donor_blood_type:   str   = Field(pattern="^(A|B|AB|O)[+-]?$")
    donor_min_age:      int   = Field(ge=18, le=80)
    donor_max_age:      int   = Field(ge=18, le=80)
    donor_min_weight:   int   = Field(ge=30, le=200)
    donor_max_weight:   int   = Field(ge=30, le=200)
    health_score:       float = Field(ge=0, le=10)
    biological_markers: float = Field(ge=0, le=10)
    survival_chance:    float = Field(ge=0, le=100)

class MatchResult(BaseModel):
    id:                 int
    compatibility_score: float
    recommendation:     str
    explanation:        str
    created_at:         datetime
    class Config:
        from_attributes = True

class MatchHistoryItem(BaseModel):
    id:                  int
    created_at:          datetime
    compatibility_score: float
    recommendation:      str
    patient_age:         int
    donor_age:           int
    patient_blood_type:  str
    donor_blood_type:    str
    class Config:
        from_attributes = True