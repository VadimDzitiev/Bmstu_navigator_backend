from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from bmstu.views import *
from bmstu_navigator import settings

from django.urls import include, path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from rest_framework import permissions
from rest_framework import routers

router = routers.DefaultRouter()

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',

        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


app_name = 'myapp'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('create/', create_user, name='create'),#+
    path('login/', login, name='login'),#+
    path('logout/', logout, name='logout'),#+
    path('user_info/', user_info, name='user_info'),#+,

    path(r'Service/', get_services, name='services-list'),#+
    path(r'Service/post/', post_service, name='service-post'),#?
    path(r'Service/<int:id>', get_service, name='service'),#+
    path(r'Service/<int:id>/put/', put_service, name='service-put'),#+
    path(r'Service/<int:id>/del/', del_service, name='service-del'),#+
    path(r'Service/<int:id>/add_to_request/', add_to_request, name='service-add-to-request'),#?
    path(r'Service/<int:id>/image/post/', postImageToOption),

    path(r'Requests/', get_requests, name='requests-list'),
    path(r'Requests/<int:id>/', get_request, name='request'),#+
    path(r'Requests/<int:id>/update_by_user/', update_by_user, name='update_by_user'),
    path(r'Requests/<int:id>/update_by_admin/', update_by_admin, name='update_by_admin'),
    path(r'Requests/<int:id>/delete/', del_request, name='request-delete'),#+
    path(r'Requests/<int:request_id>/delete_service/<int:service_id>/', delete_service_from_request, name='delete_service_from_request'),#+

    # path('', GetCampuses),
    # path('transition/<int:id>/', GetCampus, name='campus_url'),
    # path('freeze_transition/<int:account_id>/', freezeTransition, name='freeze_transition'),
    path('api/time/<int:request_id>/put/', updateStatus, name='test'),

]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






