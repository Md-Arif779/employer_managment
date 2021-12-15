
from django.contrib import admin
from django.urls import path,include
from .views import home
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',home,name="home"),
    path('calc/',include('calc.urls')),
    path('colc/',include('colc.urls')),
    path('notifications/',include('notifications.urls', namespace='notifications')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
