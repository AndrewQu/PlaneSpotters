from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

from Sighting.models import Sighting
from Sighting.models import Aircraft
from Sighting.models import Engine
from Sighting.models import Size
from Sighting.models import Wing
from Sighting.models import Spotter
from Sighting.models import Location
from Sighting.models import GetTypeChoice
 
def index(request) :
   return HttpResponse("Welcome to Plane Spotters Home: " + request.path + " !")

# Web UI for adding a new sighting
def add(request) :
   context = { 'spotters': Spotter.objects.all(),
               'locations' : Location.objects.all(),
               'engLocChoice' : Wing.LocationChoice,
               'sizeChoice' : Size.LENGTH_CHOICE,
               'engineTypes' : GetTypeChoice('engine'),
               'enginePos' : Engine.ENGINE_POSITION,
             }
   return render(request, 'add.html', context)

def save_sighting(request) :
   errmsg = "No information given to plane sighting - cannot save!"
   template = loader.get_template('adderr.html')
   context = RequestContext(request, {
        'errmsg': errmsg,
    })
   return HttpResponse(template.render(context))

def service(request) :
   cmd = request.GET.get("cmd", "")
   sid = 0
   if cmd == 'get_spotter' :
      sid = int(request.GET.get("id",""))
      spotters = Spotter.objects.filter(spotter_id=sid)
      if len(spotters) > 0 :
         return JsonResponse({'name': spotters[0].name, 'email': spotters[0].email })
      else : return JsonResponse({'err': 'Invalid spotter id: ' + str(sid) })
   elif cmd == 'get_loc' :
      sid = int(request.GET.get("id",""))
      locations = Location.objects.filter(location_id=sid)
      if len(locations) > 0 :
         return JsonResponse({'name': locations[0].name, 'lat': locations[0].latitude,
                             'long': locations[0].longitude })
      else : return JsonResponse({'err': 'Invalid spotter id: ' + str(sid) })


   return JsonResponse({'err':'sid=' + str(sid) + "  cmd=" + cmd })
