from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from datetime import datetime
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import os
import json
import sys

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
               'aircraftTypes': GetTypeChoice('aircraft'),
             }
   return render(request, 'add.html', context)

def save_sighting(request) :
   errmsg = "No information given to plane sighting - cannot save!"
   template = loader.get_template('adderr.html')
   context = RequestContext(request, {
        'errmsg': errmsg,
    })
   return HttpResponse(template.render(context))

def uploadfile(request) :
    # request to display the upload file page
    if request.method != 'POST' :
       return JsonResponse({'err':'Invalid file uplaod request!'})
    else :
       # Upload (post) a selected file
       files = request.FILES.getlist('audio_file')
       if len(files) == 0 :
          files = request.FILES.getlist('img_file')
       if len(files) == 0 :
          return JsonResponse({'path':'No files uploaded'})
       fname, fext = os.path.splitext(files[0].name)
       fpath = datetime.now().strftime("%Y_%m_%d-%H_%M_%S") + fext
       fs = FileSystemStorage()
       filename = fs.save(fpath, files[0])
       return JsonResponse({'path': fpath})

def service(request) :
   jdata = json.loads(request.body)
   cmd = jdata['cmd'] ## request.GET.get("cmd", "")
#   sys.stdout.write("*** cmd=" + cmd + "\n")
   sid = 0
   if cmd == 'get_spotter' :
      sid = int(jdata["id"])
      spotters = Spotter.objects.filter(spotter_id=sid)
      if len(spotters) > 0 :
         return JsonResponse({'name': spotters[0].name, 'email': spotters[0].email })
      else : return JsonResponse({'err': 'Invalid spotter id: ' + str(sid) })
   elif cmd == 'get_loc' :
      sid = int(jdata["id"])
      locations = Location.objects.filter(location_id=sid)
      if len(locations) > 0 :
         return JsonResponse({'name': locations[0].name, 'lat': locations[0].latitude,
                             'long': locations[0].longitude })
      else : return JsonResponse({'err': 'Invalid spotter id: ' + str(sid) })
   elif cmd == 'save_sighting' :
      spotter_v = jdata['spotter'] # name, email
      location_v = jdata['location'] # name, lat(f), long(f)
      aircraft = jdata['aircraft'] # type, engine{} size{} wing{}
      acEngine = aircraft['engine'] # type, number, positions, noise_desc, noise_audio
      acSize = aircraft['size'] # length,wingspan,tail
      acWing = aircraft['wing'] # number,position,swept

      photos = jdata['photos']
      date_v = jdata['date']
      time_v = jdata['time']
      markings = jdata['markings']
      nvp = jdata['nvp']
      return JsonResponse({'ok': 'wing ' + acWing['number']})

   return JsonResponse({'err':'Error: sid=' + str(sid) + "  cmd=" + cmd })

