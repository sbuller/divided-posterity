from django.template import Context, loader
from django.http import HttpResponse

# Create your views here.

def index(request):
		  t = loader.get_template('inventory.html.djt')
		  return HttpResponse (t.render(Context({
					 })))
