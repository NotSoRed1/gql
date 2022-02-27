from graphene import (
        ObjectType, 
        String, 
        Mutation,
        Boolean,
        Int
    )

from graphql import GraphQLError
from fastapi_sqlalchemy import db
import app.models as _md
from app.utils import get_curr_user



class Create(Mutation):
    class Arguments:
        post_id = Int(required=True)
        content = String(required=True)
    ok = Boolean()

    def mutate(self, info, post_id, content):
        curr_user = get_curr_user(info)
        new_comment = _md.Comment(
            post_id = post_id,
            author_id = curr_user["id"],
            content = content
        )
        try:
            db.session.add(new_comment)
            db.session.commit()
            db.session.refresh(new_comment)

        except Exception as e:
            raise GraphQLError(message="faild to create the comment")

        return Create(ok=True)



class Delete(Mutation):
    class Arguments:
        id = Int(required=True)
    ok = Boolean()

    def mutate(self, info, id):
        curr_user = get_curr_user(info)
        query = db.session.query(_md.Comment).filter(_md.Comment.id == id)

        if not query.first():
            raise GraphQLError(message="cannot find the comment")            
       
        if not query.first().author_id == curr_user["id"]:
            raise GraphQLError(message="unauthorized !!") 

        query.delete(synchronize_session=False)
        db.session.commit()

        return Create(ok=True)




class Update(Mutation):
    class Arguments:
        id = Int(required=True)
        content = String(required=True)
    ok = Boolean()

    def mutate(self, info, id, content):
        curr_user = get_curr_user(info)
        query = db.session.query(_md.Comment).filter(_md.Comment.id == id)

        if not query.first():
            raise GraphQLError(message="cannot find the comment")            
        
        if not query.first().author_id == curr_user["id"]:
            raise GraphQLError(message="unauthorized !!") 

        query.update({"content": content})
        db.session.commit()

        return Create(ok=True)




class CommentMutations(ObjectType):
    create_comment = Create.Field()
    delete_comment = Delete.Field()
    update_comment = Update.Field()