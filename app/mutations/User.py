from graphene import (
        ObjectType, 
        String, 
        Mutation,
        Boolean,
        Int,
    )

from graphql import GraphQLError
from fastapi_sqlalchemy import db
import app.models as _md
from app.utils import get_curr_user, hash_password, verify_password, create_jwt_token




class Create(Mutation):
    class Arguments:
        username = String(required=True)
        email = String(required=True)
        password = String(required=True)
    ok = Boolean()

    def mutate(self, info, username, email, password):
        query = db.session.query(_md.User).filter(_md.User.username == username)
        if query.first():
            raise GraphQLError('username already taken!!')

        hashed_pass = hash_password(password=password)
        new_user = _md.User(
            username = username,
            email = email,
            password = hashed_pass
        )
        db.session.add(new_user)
        db.session.commit()
        db.session.refresh(new_user)

        return Create(ok=True)





class Delete(Mutation):
    class Arguments:
        id = Int(required=True)

    ok = Boolean()

    def mutate(self, info, id):
        curr_user = get_curr_user(info)
        query = db.session.query(_md.User).filter(_md.User.id == id)

        if not query.first():
            raise GraphQLError('cannot find the given user!!')

        if not query.first().id == curr_user["id"]:
            raise GraphQLError(message="unauthorized !!")

        query.delete(synchronize_session=False)
        db.session.commit()

        return Delete(ok=True)




class Update(Mutation):
    class Arguments:
        id = Int(required=True)
        username = String(required=True)
        email = String(required=True)

    ok = Boolean()

    def mutate(self, info, id, username, email):
        curr_user = get_curr_user(info)
        query = db.session.query(_md.User).filter(_md.User.id == id)

        if not query.first():
            raise GraphQLError('cannot find the given user!!')
        
        if not query.first().id == curr_user["id"]:
            raise GraphQLError(message="unauthorized !!")

        query.update({ "username": username, "email": email })
        db.session.commit()

        return Delete(ok=True)


class Login(Mutation):
    class Arguments:
        username =String(required=True)
        password = String(required=True)
    
    ok = Boolean()
    token = String()

    async def mutate(self, info, username, password):
        user = db.session.query(_md.User).filter(_md.User.username == username).first()
        if not user:
            raise GraphQLError(message="incorrect username!!")

        if not verify_password(password, user.password):
            raise GraphQLError(message="incorrect password!!")

        data = {"id": user.id, "username": user.username}
        token = create_jwt_token(data)

        return Login(ok=True, token=token)



class UserMutations(ObjectType):
    create_user = Create.Field()
    delete_user = Delete.Field()
    update_user = Update.Field()
    login = Login.Field()