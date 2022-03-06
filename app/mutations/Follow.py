from graphene import (
    Mutation,
    ObjectType,
    Boolean,
    Int,
)


import app.models as _md
from graphql import GraphQLError
from fastapi_sqlalchemy import db
from app.utils import get_curr_user



class Create(Mutation):
    class Arguments:
        followed_id = Int(required=True)
    
    ok = Boolean()

    def mutate(self, info, followed_id):
        curr_user = get_curr_user(info)
        query = db.session.query(_md.Follow).filter(_md.Follow.follower_id == curr_user["id"] , _md.Follow.followed_id == followed_id)

        if not query.first():
            follow = _md.Follow(follower_id=curr_user["id"], followed_id=followed_id)
            try:
                db.session.add(follow)
                db.session.commit()
                db.session.refresh(follow)
            except:
                raise GraphQLError(message="faild to follow the user plz try again !!")
        else:
            try:
                query.delete(synchronize_session=False)    
                db.session.commit()
            except:
                raise GraphQLError(message="faild to unfollow the user plz try again !!")

        return Create(ok=True)




class FollowMutations(ObjectType):
    toggle_follow = Create.Field()
