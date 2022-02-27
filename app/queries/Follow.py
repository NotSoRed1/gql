from graphene import (
    Int,
    ObjectType,
    List,
    Field
)

from fastapi_sqlalchemy import db
from graphql import GraphQLError
import app.models as _md
from app.utils import get_curr_user
class User(ObjectType):
    pass



class Follow(ObjectType):
    follower_id = Int()
    followed_id = Int()
    follower = Field(lambda: User)
    followed = Field(lambda: User)



class FollowQueriers(ObjectType):
    all_follows = Field(List(Follow))
    
    async def resolve_all_follows(self, info):
        curr_user = get_curr_user(info)
        follows = db.session.query(_md.Follow).all()
        return follows

