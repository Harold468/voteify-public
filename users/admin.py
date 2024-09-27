from django.contrib import admin
from users.models import *
# Register your models here.

class USERADMIN(admin.ModelAdmin):
    list_display= ['email','name','phone_number','active','staff','admin','superuser','created_on']

    def superuser(self,obj):
        return obj.is_superuser
    
    def admin(self,obj):
        return obj.is_admin
    
    def staff(self,obj):
        return obj.is_staff
    
    def active(self,obj):
        return obj.is_active
    
    def created_on(self,obj):
        return obj.createAt
    
    def phone_number(self,obj):
        return obj.phone

admin.site.register(USERMODEL,USERADMIN)


class EVENTADMIN(admin.ModelAdmin):
    list_display = ['name_of_event','event_organizer','event_picture','paid','amount','from_date','to_date']

admin.site.register(EVENT,EVENTADMIN)