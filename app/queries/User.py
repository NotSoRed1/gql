from graphene import (
        ObjectType, 
        String, 
        Int, 
        Field, 
        DateTime, 
        List,
        Boolean
    )

from fastapi_sqlalchemy import db
from sqlalchemy.sql import exists
from graphql import GraphQLError
import app.models as _md
from app.queries.Post import Post
from app.utils import get_curr_user
from app.queries.Follow import Follow


class User(ObjectType):
    pass


class User(ObjectType):
    username = String()
    email = String()
    avatar_url = String()
    bio = String()
    id = Int()
    created_at = DateTime()
    posts = List(lambda: Post)
    posts_count = Int()
    followers = List(Follow)
    following = List(Follow)
    followers_count = Int()
    following_count = Int()
    isFollowed = Boolean()


    def resolve_posts_count(self, info):
        return len(self.posts)

    def resolve_followers_count(self, info):
        return len(self.followers)

    def resolve_following_count(self, info):
        return len(self.following)

    def resolve_isFollowed(self, info):
        curr_user = get_curr_user(info)
        query = db.session.query(_md.Follow).filter(_md.Follow.follower_id == curr_user["id"] , _md.Follow.followed_id == self.id).first()
        if query :
            return True
        else:
            return False



class UserQueries(ObjectType):
    all_users = Field(List(User), limit=Int(), offset=Int())
    one_user = Field(User, id = Int(required=True))
    search_users = Field(List(User), query = String(required=True))
    me = Field(User)

    async def resolve_all_users(self, info, limit, offset):
        curr_user = get_curr_user(info)
        users = db.session.query(_md.User).limit(limit).offset(offset).all()
        return users

    async def resolve_one_user(self, info, id):
        curr_user = get_curr_user(info)
        user = db.session.query(_md.User).filter(_md.User.id == id).first()
        if not user:
            raise GraphQLError(message="cannot find the given user!!")
        return user


    async def resolve_search_users(self, info, query):
        curr_user = get_curr_user(info)
        search = db.session.query(_md.User).filter(_md.User.username.contains(query)).limit(5).all()
        if query:
            return search
        else:
            return []
    
    async def resolve_me(self, info):
        curr_user = get_curr_user(info)
        query = db.session.query(_md.User).filter(_md.User.id == curr_user["id"])
        
        return query.first()

    
