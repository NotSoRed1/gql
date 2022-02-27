from sqlalchemy import Column, ForeignKey, String, Integer, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    bio = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text("NOW()"))
    posts = relationship("Post")
    followers = relationship("Follow", foreign_keys="Follow.followed_id")
    following = relationship("Follow", foreign_keys="Follow.follower_id") 


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    content = Column(String, nullable=False)
    attachement = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=text("NOW()"))
    updated_at = Column(DateTime(timezone=True), server_default=text("NOW()"), onupdate=text("NOW()"))
    author_id = Column(Integer , ForeignKey("users.id"), nullable=False)
    author = relationship("User", overlaps="posts")
    comments = relationship("Comment")
    likes = relationship("Like")



class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=text("NOW()"))
    updated_at = Column(DateTime(timezone=True), server_default=text("NOW()"), onupdate=text("NOW()"))
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    author = relationship("User", overlaps="comments")
    post = relationship("Post", overlaps="comments")



class Like(Base):
    __tablename__ = "likes"

    user_id =  Column(Integer, ForeignKey("users.id"), primary_key=True, nullable=False)   
    post_id =  Column(Integer, ForeignKey("posts.id"), primary_key=True, nullable=False)   
    author = relationship("User", overlaps="likes")

class Follow(Base):
    __tablename__ = "follows"

    follower_id = Column(Integer, ForeignKey("users.id"), primary_key=True, nullable=False)
    followed_id = Column(Integer, ForeignKey("users.id"), primary_key=True, nullable=False)
    follower = relationship("User", foreign_keys="Follow.follower_id", overlaps="following")
    followed = relationship("User", foreign_keys="Follow.followed_id", overlaps="followers")
