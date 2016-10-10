from django.contrib import admin

from Sighting.models import Sighting
from Sighting.models import Aircraft
from Sighting.models import Engine
from Sighting.models import Size
from Sighting.models import Wing
from Sighting.models import Spotter
from Sighting.models import Location

# Register your models here.
admin.site.register(Spotter)
admin.site.register(Location)
admin.site.register(Aircraft)
admin.site.register(Engine)
admin.site.register(Size)
admin.site.register(Wing)
admin.site.register(Sighting)
