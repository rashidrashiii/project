import os
#from settings import SITE_ROOT

# DEBUG = True
# TEMPLATE_DEBUG = DEBUG
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sqlite is the quick an easy development db
DATABASES = {
  'default': {
      'ENGINE': 'django.db.backends.sqlite3',
      'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
  }
}