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

from models import ToDoItem, Employee

from google.appengine.ext import ndb
from google.appengine.api import users
from oauth2client.client import GoogleCredentials

import httplib2
#from firebase import firebase

_FIREBASE_SCOPES = [
    'https://www.googleapis.com/auth/firebase.database',
    'https://www.googleapis.com/auth/userinfo.email']



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
        self.user = users.get_current_user()
        if self.user: #if logged in
            query = Employee.get_by_id(self.user.nickname())
            if query: #account created
                self.render_template('index.html', {})
            else:
                self.redirect('/getcurrentuser')
        else:
            self.render_template('landing.html', {})

class JsonHandler(BaseHandler):
    def get(self):
        self.decorateHeaders();
        self.response.headers['Content-Type'] = 'application/json'
        todo_query = ToDoItem.query().fetch()
        json_array = ToDoItem.toJson(todo_query)
        self.response.out.write(json.dumps(json_array))

    def post(self):
        self.decorateHeaders();
        myjson = json.loads(self.request.body)
        logging.info(myjson)
        ToDoItem.createFromJson(myjson)
        

class UserHandler(BaseHandler):
    def get(self):
        self.decorateHeaders()
        self.user = users.get_current_user()
        if self.user:#logged in
            query = Employee.get_by_id(self.user.nickname())
            if query: #account has been created
                self.response.headers['Content-Type'] = 'application/json'
                json_dict = Employee.toJson(query)
                json_dict["logout_link"] = users.create_logout_url(self.request.uri)
                self.response.out.write(json.dumps(json_dict))
            else: #no account, create account
                if self.request.get('isManager') == "true": #is manager
                    new_employee = Employee(id = self.user.nickname(),
                                       isManager = True,
                                       )
                else: #employee
                    new_employee = Employee(id = self.user.nickname(),
                                       isManager = False,
                                       )
                new_employee.put()
                self.redirect('/')                
        else:
            self.redirect('/') #go back to landing to login

    def post(self):
        self.decorateHeaders()
        myjson = json.loads(self.request.body)
        Employee.toDataStore(myjson)
        

            

class AllUserHandler(BaseHandler):
    def get(self):
        self.decorateHeaders()
        self.response.headers['Content-Type'] = 'application/json'
        employee_query = Employee.query().fetch()
        json_array = Employee.toJson(employee_query)
        self.response.out.write(json.dumps(json_array))


        
class PushTest(BaseHandler):
    def get(self):
        logging.info("yooo")
        self.render_template('push.html', {})


def _get_http():
    """Provides an authed http object."""
    http = httplib2.Http()
    # Use application default credentials to make the Firebase calls
    # https://firebase.google.com/docs/reference/rest/database/user-auth
    creds = GoogleCredentials.get_application_default().create_scoped(
        _FIREBASE_SCOPES)
    creds.authorize(http)
    return http
    
def firebase_put(path, value=None):
    """Writes data to Firebase.

    An HTTP PUT writes an entire object at the given database path. Updates to
    fields cannot be performed without overwriting the entire object

    Args:
        path - the url to the Firebase object to write.
        value - a json string.
    """
    response, content = _get_http().request(path, method='PUT', body=value)
    logging.info("gig")
    logging.info(content)
    logging.info(response)
    return json.loads(content)

def firebase_get(path):
    """Read the data at the given path.

    An HTTP GET request allows reading of data at a particular path.
    A successful request will be indicated by a 200 OK HTTP status code.
    The response will contain the data being retrieved.

    Args:
        path - the url to the Firebase object to read.
    """
    response, content = _get_http().request(path, method='GET')
    return json.loads(content)






def parseActionJson(myjson):
    logging.info(myjson)
    return myjson["queryResult"]["intent"]["displayName"]
    
def doAction(intent):
    if intent == "check on my task":
        todo_query = ToDoItem.query().fetch()
        return str(len(todo_query))
    else:
        return "fuck you"

def insertToJson(response):
    sample_json = {"payload": {
                    "google": {
                      "expectUserResponse": True,
                      "richResponse": {
                        "items": [
                          {
                            "simpleResponse": {
                              "textToSpeech": response
                            }
                          }
                        ]
                      }
                    }
                  }
                }
    return sample_json

        
class PutTest(BaseHandler):
    def get(self):
        body = json.dumps({"text":"get"})
        self.response.out.write(firebase_put("https://bookedbybits.firebaseio.com/bookedbybits.json", body))

    def post(self):
        self.decorateHeaders()
        self.response.headers['Content-Type'] = 'application/json'
        body = json.dumps({"text":"activated by voice"})
        firebase_put("https://bookedbybits.firebaseio.com/bookedbybits.json", body)
        myjson = json.loads(self.request.body)
        intent = parseActionJson(myjson)
        response = doAction(intent)
        logging.info("write out!")
        logging.info(insertToJson(response))
        self.response.out.write(json.dumps(insertToJson(response)))
        
class Reset(BaseHandler):
    def get(self):
        body = json.dumps({"text":"reset"})
        self.response.out.write(firebase_put("https://bookedbybits.firebaseio.com/bookedbybits.json", body))
        


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/getcurrentuser', UserHandler),
    ('/json', JsonHandler),
    ('/getallusers', AllUserHandler),
    ('/push', PushTest),
    ('/put', PutTest),
    ('/reset', Reset)
], debug=True)
