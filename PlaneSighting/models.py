from django.db import models
import os.path

APP_ROOT = os.path.abspath(os.path.dirname(__file__))

# Create your models here.
class Sighting(models.Model) :
   id = models.AutoField(primary_key=True)
   spotter = models.ForeignKey('Spotter', on_delete=models.PROTECT, default=1)
   location = models.ForeignKey('Location', on_delete=models.PROTECT, default=1)
   time = models.DateTimeField('Time of sighting', auto_now=True)
   nvp = models.IntegerField("Number of vapour trails", default=1)
   aircraft = models.ForeignKey('Aircraft', on_delete=models.PROTECT)
   markings = models.CharField(max_length=4096) # description of any markings on plane
   photos = models.CharField(max_length=4096) # img1;img2;...

   def NumberOfVapourTrails() :
      return nvp

def GetTypeChoice(type_type) :
   fpath = os.path.join(APP_ROOT, "static", type_type + ".cat")
   try:
      fcat = open(fpath)
      cat = ()
      i = 0
      for line in fcat :
         line = line.strip()
         if len(line) > 0 and line[0] != '#' :
            cat = cat + ((line, line),)
      return cat
   except IOError:
      return (('err', 'Error'),)

class Aircraft(models.Model) :
   id = models.AutoField(primary_key=True)
   type = models.CharField(max_length=25, choices=GetTypeChoice('aircraft'), default="unknown")
   engine = models.ForeignKey('Engine', on_delete=models.PROTECT, default=1)
   size = models.ForeignKey('Size', on_delete=models.PROTECT)
   wings = models.ForeignKey('Wings', on_delete=models.PROTECT)

class Engine(models.Model) :
   ENGINE_POSITION = (
      ('12', 'left-right'),
      ('123', 'left-cen-right'),
      ('1234', 'left-left-right-right'),
      ('123456','left-left-cen-cen-right-right'),
      ('other', 'other')
                      )
   type = models.CharField(max_length=25, choices=GetTypeChoice('engine'), default="unknown")
   number = models.IntegerField('Number of engines', default=1)
   positions = models.CharField(max_length=60, choices=ENGINE_POSITION)
   noise_desc = models.CharField(max_length=500, blank=True)
   noise_audio = models.CharField(max_length=1024) # wav1;wav2,...

class Size(models.Model) :
   LENGTH_CHOICE = (
      ('1', '10-20m'),
      ('2', '20-30m'),
      ('3', '30-40m'),
      ('4', '40-50m'),
      ('5', '50-60m'),
      ('6', '60-70m'),
      ('7', '70-80m'),
      ('8', '80-90m'),
      ('9', '90-100m'),
      ('10', '> 100m')
   )
   length = models.CharField('Length', max_length=3, choices=LENGTH_CHOICE)
   wingspan = models.CharField('Wing Span', max_length=3, choices=LENGTH_CHOICE)
   tailheight = models.CharField('Tail Height', max_length=3, choices=LENGTH_CHOICE)

   def __unicode__(self):
      return "Length: " + self.length + " Wing span: " + self.wingspan + " Tail height: " + self.tailheight


class Wings(models.Model) :
   number = models.IntegerField("Number of wings", default=2)
   position = models.CharField("Fuselage position", max_length=3, choices=(('A', 'Above'), ('B', 'Below'), ('M','Fixed at mid-point')))
   swept = models.IntegerField("Swept Rearwards (degrees)", default=10)

   def NumberOfWings() :
      return number

class Spotter(models.Model) :
   spotter_id = models.AutoField(primary_key=True)
   name = models.CharField(max_length=60)
   email = models.CharField(max_length=80)

   def __unicode__(self):
      return "" + str(self.spotter_id) + "-" + self.name + "-" + self.email

class Location(models.Model) :
   location_id = models.AutoField(primary_key=True)
   name = models.CharField(max_length=120)
   latitude = models.FloatField(default=0)
   longitude = models.FloatField(default=0)

   def __unicode__(self):
      return name + "(lat:" + self.latitude + ", long:" + self.longitude + ")"