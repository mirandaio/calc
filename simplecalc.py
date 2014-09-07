import os
import webapp2
import jinja2
import calc

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):
    def get(self):
        self.render('index.html')

    def post(self):
        expr = str(self.request.get('expr'))
        session = str(self.request.get('session')
        result = str(calc.calc(expr))
        self.response.write(result)

application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
