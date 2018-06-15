from google.appengine.ext import ndb
import datetime
import logging

def convertToJsonEpoch(databaseItem): #receive datetime objec
    if type(databaseItem) == type([]):
        new_a = []
        for timestamp in databaseItem:
            new_a.append(convertToJsonEpoch(timestamp))
        return new_a
    return (databaseItem - datetime.datetime(1970,1,1)).total_seconds() * 1000

def convertToDateTime(epochtime):
        logging.info(type(epochtime))
        if type(epochtime) == type([]):
            new_a = []
            for i in epochtime:
                new_a.append(convertToDateTime(i))
            return new_a
        else:
            return datetime.datetime.fromtimestamp(epochtime/1000) #javascript gives out in milisecons, python expects seconds

class Employee(ndb.Model):
    userName = ndb.StringProperty()
    isManager = ndb.BooleanProperty()
    manager = ndb.KeyProperty()

    @staticmethod
    def toJson(query):
        if type(query) == type([]):
            new_a = []
            for employee in query:
                new_dict = {"userName" : employee.userName,
                        "isManager" : employee.isManager,
                        "manager" : employee.manager}
                new_a.append(new_dict)
            return new_a
        else:
            new_dict = {"userName" : query.userName,
                        "isManager" : query.isManager,
                        "manager" : query.manager}
            return new_dict

    
class ToDoItem(ndb.Model):
    onCreateTimeStamp = ndb.DateTimeProperty()
    onFinishTimeStamp = ndb.DateTimeProperty()
    deadLine = ndb.DateTimeProperty(default=0)
    predictedTime = ndb.DateTimeProperty(default=0)
    usedTime = ndb.IntegerProperty(default=0)
    onCheckInTimeStamps = ndb.DateTimeProperty(repeated = True)
    onCheckOutTimeStamps = ndb.DateTimeProperty(repeated = True)
    taskDescription = ndb.StringProperty()
    taskType = ndb.StringProperty()
    reason = ndb.StringProperty(default = "")
    auditor = ndb.KeyProperty(kind = Employee)
    manager = ndb.KeyProperty(kind = Employee)
    auditorName = ndb.StringProperty()
    managerName = ndb.StringProperty() 
    confirmSubmitted = ndb.BooleanProperty(default = False)
    confirmSubmittedTimeStamp = ndb.DateTimeProperty()
    checker = ndb.BooleanProperty(default = False)
    progress = ndb.StringProperty()

    
    @staticmethod
    def cleanJsonDateTime(myjson):
        logging.info('DEADLINE')
        logging.info(myjson['deadLine'])
        myjson['onCreateTimeStamp'] = convertToDateTime(myjson['onCreateTimeStamp'])
        myjson['onFinishTimeStamp'] = convertToDateTime(myjson['onFinishTimeStamp'])
        myjson['deadLine'] = convertToDateTime(myjson['deadLine'])
        myjson['predictedTime'] = convertToDateTime(myjson['predictedTime'])
        myjson['onCheckInTimeStamps']= convertToDateTime(myjson['onCheckInTimeStamps'])
        myjson['onCheckOutTimeStamps'] = convertToDateTime(myjson['onCheckOutTimeStamps'])
        myjson['confirmSubmittedTimeStamp'] = convertToDateTime(myjson['confirmSubmittedTimeStamp'])
                
    @staticmethod
    def createFromJson(myjson):
#TODO
##        manager = Employee.get_by_id(myjson['managerName'])
##        auditor = Employee.get_by_id(myjson['auditorName'])
        ToDoItem.cleanJsonDateTime(myjson)
        query = ToDoItem.get_by_id(myjson['iD'])
        if query: #item exist
            logging.info("Edit to do")
            query.onCreateTimeStamp = myjson['onCreateTimeStamp']
            query.onFinishTimeStamp = myjson['onFinishTimeStamp']
            query.deadLine = myjson['deadLine']
            query.predictedTime = myjson['predictedTime']
            query.usedTime = myjson['usedTime']
            query.onCheckInTimeStamps = myjson['onCheckInTimeStamps']
            query.onCheckOutTimeStamps = myjson['onCheckOutTimeStamps']
            query.taskDescription = myjson['taskDescription']
            query.taskType = myjson['taskType']
            query.reason = myjson['reason']
            query.confirmSubmitted = myjson['confirmSubmitted']
            query.confirmSubmittedTimeStamp = myjson['confirmSubmittedTimeStamp']
            query.checker = myjson['checker']
            query.auditorName = myjson['auditorName']
            query.managerName = myjson['managerName']
            query.progress = myjson['progress']
            query.put()
            
        else:
            logging.info("New to do")
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
                managerName = myjson['managerName'],
                progress = myjson['progress']
                )
            new_todo.put()


    @staticmethod     
    def toJson(iterable):
        logging.info(type(iterable))
        json_array = []
        for todoitem in iterable:
            new_dict = {
                "onCreateTimeStamp" : convertToJsonEpoch(todoitem.onCreateTimeStamp),
                "onFinishTimeStamp" : convertToJsonEpoch(todoitem.onFinishTimeStamp),
                "deadLine" : convertToJsonEpoch(todoitem.deadLine),
                "predictedTime" : convertToJsonEpoch(todoitem.predictedTime),
                "usedTime" : todoitem.usedTime,
                "onCheckInTimeStamps" : convertToJsonEpoch(todoitem.onCheckInTimeStamps),
                "onCheckOutTimeStamps": convertToJsonEpoch(todoitem.onCheckOutTimeStamps),
                "taskDescription": todoitem.taskDescription,
                "taskType": todoitem.taskType,
                "reason": todoitem.reason,
                "auditorName": todoitem.auditorName,
                "managerName": todoitem.managerName,
                "confirmSubmitted": todoitem.confirmSubmitted,
                "confirmSubmittedTimeStamp": convertToJsonEpoch(todoitem.confirmSubmittedTimeStamp),
                "iD": todoitem.key.id(),
                'checker': todoitem.checker,
                'progress': todoitem.progress
            }
            json_array.append(new_dict)
        return json_array

        
        
        

    


    
        
