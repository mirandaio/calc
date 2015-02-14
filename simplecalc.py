import webapp2
import calc

from google.appengine.ext import db

with open('views/index.html', 'r') as template:
    home = template.read()

with open('views/help.html', 'r') as h:
    helpcontent = h.read()

class Session(db.Model):
    name = db.StringProperty(required = True)
    content = db.TextProperty(required = True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        with open('views/index.html', 'r') as front:
            home = front.read()
        self.response.write(home)

    def post(self):
        expr = str(self.request.get('expr'))
        session = str(self.request.get('session'))
        tokens = expr.split()

        if expr == 'h':
            self.response.write(helpcontent)
        elif len(tokens) == 2 and tokens[0] == 'save':
            saved_sessions = db.GqlQuery('SELECT * FROM Session WHERE ' +
                'name = :1', tokens[1])

            if saved_sessions.count() == 1:
                for s in saved_sessions:
                    s.content = session
                    s.put()
            else:
                s = Session(name=tokens[1], content=session)
                s.put()

            self.response.write('session saved')
        elif len(tokens) == 2 and tokens[0] == 'load':
            saved_sessions = db.GqlQuery('SELECT * FROM Session WHERE ' +
                'name = :1', tokens[1])

            if saved_sessions.count() == 0:
                self.response.write('session not found')
            else:
                self.response.write(saved_sessions[0].content)
        else:
            try:
                result = calc.calc(expr)
                self.response.write(result)
            except Exception, e:
                self.response.write(e)

application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
