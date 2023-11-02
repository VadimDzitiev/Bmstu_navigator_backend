from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from bmstu.views import *
from bmstu_navigator import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', GetCampuses),
    path('transition/<int:id>/', GetCampus, name='campus_url'),
    path('freeze_transition/<int:account_id>/', freezeTransition, name='freeze_transition'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




