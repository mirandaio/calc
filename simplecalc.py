import os
import webapp2
import jinja2
import calc

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class Session(db.Model):
    name = db.StringProperty(required = True)
    content = db.TextProperty(required = True)

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
        session = str(self.request.get('session'))
        tokens = expr.split()

        if len(tokens) == 2 and tokens[0] == 'guardar':
            saved_sessions = db.GqlQuery('SELECT * FROM Session WHERE ' +
                'name = :1', tokens[1])

            if saved_sessions.count() > 0:
                for s in saved_sessions:
                    s.content = session
                    s.put()
            else:
                s = Session(name=tokens[1], content=session)
                s.put()

            self.response.write('sesion almacenada')
        elif len(tokens) == 2 and tokens[0] == 'recuperar':
            saved_sessions = db.GqlQuery('SELECT * FROM Session WHERE ' +
                'name = :1', tokens[1])

            print 'count:', saved_sessions.count()

            if saved_sessions.count() == 0:
                self.response.write('sesion no encontrada')
            else:
                self.response.write(saved_sessions[0].content)
        else: 
            result = str(calc.calc(expr))
            self.response.write(result)

application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
