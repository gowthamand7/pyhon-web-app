import datetime
import uuid

from src.common.database import Database


class Post(object):

    def __init__(self,title,author,content,blogId,dateCreated=datetime.datetime.utcnow(),_id=None):
        self.title = title
        self.author = author
        self.dateCreated = dateCreated
        self.content = content
        self.blogId = blogId
        self._id = uuid.uuid4().hex if _id is None else _id

    def save(self):
        Database.insert(collection='posts',data=self.json())


    def json(self):
        return {
            '_id':self._id,
            'blogId':self.blogId,
            'title':self.title,
            'author':self.author,
            'content':self.content,
            'dateCreated':self.dateCreated
        }

    @classmethod
    def fromMonogo(cls, id):
        postData = Database.findOne(collection='posts',query={'_id':id})
        return cls(**postData) #**postdata It will map the class argument name and array key name

    @classmethod
    def fromBlog(cls, id):
        return [cls(**post) for post in Database.find(collection='posts', query={'blogId': id})]
