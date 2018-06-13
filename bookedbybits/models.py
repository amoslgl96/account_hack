from google.appengine.ext import ndb

class ToDoItem(ndb.Model):
    onCreateTimeStamp = ndb.DateTimeProperty(auto_now_add=True)
    onFinishTimeStamp = ndb.DateTimeProperty(auto_now_add=True)
    deadline = ndb.IntegerProperty(default=0)
    predictedTime = ndb.IntegerProperty(default=0)
    usedTime = ndb.IntegerProperty(default=0)
    onCheckInTimeStamps = ndb.DateTimeProperty(repeated = True)
    onCheckOutTimeStamps = ndb.DateTimeProperty(repeated = True)
    taskDescription = ndb.StringProperty()
    taskType = ndb.StringProperty()
    reason = ndb.StringProperty(default = "")
    auditorName = ndb.StringProperty()
    managerName = ndb.StringProperty()
    confirmSubmitted = ndb.BooleanProperty(default = False)
    confirmSubmittedTimeStamp = ndb.DateTimeProperty(auto_now_add=True)
    iD = ndb.IntegerProperty(default=0)
    checker = ndb.BooleanProperty(default = False)
    
