import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

INSTALLED_APPS = ["debug_toolbar", "elastic_panel"]

DEBUG_TOOLBAR_PANELS = [
    "elastic_panel.panel.ElasticDebugPanel",
]
SECRET_KEY = "test"
DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR + "/tests/templates"],
        "APP_DIRS": True,
    },
]
