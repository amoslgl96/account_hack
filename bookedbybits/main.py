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
        if self.user:
            self.render_template('index.html', {})
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
        self.decorateHeaders();
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
                                       userName = self.user.nickname()
                                       )
                else: #employee
                    new_employee = Employee(id = self.user.nickname(),
                                       isManager = False,
                                       userName = user.nickname()
                                       )
                new_employee.put()
        else:
            self.redirect('/') #go back to landing to login
            

        
        

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/getcurrentuser', UserHandler),
    ('/json', JsonHandler)
], debug=True)
