import bcrypt

class PassowrdHasher:

    def bcrypt_hash_password(self, password) -> str:
        hashed_pwd: str = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        return hashed_pwd

    def bscript_verify_password(self, password, hashed_password) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))