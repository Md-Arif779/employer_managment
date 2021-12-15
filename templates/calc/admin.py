from django.contrib import admin
from .models import Post,Comment
# Register your models here.




admin.site.site_header = 'HelloCare.Com admin Panel'
admin.site.site_title = 'HelloCare.Com admin Panel'
admin.site.index_title = ''

class PostAdmin(admin.ModelAdmin):
    fields = ('user','Name')
    list_display = ('user','Name','DateTime','Category')
    search_fields = ('Details','user__username','Category','Phone','Email')
    
    
    
    
    
admin.site.register(Post,PostAdmin) 
admin.site.register(Comment)