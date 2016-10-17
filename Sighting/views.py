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
import os.path

from Sighting.models import Sighting
from Sighting.models import Aircraft
from Sighting.models import Engine
from Sighting.models import Size
from Sighting.models import Wing
from Sighting.models import Spotter
from Sighting.models import Location
from Sighting.models import GetTypeChoice

APP_ROOT = os.path.abspath(os.path.dirname(__file__))
 
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

def writeDitaProperties(fdita, properties, indent) :
   fdita.write(indent + '   <properties>\n')
   for pname in properties.keys() :
      fdita.write(indent + '      <property>\n')
      fdita.write(indent + '      <proptype>' + pname + '</proptype>\n')
      fdita.write(indent + '      <propvalue>' + str(properties[pname]) + '</propvalue>\n')
      fdita.write(indent + '      </property>\n')

   fdita.write(indent + '   </properties>\n')

def saveSightingToDitaFile(sighting) :
   fpath = os.path.join(APP_ROOT, "dita", "sighting_" + str(sighting.id) + ".xml")
   fdita = open(fpath, 'w')
   fdita.write('<?xml version="1.0" encoding="utf-8"?>\n')
##   fdita.write('<!DOCTYPE topic PUBLIC "-//OASIS//DTD DITA Topic//EN" "reference.dtd">\n')

   fdita.write('<reference id="sighting_' + str(sighting.id) + '">\n')
   fdita.write('<title>Plane sighting #' + str(sighting.id) + '</title>\n')
   fdita.write('<refbody>\n')
   fdita.write('   <section>\n')
   fdita.write('      <title>Spotter details</title>\n')
   writeDitaProperties(fdita,
        {'Name': sighting.spotter.name, 'Email': sighting.spotter.email}, '      ')
   fdita.write('   </section>\n</refbody>\n</reference>\n')
   fdita.close()

#   <?xml version="1.0" encoding="utf-8"?>
#<!DOCTYPE task PUBLIC "-//OASIS//DTD DITA Task//EN"
# "C:/UTIL/dita-ot-2.3.2/plugins/org.dita.specialization.dita11/dtd/task.dtd">
#
#<task id="washcar" xml:lang="en-us">
#   <title>Washing the car</title>
#   <!-- shortdesc>Keep your car looking great by washing it regularly.</shortdesc -->
#   <taskbody>
#      <context>
#         <p>Keep your car looking great by washing it regularly.</p>
#         <simpletable>
#            <sthead><stentry>Column1</stentry>
#            <stentry>Column2</stentry></sthead>
#            <strow><stentry>Field1</stentry>
#            <stentry>Field2</stentry></strow>
#         </simpletable>
#      </context>
#      <!--<context><p></p></context>-->
#      <steps>
#         <step>
#            <cmd>
#               Rinse the car by spraying clean water
#               from the hose.
#            </cmd>
#         </step>
#         <step>
#            <cmd>Dry the car using a dampened chamois.</cmd>
#         </step>
#      </steps>
#      <result>
#         <p>Very good results.</p>
#      </result>
#   </taskbody>
#</task>

def service(request) :
   jdata = json.loads(request.body)
   cmd = jdata['cmd']
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
      sighting = Sighting()
      spotter_v = jdata['spotter'] # name, email
      spotter = Spotter.objects.filter(name=spotter_v['name']).first()
      if spotter == None :
         spotter = Spotter(name=spotter_v['name'], email=spotter_v['email'])
         spotter.save()
      sighting.spotter = spotter

      location_v = jdata['location'] # name, lat(f), long(f)
      loc = Location.objects.filter(name=location_v['name']).first()
      if loc == None :
         loc = Location(name=location_v['name'], latitude=location_v['lat'], longitude=location_v['long'])
         loc.save()
      sighting.location = loc

      ddmmyy = jdata['date'].split('/') # dd/mm/yyyy
      hhmm = jdata['time'].split(':')  # hh:mm
      sighting.time = datetime(int(ddmmyy[2]), int(ddmmyy[1]), int(ddmmyy[0]), int(hhmm[0]), int(hhmm[1]))
      sighting.nvp = int(jdata['nvp'])

      acrft = jdata['aircraft'] # type, engine{} size{} wing{}
      acEngine = acrft['engine'] # type, number, positions, noise_desc, noise_audio
      acSize = acrft['size'] # length,wingspan,tail
      acWing = acrft['wing'] # number,position,swept

      kvargs = {'type': acEngine['type'], 'number': acEngine['number'], 'positions': acEngine['positions'],
                'noise_desc': acEngine['noise_desc'], 'noise_audio':acEngine['noise_audio']}
      engine = Engine.objects.filter(**kvargs).first()
      if engine == None :
         engine = Engine(**kvargs)
         engine.save()

      kvargs = {'length':acSize['length'], 'wingspan':acSize['wingspan'], 'tailheight':acSize['tail']}
      size = Size.objects.filter(**kvargs).first()
      if size == None :
        size = Size(**kvargs)
        size.save()

      kvargs = {'number':acWing['number'], 'position':acWing['position'], 'swept':acWing['swept']}
      wing = Wing.objects.filter(**kvargs).first()
      if wing == None :
         wing = Wing(**kvargs)
         wing.save()

      aircraft = Aircraft(type=acrft['type'], engine=engine, size=size, wing=wing)
      aircraft.save()

      sighting.aircraft = aircraft
      sighting.markings = jdata['markings']
      sighting.photos = jdata['photos']
      sighting.save()

      for s in Sighting.objects.all() :
         saveSightingToDitaFile(s)

      return JsonResponse({'ok': 'Your sighting saved successfully (id=' + str(sighting.id) + ')'})

   return JsonResponse({'err': 'Error in processing command:' + cmd })

