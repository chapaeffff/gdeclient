from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('scanner/', include('scanner.urls')),
    path('admin/', admin.site.urls),
]