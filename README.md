# PlaneSpotters - Demonstrating the use of Django, Eclipse plugin, DITA publishing
Development notes:
1. python --version --- 2.7.2
2. python -m django --version --- 1.10.2
3. django-admin startproject PlaneSpoters --- Create project
4. python manage.py runserver 0.0.0.0:8000 --- Test initial project
5. python manage.py startapp Sighting --- Create a ew application
6. Add index() view to Sighting/views.py
7. Match index view to a url in Sighting/urls.py: url(r'^$', views.index, name='index'),
8. Match site url in PlaneSpotters/urls.py: url(r'^(?i)Sighting/', include('Sighting.urls')),
9. Add models to Sighting/models.py
10. Change Sighting app to INSTALLED_APPS in settings.py: 'Sighting.apps.SightingConfig',
11. python manage.py makemigrations --- Generate db migration scripts
12. python manage.py migrate --- Actually apply db migration.
13. python manage.py createsuperuser --- root/PlaneSpotters
14. visit localhost:8000/admin/
15. Edit Sighting/admin.py and admin.site.register(Sighting),...
16. Add dita processing