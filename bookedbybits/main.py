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

#from models import Post, Place, Comment

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

class BaseHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app = self.app)

    def render_template(self,
        filename,
        template_values):
        self.user = users.get_current_user()
        if self.user:
          template_values['user']= user.nickname()
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
        self.render_template('index.html', {"hi":"yo"})

class ToDoListHandler(BaseHandler):
    def get(self):
        test_list = []
        for i in range(10):
            test_list.append(ToDo(i,i,i,i,i,i,i,i))
        self.render_template('list.html', {'to_do_list':test_list})

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/todolist', ToDoListHandler)
], debug=True)
