from re import L
from graphene import (
    Int,
    ObjectType,
    String,
    Field,
    Boolean,
    List
)

from app.utils import get_curr_user
from fastapi_sqlalchemy import db
from graphql import GraphQLError
import app.models as _md

class User(ObjectType):
    pass


class Like(ObjectType):
    user_id = Int()
    post_id = Int()
    author = Field(lambda: User)



class LikeQueries(ObjectType):
    all_likes = Field(List(Like))
    likes_by_post = Field(List(Like), id = Int(required=True))
    likes_by_user = Field(List(Like), id = Int(required=True))


    async def resolve_all_likes(self, info):
        curr_user = get_curr_user(info)
        likes = db.session.query(_md.Like).all()
        return likes

    async def resolve_likes_by_post(self, info, id):
        curr_user = get_curr_user(info)
        likes = db.session.query(_md.Like).filter(_md.Like.post_id == id).all()
        return likes
    
    async def resolve_likes_by_user(self, info, id):
        curr_user = get_curr_user(info)
        likes = db.session.query(_md.Like).filter(_md.Like.user_id == id).all()
        return likes