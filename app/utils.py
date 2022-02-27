from lib2to3.pgen2 import token
from graphql import GraphQLError
from passlib.context import CryptContext
from app.Config import settings
from datetime import datetime, timedelta
from jose import JWTError, jwt
from graphene import ResolveInfo



password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password):
    return password_context.hash(password)

def verify_password(plain_pass, hashed_pass):
    return password_context.verify(plain_pass, hashed_pass)


def create_jwt_token(data):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.expire_time)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


# def get_curr_user(info: ResolveInfo):
#     token = info.context['request']["headers"][6][1].decode()
#     try:
#         payload = jwt.decode(token, settings.secret_key, algorithms= settings.algorithm)
#         id, username = payload.get("id"), payload.get("username")
#         if not id or not username:
#             raise GraphQLError(message="unauthorized!!")
        
#         return {"id": id, "username": username}
#     except:
#         raise GraphQLError(message="unauthorized!!")



def get_curr_user(info: ResolveInfo):
    token = info.context['request']["headers"].decode()
    # payload = jwt.decode(token, settings.secret_key, algorithms= settings.algorithm)
    # id, username = payload.get("id"), payload.get("username")
    # if not id or not username:
        # raise GraphQLError(message="unauthorized!!")
        
    return token