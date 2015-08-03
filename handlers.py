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

class MainPaige(Handler):
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

# example dataset from which to design input
# make a Comment class
Comment = namedtuple('Comment', ['name', 'text'])

# example data
comments = [Comment('Phil', 'Add X and remove Y.'),
			Comment('Lindsey', 'Change Z.')]
		
app = webapp2.WSGIApplication([('/', MainPaige),
							   ('/stage1', Stage1),
							   ('/stage2', Stage2),
							   ('/stage3', Stage3),
							   ('/stage4', Stage4),
							   ('/stage5', Stage4),
							   ],
								debug=True)