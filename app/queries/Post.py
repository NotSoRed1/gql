from graphene import (
        ObjectType, 
        String, 
        List,
        Int, 
        Field,
        Boolean,
        DateTime, 
    )

from sqlalchemy.sql import exists
from sqlalchemy import select
from fastapi_sqlalchemy import db
from graphql import GraphQLError
import app.models as _md
from app.queries.Comment import Comment
from app.queries.Like import Like
from app.utils import get_curr_user

class User(ObjectType):
    pass


class Post(ObjectType):
    id = Int()
    content = String()
    attachement = String()
    created_at = DateTime()
    updated_at = DateTime()
    author = Field(lambda: User)
    comments = Field(lambda: List(Comment))
    likes = Field(lambda: List(Like))
    comments_count = Int()
    likes_count = Int()
    is_liked = Boolean()

    async def resolve_comments_count(self, info):
        return len(self.comments)

    async def resolve_likes_count(self, info):
        return len(self.likes)
    
    async def resolve_is_liked(self, info):
        curr_user = get_curr_user(info)
        result = db.session.query(_md.Like).filter(_md.Like.user_id == curr_user["id"] & _md.Like.post_id == self.id).first()
        if result is not None:
            return True
        else:
            return False



class PostQueries(ObjectType):
    all_posts = Field(List(Post), limit=Int(), offset=Int())
    one_post = Field(Post, id=Int(required=True))


    async def resolve_all_posts(self, info, limit, offset):
        curr_user = get_curr_user(info)
        posts = db.session.query(_md.Post).limit(limit).offset(offset).all()
        return posts


    async def resolve_one_post(self, info, id):
        curr_user = get_curr_user(info)
        post = db.session.query(_md.Post).filter(_md.Post.id == id).first()
        if not post:
            raise GraphQLError(message="cannot find the given post!!")
        return post

