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

# router.register(r'user', views.UserViewSet, basename='user')

urlpatterns = [
    path('create/', create, name='create'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('user_info/', user_info, name='user_info'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('admin/', admin.site.urls),
    path('', GetCampuses),
    path('transition/<int:id>/', GetCampus, name='campus_url'),
    path('freeze_transition/<int:account_id>/', freezeTransition, name='freeze_transition'),

    path(r'Service/', get_list_services, name='services-list'),#GET
    path(r'Service/<int:id>', get_service, name='service'),#GET
    path(r'Service/<int:id>/put/', put_detail_service, name='service-put'),#PUT
    path(r'Service/post/', post_service, name='service-post'),#POST
    path(r'Service/post/<int:id>', post_service_in_request, name='post_service_in_request-application-post'),
    path(r'Service/<int:id>/del/', del_service, name='service-del'),  # PUT
    path(r'Service/<int:id>/add_to_request/', add_to_request, name='service-add-to-request'),



    path(r'Request/', get_list_requests, name='requests-list'),#GET
    path(r'Request/post/', post_request, name='request-post'),  # POST
    path(r'Request/<int:id>/delete/', delete_request, name='request-delete'),#DELETE
    path(r'Request/<int:request_id>/delete_service/<int:service_id>/', delete_service_from_request,name='delete_service_from_request'),#DELETE

    path(r'RequestService/', get_list_requestservices, name='requestservice-list'),#GET
    path(r'RequestService/put/', put_requestservice, name='requestservice-put'),  # Put
    path(r'RequestService/<int:id1>/<int:id2>/delete/', delete_requestservice, name='requestservice-delete'),#DELETE

    path(r'UserProfile/', get_list_userprofiles, name='userprofile-list'),#GET
    path(r'UserProfile/post/', post_userprofile, name='userprofile-post'),  # POST
    path(r'UserProfile/<int:id>/delete/', delete_userprofile, name='userprofile-delete'),#DELETE
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






