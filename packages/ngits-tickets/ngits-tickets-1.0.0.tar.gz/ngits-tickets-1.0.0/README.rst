ngits-tickets
=============

Bazowa aplikacja 'tickets' dla projektów Django

Instalacja
----------

1. Zainstaluj paczkę następującą komendą:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

       pip install ngits-tickets

2. Dodaj następujące wartości do ustawień projektu Django:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

       INSTALLED_APPS = [
           ...
           "rest_framework",
           "rest_framework.authtoken",
           "tickets"
       ]

       ...

       REST_FRAMEWORK = {
           "DEFAULT_AUTHENTICATION_CLASSES": [
               "rest_framework.authentication.TokenAuthentication",
           ],
           # Optional
           "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
       }

3. Dodaj ścieżki do ``urls.py``:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

       from django.urls import path, include

       urlpatterns = [
           ...
           path("/", include("tickets.urls")),
       ]

4. Uruchom polecenie:
~~~~~~~~~~~~~~~~~~~~~

::

       py manage.py migrate


5. Konfiguracja opcjonalna:
~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

       pip install drf-spectacular==0.23.*

``settings.py``:

::

       INSTALLED_APPS = [
           ...
           "drf_spectacular"
       ]

       SPECTACULAR_SETTINGS = {
           "TITLE": "<proj_name> API",
           "VERSION": "1.0.0",
       }

       TEMPLATES = [
           ...
           'DIRS': [ BASE_DIR / "templates"],
           ...
       ]

``../<django_project>/templates/redoc.html``:

::

       <!DOCTYPE html>
       <html>
           <head>
               <title>ReDoc</title>
               <!-- needed for adaptive design -->
               <meta charset="utf-8"/>
               <meta name="viewport" content="width=device-width, initial-scale=1">
               <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
               <!-- ReDoc doesn't change outer page styles -->
               <style>
                   body {
                       margin: 0;
                       padding: 0;
                   }
               </style>
           </head>
           <body>
               <redoc spec-url='{% url schema_url %}'></redoc>
               <script src="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"> </script>
           </body>
       </html>
