=====
Django Todo Manager
=====
Django Task is the for apis for a todo app in django.
Detailed documentation is in the "docs" directory.
Quick start
-----------
1. Add "api" to your INSTALLED_APPS setting like this::
INSTALLED_APPS = [
        ...
        'api',
    ]
2. Include the polls URLconf in your project urls.py like this::
url(r'^api/', include('api.urls')),
3. Run `python manage.py migrate` to create the polls models.
4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a task
