from fastapi import FastAPI,Depends,HTTPException,status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError
from .config import settings
from .database import Base,engine,get_db
from .models import User,Case,Evidence,AuditLog
from .schemas import RegisterRequest,TokenResponse,CaseCreate,CaseResponse,EvidenceResponse
from .security import hash_password,verify_password,create_access_token,decode_token

Base.metadata.create_all(bind=engine)
app=FastAPI(title=settings.app_name,version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[x.strip() for x in settings.cors_origins.split(",") if x.strip()],
    allow_credentials=True,
    allow_methods=["GET","POST","PUT","DELETE"],
    allow_headers=["*"],
)
bearer=HTTPBearer(auto_error=False)

def current_user(credentials:HTTPAuthorizationCredentials=Depends(bearer),db:Session=Depends(get_db))->User:
    if not credentials:
        raise HTTPException(401,"Authentication required")
    try:
        username=decode_token(credentials.credentials)
    except (JWTError,ValueError):
        raise HTTPException(401,"Invalid or expired token")
    user=db.query(User).filter(User.username==username).first()
    if not user:
        raise HTTPException(401,"User not found")
    return user

def audit(db:Session,user:User,action:str,target:str=""):
    db.add(AuditLog(username=user.username,action=action,target=target))
    db.commit()

@app.get("/health")
def health():
    return {"status":"ok","service":settings.app_name}

@app.post("/auth/register",response_model=TokenResponse,status_code=201)
def register(payload:RegisterRequest,db:Session=Depends(get_db)):
    if db.query(User).filter(User.username==payload.username).first():
        raise HTTPException(409,"Username already exists")
    user=User(username=payload.username,password_hash=hash_password(payload.password))
    db.add(user);db.commit()
    return {"access_token":create_access_token(user.username),"token_type":"bearer"}

@app.post("/auth/login",response_model=TokenResponse)
def login(payload:RegisterRequest,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.username==payload.username).first()
    if not user or not verify_password(payload.password,user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,"Invalid credentials")
    return {"access_token":create_access_token(user.username),"token_type":"bearer"}

@app.post("/cases",response_model=CaseResponse,status_code=201)
def create_case(payload:CaseCreate,user:User=Depends(current_user),db:Session=Depends(get_db)):
    if db.query(Case).filter(Case.case_number==payload.case_number).first():
        raise HTTPException(409,"Case number already exists")
    case=Case(**payload.model_dump())
    db.add(case);db.commit();db.refresh(case)
    audit(db,user,"case.created",case.case_number)
    return case

@app.get("/cases",response_model=list[CaseResponse])
def list_cases(user:User=Depends(current_user),db:Session=Depends(get_db)):
    return db.query(Case).order_by(Case.created_at.desc()).all()

@app.post("/cases/{case_id}/evidence",response_model=EvidenceResponse,status_code=201)
def register_evidence(case_id:int,name:str,path:str,sha256:str,size_bytes:int,user:User=Depends(current_user),db:Session=Depends(get_db)):
    if not db.get(Case,case_id):
        raise HTTPException(404,"Case not found")
    if len(sha256)!=64 or not re.fullmatch(r"[0-9a-fA-F]{64}",sha256):
        raise HTTPException(422,"sha256 must be a 64-character hexadecimal digest")
    evidence=Evidence(case_id=case_id,name=name,path=path,sha256=sha256.lower(),size_bytes=size_bytes,collected_by=user.username)
    db.add(evidence);db.commit();db.refresh(evidence)
    audit(db,user,"evidence.registered",name)
    return evidence

@app.get("/cases/{case_id}/evidence",response_model=list[EvidenceResponse])
def list_evidence(case_id:int,user:User=Depends(current_user),db:Session=Depends(get_db)):
    if not db.get(Case,case_id):
        raise HTTPException(404,"Case not found")
    return db.query(Evidence).filter(Evidence.case_id==case_id).order_by(Evidence.created_at.desc()).all()
