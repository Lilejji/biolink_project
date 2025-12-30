from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings # Add this
from django.conf.urls.static import static # Add this

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. Handle the Home Page first (Redirect to admin)
    path('', lambda request: redirect('/admin/'), name='home'),
    
    # 2. Hand over everything else to the 'links' app
    # We do NOT add <slug:slug> here! The links app will handle it.
    path('', include('links.urls')),
]

# 3. Media settings for images
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)