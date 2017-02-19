import datetime
import uuid

from src.common.database import Database
from src.models.posts import Post


class Blog(object):

    def __init__(self,author,title,description,authorId,_id = None):
        self.author = author
        self.title = title
        self.authorId =  authorId
        self.description  = description
        self._id = uuid.uuid4().hex if _id is None else _id

    def newPost(self,title,content,date=datetime.datetime.utcnow()):
        post = Post(title=title,
                    author=self.author,
                    content=content,
                    blogId=self._id,
                    dateCreated=date)
        post.save()

    def getPosts(self):
        return Post.fromBlog(self._id)

    def saveToMongo(self):
        Database.insert(collection='blogs', data=self.json())

    def json(self):
        return {
            'author':self.author,
            'authorId':self.authorId,
            'title':self.title,
            'description':self.description,
            '_id':self._id
        }

    @classmethod
    def getFromMongo(cls,id):
        blogData = Database.findOne(collection='blogs',query={'_id':id})
        return cls(**blogData) #**blogData It will map the argument name and array key name


    @classmethod
    def findByAuthorId(cls,id):
        return [cls(**blog) for blog in  Database.find(collection='blogs',query={'authorId':id})]