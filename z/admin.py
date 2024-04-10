from django.contrib import admin

from .models import Treasure, Token, Photo

# Register your models here.

class TreasureAdmin(admin.ModelAdmin):
    list_display = ["id", "date_posted"]

admin.site.register(Treasure, TreasureAdmin)
admin.site.register(Token)
admin.site.register(Photo)

