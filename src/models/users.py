import datetime
import uuid

from flask import session
from src.common.database import Database
from src.models.blogs import Blog


class User(object):
    def __init__(self,email,password,_id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def getByEmail(cls,email):
        data = Database.findOne(collection='users',query={'email':email})
        if data is not None:
            return cls(**data)

    @classmethod
    def getById(cls,id):
        data = Database.findOne(collection='users',query={'_id':id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def loginValid(email,password):
        user = User.getByEmail(email=email)
        if user is not None:
            return user.password == password
        return False

    @staticmethod
    def register(email,password):
        user = User.getByEmail(email)
        if user is not None:
            user = User(email=email,password=password)
            user.saveToMongo()
            session['email'] = email
            return True
        else:
            return False

    @staticmethod
    def login(email):
        session['email'] = email

    @staticmethod
    def logout():
        session['email'] = None

    def newBlog(self,title,description):
        blog = Blog(author=self.email,
                    title=title,
                    description=description,
                    authorId=self._id)
        blog.saveToMongo()

    @staticmethod
    def newPost(blogId,title,content,dateCreated=datetime.datetime.utcnow()):
        blog = Blog.getFromMongo(blogId)
        if blog is not None:
            blog.newPost(title=title,content=content,dateCreated=dateCreated)

    def getBlogs(self):
        Blog.findByAuthorId(self._id)

    def saveToMongo(self):
        Database.insert(collection='users',data=self.json())

    def json(self):
        return {
            'email':self.email,
            'password':self.password
        }

