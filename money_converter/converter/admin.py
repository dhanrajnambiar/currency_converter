from django.contrib import admin

from .models import client, transaction
# Register your models here.
class clientAdmin(admin.ModelAdmin):
    list_display = ('user',)

class transactionAdmin(admin.ModelAdmin):
    list_display = ('text','creator','trans_time')

admin.site.register(transaction, transactionAdmin)
admin.site.register(client, clientAdmin)
