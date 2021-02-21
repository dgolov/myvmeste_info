"""myvmeste URL Configuration"""
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('myvmeste_admin/', admin.site.urls),
    path('', include('web.urls')),
    path('profile/', include('profiles.urls')),
    path('news/', include('news.urls')),
    path('api/', include('api.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
