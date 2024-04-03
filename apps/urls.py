from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from root import settings

urlpatterns = [

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                        document_root=settings.MEDIA_ROOT)
