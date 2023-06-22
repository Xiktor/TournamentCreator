from django.contrib import admin

from app.models import Arena, Player, Result, Round, Tournament

admin.site.register(Arena)
admin.site.register(Player)
admin.site.register(Result)
admin.site.register(Round)
admin.site.register(Tournament)
