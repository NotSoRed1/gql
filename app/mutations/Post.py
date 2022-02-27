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
        content = String(required=True)
        attachement = String(required=True)
    ok = Boolean()

    def mutate(self, info, content, attachement):
        curr_user = get_curr_user(info)
        new_user = _md.Post(
            author_id = curr_user["id"],
            content = content,
            attachement = attachement
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            db.session.refresh(new_user)
        except :
            raise GraphQLError(message="faild to create the post")

        return Create(ok=True)





class Delete(Mutation):
    class Arguments:
        id = Int(required=True)

    ok = Boolean()

    def mutate(self, info, id):
        curr_user = get_curr_user(info)
        query = db.session.query(_md.Post).filter(_md.Post.id == id)

        if not query.first():
            raise GraphQLError('cannot find the given Post!!')

        if not query.first().author_id == curr_user["id"]:
            raise GraphQLError(message="unauthorized !!")

        query.delete(synchronize_session=False)
        db.session.commit()

        return Delete(ok=True)




class Update(Mutation):
    class Arguments:
        id = Int(required=True)
        content = String(required=True)

    ok = Boolean()

    def mutate(self, info, id, content):
        curr_user = get_curr_user(info)
        query = db.session.query(_md.Post).filter(_md.Post.id == id)

        if not query.first():
            raise GraphQLError('cannot find the given Post!!')

        if not query.first().author_id == curr_user["id"]:
            raise GraphQLError(message="unauthorized !!")

        query.update({"content": content})
        db.session.commit()

        return Delete(ok=True)





class PostMutations(ObjectType):
    create_post = Create.Field()
    delete_post = Delete.Field()
    update_post = Update.Field()