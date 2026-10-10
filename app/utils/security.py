import bcrypt

def hash_password(password: str)-> str:
    pwd_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(pwd_bytes, salt)

    return hashed_bytes.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str)-> bool:
    plain_bytes = plain_password.encode('utf-8')[:72]
    hash_bytes = hashed_password.encode('utf-8')

    return bcrypt.checkpw(plain_bytes, hash_bytes)