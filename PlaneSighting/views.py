# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

from PlaneSighting.models import Sighting
from PlaneSighting.models import Aircraft
from PlaneSighting.models import Engine
from PlaneSighting.models import Size
from PlaneSighting.models import Wings
from PlaneSighting.models import Spotter
from PlaneSighting.models import Location
 
def index(request) :
   return HttpResponse("Welcome to Plane Spotters Home: " + request.path + " !")

# Web UI for adding a new sighting
def add(request) :
   template = loader.get_template('add.html')
   spotters = Spotter.objects.all()
   context = RequestContext(request, {
        'spotters': spotters,
    })
   return HttpResponse(template.render(context))

def save_sighting(request) :
   errmsg = "No information given to plane sighting - cannot save!"
   template = loader.get_template('adderr.html')
   context = RequestContext(request, {
        'errmsg': errmsg,
    })
   return HttpResponse(template.render(context))

def service(request) :
   cmd = request.POST.get("cmd", "")
   sid = "no id"
   if cmd == 'get_spotter' :
      sid = request.POST.get("id","")

   return HttpResponse(sid)