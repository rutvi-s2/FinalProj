
from django.contrib import admin
# TODO: delete author later
from coloring.models import Author
from coloring.models import User
from coloring.models import Posting

# Register your models here.
# https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#modeladmin-objects

admin.site.register(User)
admin.site.register(Posting)


