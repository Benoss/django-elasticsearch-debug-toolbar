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
        "APP_DIRS": True,
    },
]
