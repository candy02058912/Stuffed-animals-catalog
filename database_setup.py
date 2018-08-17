#!/usr/bin/python python2.7
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    """User information"""
    __tablename__ = 'user'

    name = Column(String(250), nullable=False)
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Category(Base):
    """Stuffed animal category"""
    __tablename__ = 'category'

    name = Column(String(250), nullable=False, primary_key=True)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
        }


class CategoryItem(Base):
    """Individual stuffed animal"""
    __tablename__ = 'category_item'

    name = Column(String(80), nullable=False, primary_key=True)
    description = Column(String(250))
    picture = Column(String(250))
    category_name = Column(Integer, ForeignKey('category.name'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    create_time = Column(DateTime, server_default=func.now())

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'picture': self.picture,
            'category': self.category_name,
            'userId': self.user_id,
            'createTime': self.create_time
        }


engine = create_engine('sqlite:///stuffedanimals.db')
Base.metadata.create_all(engine)
