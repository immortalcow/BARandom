from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("randomize/", views.randomize, name="randomize"),
]

if not settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
