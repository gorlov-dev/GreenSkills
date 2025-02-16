from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(payload: str) -> str:
    return pwd_context.hash(payload)

def verify_password(payload: str, hashed_password: str) -> bool:
    return pwd_context.verify(payload, hashed_password)
