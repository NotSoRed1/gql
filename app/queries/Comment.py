from graphene import (
    ObjectType,
    String,
    Int,
    List,
    DateTime,
    Field,
)
from app.utils import get_curr_user
from fastapi_sqlalchemy import db
from graphql import GraphQLError
import app.models as _md


class User(ObjectType):
    pass
class Post(ObjectType):
    pass


class Comment(ObjectType):
    id = Int()
    content = String()
    created_at = DateTime()
    updated_at = DateTime()
    author = Field(lambda: User)
    post = Field(lambda: Post)




class CommentQueries(ObjectType):
    all_comments = Field(List(Comment))
    one_comment = Field(Comment, id = Int(required=True))
    comment_by_post = Field(List(Comment), id = Int(required=True))
    
    async def resolve_all_comments(root, info):
        curr_user  = get_curr_user(info)
        comments = db.session.query(_md.Comment).all() 
        return comments

    
    async def resolve_one_comment(root, info, id):
        curr_user  = get_curr_user(info)
        comment = db.session.query(_md.Comment).filter(_md.Comment.id == id).first()
        if not comment:
            raise GraphQLError(message="couldnt find the comment")
        return comment


    async def resolve_comment_by_post(root, info, id):
        curr_user  = get_curr_user(info)
        comments = db.session.query(_md.Comment).filter(_md.Comment.post_id == id).all() 
        return comments
