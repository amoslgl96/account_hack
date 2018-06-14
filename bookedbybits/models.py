from google.appengine.ext import ndb

class Employee(ndb.Model):
    userName = ndb.StringProperty()
    isManager = ndb.BooleanProperty()
    manager = ndb.KeyProperty()

    @staticmethod
    def toJson(query):
        new_dict = {"userName" : query.userName,
                    "isManager" : query.isManager,
                    "manager" : query.manager}
        return new_dict
    
class ToDoItem(ndb.Model):
    onCreateTimeStamp = ndb.IntegerProperty()
    onFinishTimeStamp = ndb.IntegerProperty()
    deadLine = ndb.IntegerProperty(default=0)
    predictedTime = ndb.IntegerProperty(default=0)
    usedTime = ndb.IntegerProperty(default=0)
    onCheckInTimeStamps = ndb.IntegerProperty(repeated = True)
    onCheckOutTimeStamps = ndb.IntegerProperty(repeated = True)
    taskDescription = ndb.StringProperty()
    taskType = ndb.StringProperty()
    reason = ndb.StringProperty(default = "")
    auditor = ndb.KeyProperty(kind = Employee)
    manager = ndb.KeyProperty(kind = Employee)
    auditorName = ndb.StringProperty()
    managerName = ndb.StringProperty() 
    confirmSubmitted = ndb.BooleanProperty(default = False)
    confirmSubmittedTimeStamp = ndb.IntegerProperty()
    checker = ndb.BooleanProperty(default = False)

    @staticmethod
    def createFromJson(myjson):
#TODO
##        manager = Employee.get_by_id(myjson['managerName'])
##        auditor = Employee.get_by_id(myjson['auditorName'])

        query = ToDoItem.get_by_id(myjson['iD'])
        if query: #item exist
            query.onCreateTimeStamp = myjson['onCreateTimeStamp'],
            query.onFinishTimeStamp = myjson['onFinishTimeStamp'],
            query.deadLine = myjson['deadLine'],
            query.predictedTime = myjson['predictedTime'],
            query.usedTime = myjson['usedTime'],
            query.onCheckInTimeStamps = myjson['onCheckInTimeStamps'],
            query.onCheckOutTimeStamps = myjson['onCheckOutTimeStamps'],
            query.taskDescription = myjson['taskDescription'],
            query.taskType = myjson['taskType'],
            query.reason = myjson['reason'],
            query.confirmSubmitted = myjson['confirmSubmitted'],
            query.confirmSubmittedTimeStamp = myjson['confirmSubmittedTimeStamp'],
            query.checker = myjson['checker'],
            query.auditorName = myjson['auditorName'],
            query.managerName = myjson['managerName']
            query.put
        else:
            new_todo = ToDoItem(
                onCreateTimeStamp = myjson['onCreateTimeStamp'],
                onFinishTimeStamp = myjson['onFinishTimeStamp'],
                deadLine = myjson['deadLine'],
                predictedTime = myjson['predictedTime'],
                usedTime = myjson['usedTime'],
                onCheckInTimeStamps = myjson['onCheckInTimeStamps'],
                onCheckOutTimeStamps = myjson['onCheckOutTimeStamps'],
                taskDescription = myjson['taskDescription'],
                taskType = myjson['taskType'],
                reason = myjson['reason'],
                confirmSubmitted = myjson['confirmSubmitted'],
                confirmSubmittedTimeStamp = myjson['confirmSubmittedTimeStamp'],
                id = myjson['iD'],
                checker = myjson['checker'],
                auditorName = myjson['auditorName'],
                managerName = myjson['managerName']
                )
            new_todo.put()


    @staticmethod     
    def toJson(iterable):
        json_array = []
        for todoitem in iterable:
            new_dict = {
                "onCreateTimeStamp" : todoitem.onCreateTimeStamp,
                "onFinishTimeStamp" : todoitem.onFinishTimeStamp,
                "deadline" : todoitem.deadLine,
                "predictedTime" : todoitem.predictedTime,
                "usedTime" : todoitem.usedTime,
                "onCheckInTimeStamps" : todoitem.onCheckInTimeStamps,
                "onCheckOutTimeStamps": todoitem.onCheckOutTimeStamps,
                "taskDescription": todoitem.taskDescription,
                "taskType": todoitem.taskType,
                "reason": todoitem.reason,
                "auditorName": todoitem.auditorName,
                "managerName": todoitem.managerName,
                "confirmSubmitted": todoitem.confirmSubmitted,
                "confirmSubmittedTimeStamp": todoitem.confirmSubmittedTimeStamp,
                "iD": todoitem.key.id(),
                'checker': todoitem.checker
            }
            json_array.append(new_dict)
        return json_array

        
        
        

    


    
        
