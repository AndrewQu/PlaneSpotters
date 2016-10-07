#
from django.contrib import admin
from PlaneSighting.models import Sighting
from PlaneSighting.models import Aircraft
from PlaneSighting.models import Engine
from PlaneSighting.models import Size
from PlaneSighting.models import Wings
from PlaneSighting.models import Spotter
from PlaneSighting.models import Location
 
admin.site.register(Spotter)
admin.site.register(Location)
admin.site.register(Aircraft)
admin.site.register(Engine)
admin.site.register(Size)
admin.site.register(Wings)
admin.site.register(Sighting)
