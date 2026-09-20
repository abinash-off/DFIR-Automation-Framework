from pydantic import BaseModel,Field

class RegisterRequest(BaseModel):
    username:str=Field(min_length=3,max_length=80,pattern=r"^[A-Za-z0-9_.-]+$")
    password:str=Field(min_length=8,max_length=128)

class TokenResponse(BaseModel):
    access_token:str
    token_type:str="bearer"

class CaseCreate(BaseModel):
    case_number:str=Field(min_length=2,max_length=80)
    title:str=Field(min_length=1,max_length=200)
    description:str=""

class CaseResponse(CaseCreate):
    id:int
    status:str
    model_config={"from_attributes":True}

class EvidenceResponse(BaseModel):
    id:int
    case_id:int
    name:str
    path:str
    sha256:str
    size_bytes:int
    collected_by:str
    model_config={"from_attributes":True}
