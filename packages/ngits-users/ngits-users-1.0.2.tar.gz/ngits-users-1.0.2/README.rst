ngits-users
============

Base ‘users’ application for Django projects. It provides following endpoints:

    - Registration
    - Background registration
    - Login
    - Change password
    - Remind password
    - Delete account
    - Google authentication
    - Facebook authentication

... and following template views:

    - Verify account
    - Confirm password remind


Setup
-----

1. Install using pip:
~~~~~~~~~~~~~~~~~~~~~

::

       pip install ngits-users

2. Change your ``settings`` file:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

       import os

       ...

       INSTALLED_APPS = [
           ...
           "rest_framework",
           "rest_framework.authtoken",
           "users"
       ]

       ...

       AUTH_USER_MODEL = "users.User"

       CELERY_BROKER_URL = "<redis_url>"
       CELERY_RESULT_BACKEND = "<redis_url>"

       DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "<your_email>")

       REST_FRAMEWORK = {
           "DEFAULT_AUTHENTICATION_CLASSES": [
               "rest_framework.authentication.TokenAuthentication",
           ],
           # Optional
           "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
       }

       REGISTRATION_EMAIL_SUBJECT = "<email subject>"
       REMIND_EMAIL_SUBJECT = "<email subject>"

       # debugging
       EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

3. Add paths to your ``urls.py`` file:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

       from django.urls import path, include

       urlpatterns = [
           ...
           path("users/", include("users.urls"))
       ]

4. Run migrations:
~~~~~~~~~~~~~~~~~~

::

       py manage.py migrate

5. Add following variables to your ``.env`` file:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

      # smpt config
      DEFAULT_FROM_EMAIL=no-reply@ngits.dev

      EMAIL_HOST=
      EMAIL_HOST_PASSWORD=
      EMAIL_HOST_USER=
      EMAIL_PORT=

      # celery
      CELERY_BROKER_URL=
      CELERY_RESULT_BACKEND=

6. Celery configuration:
~~~~~~~~~~~~~~~~~~~~~~~~

``../<django_project>/<proj_name>/celery.py``

::


       import os

       from celery import Celery

       os.environ.setdefault("DJANGO_SETTINGS_MODULE", "<proj_name>.settings")

       app = Celery("<proj_name>")
       app.config_from_object("django.conf:settings", namespace="CELERY")
       app.autodiscover_tasks()

``../<django_project>/<proj_name>/__init__.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

      from .celery import app as celery_app

      __all__ = ("celery_app",)

7. Optional ``redoc`` configuration:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
