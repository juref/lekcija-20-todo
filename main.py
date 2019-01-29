#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time

import jinja2
import webapp2
from models import Todo

reload(sys)
sys.setdefaultencoding('utf8')


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        list = Todo.query(Todo.deleted == False).fetch()
        deleted = Todo.query(Todo.deleted == True).fetch()

        params = {"list": list, "deleted": deleted}

        return self.render_template("index.html", params=params)


class AddHandler(BaseHandler):
    def get(self):
        list = Todo.query(Todo.deleted == False).fetch()
        deleted = Todo.query(Todo.deleted == True).fetch()
        task = ""

        params = {"list": list, "deleted": deleted, "task": task}

        return self.render_template("add.html", params=params)

    def post(self):
        status = self.request.get("status")
        task = self.request.get("task")

        if status == "True":
            status = True
        else:
            status = False

        new_task = Todo(task=task, status=status)
        new_task.put()
        time.sleep(1)
        list = Todo.query(Todo.deleted == False).fetch()
        deleted = Todo.query(Todo.deleted == True).fetch()

        params = {"list": list, "deleted": deleted}

        return self.render_template("index.html", params=params)


class EditHandler(BaseHandler):
    def get(self, task_id):
        edit = Todo.get_by_id(int(task_id))
        # if edit.status == "True":
        #     status = True
        # else:
        #     status = False

        params = {"task": edit}

        return self.render_template("add.html", params=params)

    def post(self, task_id):
        status = self.request.get("status")
        task = self.request.get("task")

        edit = Todo.get_by_id(int(task_id))

        if status == "True":
            status = True
        else:
            status = False

        edit.task = task
        edit.status = status

        edit.put()
        time.sleep(1)
        list = Todo.query(Todo.deleted == False).fetch()
        deleted = Todo.query(Todo.deleted == True).fetch()

        params = {"list": list, "deleted": deleted}

        return self.render_template("index.html", params=params)


class DeleteHandler(BaseHandler):
    def get(self, task_id):
        edit = Todo.get_by_id(int(task_id))
        params = {"task": edit}

        return self.render_template("delete.html", params=params)

    def post(self, task_id):
        edit = Todo.get_by_id(int(task_id))

        edit.deleted = True

        edit.put()
        time.sleep(1)
        list = Todo.query(Todo.deleted == False).fetch()
        deleted = Todo.query(Todo.deleted == True).fetch()

        params = {"list": list, "deleted": deleted}

        return self.render_template("index.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/add', AddHandler),
    webapp2.Route('/edit/<task_id:\d+>', EditHandler),
    webapp2.Route('/delete/<task_id:\d+>', DeleteHandler),
], debug=True)
