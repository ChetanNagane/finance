from django.contrib import admin
from .models import User, Stocks, History


# Register your models here.
admin.site.register(User)
admin.site.register(Stocks)
admin.site.register(History)
