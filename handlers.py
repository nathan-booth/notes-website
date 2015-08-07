import os
import webapp2
import jinja2
from google.appengine.ext import ndb

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class CoursePaige(Handler):
    def get(self):
        self.render("course_toc.html")

class Stage1(Handler):
    def get(self):
        self.render("stage1.html")

class Stage2(Handler):
    def get(self):
        self.render("stage2.html")

class Stage3(Handler):
    def get(self):
        self.render("stage3.html")

class Stage4(Handler):
    def get(self):
        self.render("stage4.html")

class Stage5(Handler):
    def get(self):
        self.render("stage5.html")

class Comment(ndb.Model):
    name = ndb.StringProperty()
    comment_content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

class CommentsHandler(CoursePaige):
    def get(self):
        comments_query = Comment.query(ancestor=comment_key).order(-Comment.date)
        comments = comments_query.fetch()

        blank_error = self.request.get('blank_error')

        self.render("comments.html", comments=comments, blank_error=blank_error)

    def post(self):
        comment = Comment(parent=comment_key)
        comment.name = self.request.get('name')
        comment.comment_content = self.request.get('comment_content')
        blank_error = ''

        if comment.name == '' or comment.comment_content == '' or len(comment.name) > 15 or len(comment.comment_content) > 1000:
            blank_error = "Please, fill out both the name and comment sections."
        else:
            comment.put()

        self.redirect('/comments?blank_error='+blank_error)

comment_key = ndb.Key('Comment', 'course_toc')

app = webapp2.WSGIApplication([('/', CoursePaige),
                               ('/stage1', Stage1),
                               ('/stage2', Stage2),
                               ('/stage3', Stage3),
                               ('/stage4', Stage4),
                               ('/stage5', Stage4),
                               ('/comments', CommentsHandler)
                               ],
                                debug=True)