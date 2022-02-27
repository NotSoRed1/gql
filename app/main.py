from starlette_graphene3 import GraphQLApp, make_playground_handler
from graphene import ObjectType, Schema
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.Config import settings



from app.mutations.Comment import CommentMutations
from app.mutations.Follow import FollowMutations
from app.mutations.Like import LikeMutations
from app.mutations.Post import PostMutations
from app.mutations.User import UserMutations
from app.queries.Comment import CommentQueries
from app.queries.Follow import FollowQueriers
from app.queries.Like import LikeQueries
from app.queries.Post import PostQueries
from app.queries.User import UserQueries




app = FastAPI()


app.add_middleware(DBSessionMiddleware, db_url=settings.gql_database_url)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    )



class RootQuery(
        UserQueries, 
        PostQueries,
        CommentQueries, 
        LikeQueries,
        FollowQueriers,
        ObjectType
    ):
    pass


class RootMutation(
        UserMutations,
        PostMutations,
        CommentMutations,
        LikeMutations,
        FollowMutations,
        ObjectType
    ):
    pass



schema = Schema(query=RootQuery, mutation=RootMutation)
app.add_route("/graphql", GraphQLApp(schema, on_get=make_playground_handler()))


























# @app.post("/users")
# async def create_user(user: _sc.UserCreate):
#     query = db.session.query(_md.User).filter(_md.User.username == user.username).first()
#     if query:
#         raise HTTPException(
#                 status_code=status.HTTP_302_FOUND, 
#                 detail="Username already taken!!"
#             )

#     new_user = _md.User(username= user.username, password= user.password)
#     db.session.add(new_user)
#     db.session.commit()
#     db.session.refresh(new_user)

#     return new_user



# @app.get("/users", response_model=list[_sc.UserOut])
# async def get_users():
#     users = db.session.query(_md.User).all()

#     return users

