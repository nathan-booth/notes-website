import os
import webapp2
import jinja2
from google.appengine.ext import ndb
# forcing sleep for testing
import time

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

# Model for individual comment
class Comment(ndb.Model):
	name = ndb.StringProperty()
	comment_content = ndb.StringProperty()
	date = ndb.DateTimeProperty(auto_now_add=True)

class CommentsHandler(CoursePaige):
	def get(self):
		# enable queries
		comments_query = Comment.query(ancestor=comment_key).order(-Comment.date)
		comments = comments_query.fetch()

		self.render("comments.html")

	def post(self):
		comment = Comment(parent=comment_key)
		comment.name = self.request.get('name')
		comment.comment_content = self.request.get('comment_content')
		# temp, for testing
		comment.put()

		# will be for validation
		# if comment.name == '' or comment.comment_content == '':
		# 	self.redirect('/?error=Please fill out the name and comment sections.')
		# else:
		# 	comment.put()

		self.redirect('/comments')

comment_key = ndb.Key('Comment', 'course_toc')

# # populate datastore for testing
# comment1 = Comment(name='Phil', comment='Add X.')
# comment2 = Comment(name='Nadia', comment='Remove Y.')
# comment3 = Comment(name='John', comment='Change Z.')

# # update datastore
# comment1.put()
# comment2.put()
# comment3.put()
# # all time for datastore update
# time.sleep(.1)

app = webapp2.WSGIApplication([('/', CoursePaige),
							   ('/stage1', Stage1),
							   ('/stage2', Stage2),
							   ('/stage3', Stage3),
							   ('/stage4', Stage4),
							   ('/stage5', Stage4),
							   ('/comments', CommentsHandler)
							   ],
								debug=True)