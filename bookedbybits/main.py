#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os
import json
import datetime
import logging

from models import ToDoItem

from google.appengine.ext import ndb
from google.appengine.api import users


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class ToDo:
    def __init__(self, title, name_of_coy, type_of_task, name, reccomended_time, start_time, end_time, time_spent):
        self.title = title
        self.name_of_coy = name_of_coy
        self.type_of_task = type_of_task
        self.name = name
        self.reccomended_time = reccomended_time
        self.start_time = start_time
        self.end_time = end_time
        self.time_spent = time_spent
        
class RestHandler(webapp2.RequestHandler):
    def decorateHeaders(self):
        """Decorates headers for the current request."""
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers.add_header('Access-Control-Allow-Headers', 'Authorization, content-type')
        self.response.headers.add_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')

    def options(self):
        """Default OPTIONS handler for the entire app."""
        self.decorateHeaders()
        
class BaseHandler(RestHandler):
    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app = self.app)

    def render_template(self, filename, template_values):
        self.user = users.get_current_user()
        if self.user:
          template_values['user']= self.user.nickname()
          template_values['url_linktext'] = 'Logout'
          template_values['url'] = users.create_logout_url(self.request.uri)
        else:
            template_values['user'] = 'anonymous'
            template_values['url_linktext'] = 'Login'
            template_values['url'] = users.create_login_url(self.request.uri)

        template = JINJA_ENVIRONMENT.get_template(filename)
        self.response.out.write(template.render(template_values))
        
class MainHandler(BaseHandler):
    def get(self):
        self.render_template('landing.html', {})

class JsonHandler(BaseHandler):
    def get(self):
        self.decorateHeaders();
        self.response.headers['Content-Type'] = 'application/json'
        todo_query = ToDoItem.query().fetch()
        json_array = []
        for todoitem in todo_query:
            new_dict = {
                "onCreateTimeStamp" : (todoitem.onCreateTimeStamp -  datetime.datetime(1970,1,1)).total_seconds(),
                 "onFinishTimeStamp" : (todoitem.onFinishTimeStamp -  datetime.datetime(1970,1,1)).total_seconds(),
                 "deadline" : todoitem.deadline,
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
                 "confirmSubmittedTimeStamp": (todoitem.confirmSubmittedTimeStamp -  datetime.datetime(1970,1,1)).total_seconds() 
            }
            json_array.append(new_dict)

##        obj = [
##            {"onCreateTimeStamp": time.time(),
##             "onFinishTimeStamp": time.time(),
##             "deadline": time.time(),
##             "predictedTime": time.time(),
##             "usedTime": 123,
##             "onCheckInTimeStamps": [time.time(),time.time()],
##             "onCheckOutTimeStamps": [time.time(),time.time()],
##             "taskDescription": "Stupid amos",
##             "taskType": "Stock take",
##             "reason": None ,
##             "auditorName": "Amos",
##             "managerName": "Jordan",
##             "confirmSubmitted": False,
##             "confirmSubmittedTimeStamp": time.time(),
##             "ID":id(2)},
##            
##            {"onCreateTimeStamp": time.time(),
##             "onFinishTimeStamp": time.time(),
##             "deadline": time.time(),
##             "predictedTime": time.time(),
##             "usedTime": 123,
##             "onCheckInTimeStamps": [time.time(),time.time()],
##             "onCheckOutTimeStamps": [time.time(),time.time()],
##             "taskDescription": "amos Stupid Stupid",
##             "taskType": "Stock take",
##             "reason": None ,
##             "auditorName": "Amos",
##             "managerName": "Jordan",
##             "confirmSubmitted": False,
##             "confirmSubmittedTimeStamp": time.time(),
##             "ID":id(3)}
##            ]

        self.response.out.write(json.dumps(json_array))

    def post(self):
        self.decorateHeaders();
        myjson = json.loads(self.request.body)
        todo = ToDoItem(
            onFinishTimeStamp = myjson['onFinishTimeStamp'],
            deadline = myjson['deadline'],
            predictedTime = myjson['predictedTime'],
            usedTime = myjson['usedTime'],
            onCheckInTimeStamps = myjson['onCheckInTimeStamps'],
            onCheckOutTimeStamps = myjson['onCheckOutTimeStamps'],
            taskDescription = myjson['taskDescription'],
            taskType = myjson['taskType'],
            reason = myjson['reason'],
            auditorName = myjson['auditorName'],
            managerName = myjson['managerName'],
            confirmSubmitted = myjson['confirmSubmitted'],
            confirmSubmittedTimeStamp = myjson['confirmSubmittedTimeStamp'],
            iD = myjson['iD'],
            checker = myjson['checker']
            )
        todo.put()
            
        

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/json', JsonHandler)
], debug=True)
