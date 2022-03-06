from ast import In
from graphene import (
    Field,
    ObjectType,
    Mutation,
    Boolean,
    Int,
    String,
)

from fastapi_sqlalchemy import db
from graphql import GraphQLError
import app.models as _md
from app.utils import get_curr_user



class CreateLike(Mutation):
    class Arguments:
        post_id = Int(required=True)
    
    ok = Boolean()
    test = Int()

    def mutate(self, info, post_id):
        curr_user = get_curr_user(info)
        query = db.session.query(_md.Like).filter(_md.Like.user_id == curr_user["id"] , _md.Like.post_id == post_id)
        if not query.first():
            like = _md.Like(user_id=curr_user["id"], post_id=post_id)
            try:
                db.session.add(like)
                db.session.commit()
                db.session.refresh(like)

            except Exception as e:
                raise GraphQLError(message="somthing went wrong!!")
        else:
            query.delete(synchronize_session=False)    
            db.session.commit()

        return CreateLike(test=post_id ,ok=True)




class LikeMutations(ObjectType):
    toggle_like = CreateLike.Field()
