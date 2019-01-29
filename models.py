from google.appengine.ext import ndb


class Todo(ndb.Model):
    task = ndb.StringProperty()
    status = ndb.BooleanProperty(default = False)
    createDate = ndb.DateTimeProperty(auto_now_add = True)
    deleted = ndb.BooleanProperty(default = False)