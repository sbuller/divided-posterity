from django.template import Context, loader
from django.http import HttpResponse

# Create your views here.

def index(request, template):
		  t = loader.get_template("%s.djt" % template)
		  return HttpResponse (t.render(Context({
					 })))
