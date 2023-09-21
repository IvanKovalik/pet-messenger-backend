from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('api/', include('api.urls')),
    path('profiles/', include('profiles.urls')),
]
