from django.contrib import admin
from .models import *
# Register your models here.

class ContestantAdmin(admin.ModelAdmin):
    list_display = ['name','event']

admin.site.register(ContestantInfo,ContestantAdmin)
admin.site.register(ContestanInfoImages)

class VotesAdmin(admin.ModelAdmin):
    list_display = ['id','vote','total_balance','paid','contestant']

    
    def paid(self,obj):
        return obj.event.paid
    
    def total_balance(self,obj):
        return obj.event.total_balance
    
    
admin.site.register(Votes,VotesAdmin)