from bmstu.models import Service, Request, Users, RequestService
from bmstu.serializers import *
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from minio import Minio
from django.http import HttpResponseBadRequest, HttpResponseServerError, HttpRequest, JsonResponse
from rest_framework.parsers import MultiPartParser
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .permissionss import *
from .test import *
import redis
import uuid
from django.conf import settings
from django.http import HttpResponse

session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


@swagger_auto_schema(method='post', request_body=UserSerializer)
@api_view(['Post'])
@permission_classes([AllowAny])
def create_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    is_moderator = request.data.get('is_moderator', False)

    if Users.objects.filter(email=email).exists():
        return Response({'status': 'Exist'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        Users.objects.create_user(email=email, password=password, is_moderator=is_moderator)
        return Response({'status': 'Success'}, status=status.HTTP_200_OK)
    else:
        return Response({'status': 'Error', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuth])
def user_info(request):
    try:
        access_token = request.COOKIES.get("access_token")

        if not access_token:
            return Response({'status': 'Error', 'message': 'Access token not provided'},
                            status=status.HTTP_400_BAD_REQUEST)

        if session_storage.exists(access_token):
            email = session_storage.get(access_token).decode('utf-8')
            user = Users.objects.get(email=email)
            application = Request.objects.filter(user_id=user.id, status=1).first()

            user_data = {
                "user_id": user.id,
                "email": user.email,
                "is_moderator": user.is_moderator,
                "current_cart": application.id if application else -1,
            }

            return Response(user_data, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Error', 'message': 'Session does not exist'},
                            status=status.HTTP_401_UNAUTHORIZED)
    except Users.DoesNotExist:
        return Response({'status': 'Error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'status': 'Error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(method='post', request_body=UserSerializer)
@api_view(['Post'])
@permission_classes([AllowAny])
def login(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'status': 'Error', 'message': 'Both email and password are required'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)

        if user is not None:
            random_key = str(uuid.uuid4())
            application = Request.objects.filter(user_id=user.id, status=1).first()

            user_data = {
                "user_id": user.id,
                "email": user.email,
                "access_token": random_key,
                "is_moderator": user.is_moderator,
                "current_cart": application.id if application else -1,
            }

            session_storage.set(random_key, email)
            response = Response(user_data, status=status.HTTP_201_CREATED)
            response.set_cookie("access_token", random_key)

            return response
        else:
            return Response({'status': 'Error', 'message': 'Invalid email or password'},
                            status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        return Response({'status': 'Error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['Post'])
@permission_classes([IsAuth])
def logout(request):
    try:
        access_token = request.COOKIES.get("access_token")

        if not access_token:
            return Response({'message': 'Token is not found in cookie'}, status=status.HTTP_401_UNAUTHORIZED)

        session_storage.delete(access_token)

        response = Response({'message': 'Logged out successfully'})
        response.delete_cookie('access_token')

        return response

    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuth])
def user_info(request):
    try:
        access_token = request.COOKIES["access_token"]
        print('access_token', access_token)
        if session_storage.exists(access_token):
            email = session_storage.get(access_token).decode('utf-8')
            user = Users.objects.get(email=email)
            application = Request.objects.filter(id=user.id).filter(status=1).first()
            user_data = {
                "user_id": user.id,
                "email": user.email,
                "is_moderator": user.is_moderator,
                "current_cart": application.id if application else -1,
            }
            print(user_data)
            return Response(user_data, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Error', 'message': 'Session does not exist'})
    except:
        return Response({'status': 'Error', 'message': 'Cookies are not transmitted'})


@api_view(['GET'])
@permission_classes([AllowAny])
def get_services(request, format=None):
    min_time = int(request.GET.get('min_time', 0))
    max_time = int(request.GET.get('max_time', 20))
    search_query = request.GET.get('search', '')
    service = Service.objects.filter(status=True).filter(name__icontains=search_query).filter(
        transition_time__range=(min_time, max_time))

    try:
        access_token = request.COOKIES["access_token"]
        username = session_storage.get(access_token).decode('utf-8')
        user_ind = Users.objects.filter(email=username).first()
        request = Request.objects.filter(user_id=user_ind.id, status=1).values_list('id', flat=True).first()
        serializer = ServiceSerializer(service, many=True)
        response_data = {
            'app_id': request,  # Черновая
            'service': serializer.data,
        }
        return Response(response_data)
    except:
        serializer = ServiceSerializer(service, many=True)
        result = {
            'service': serializer.data,
        }
        return Response(result)


@api_view(['Get'])
@permission_classes([AllowAny])
def get_service(request, id):
    """Возвращает 1 маршрут"""
    if not Service.objects.filter(id=id).exists():
        return Response(f"Такого маршрута нету")
    service = get_object_or_404(Service, id=id)
    serializer = ServiceSerializer(service)
    return Response(serializer.data)


@api_view(['Post'])
@permission_classes([AllowAny])
def post_service(request, format=None):
    serializer = ServiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['Put'])
@permission_classes([AllowAny])
def put_service(request, id, format=None):
    """Обновляет информацию о маршруте"""
    service = get_object_or_404(Service, id=id)
    serializer = ServiceSerializer(service, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@parser_classes([MultiPartParser])
@permission_classes([AllowAny])
def postImageToOption(request, id):
    if 'file' in request.FILES:
        file = request.FILES['file']
        subscription = Service.objects.get(id=id, status=True)

        client = Minio(endpoint="localhost:9000",
                       access_key='minioadmin',
                       secret_key='minioadmin',
                       secure=False)

        bucket_name = 'img'
        file_name = file.name
        file_path = "http://localhost:9000/navigator-images/" + file_name

        try:
            client.put_object(bucket_name, file_name, file, length=file.size, content_type=file.content_type)
            print("Файл успешно загружен в Minio.")

            serializer = ServiceSerializer(instance=subscription, data={'image': file_path}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return HttpResponse('Image uploaded successfully.')
            else:
                return HttpResponseBadRequest('Invalid data.')
        except Exception as e:
            print("Ошибка при загрузке файла в Minio:", str(e))
            return HttpResponseServerError('An error occurred during file upload.')

    return HttpResponseBadRequest('Invalid request.')


@api_view(['Put'])
@permission_classes([IsModerator])
def del_service(request, id, format=None):
    """Удаляет маршрут"""
    try:
        service = Service.objects.get(id=id)
    except Service.DoesNotExist:
        return Response(f"Маршрута с таким id не существует!", status=status.HTTP_404_NOT_FOUND)

    service.status = False
    service.save()

    service = Service.objects.filter(status=True)
    serializer = ServiceSerializer(service, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuth])
def get_requests(request, format=None):
    access_token = request.COOKIES["access_token"]
    try:
        email = session_storage.get(access_token).decode("utf-8")
        current_user = Users.objects.get(email=email)
    except:
        return Response("Сессия не найдена")

    date_format = "%Y-%m-%d"
    start_date_str = request.query_params.get("start_day", "2024-01-01")
    end_date_str = request.query_params.get("end_day", "2024-12-01")
    start = datetime.strptime(start_date_str, date_format).date()
    end = datetime.strptime(end_date_str, date_format).date()

    current_status = request.query_params.get("status", 0)

    if current_user.is_moderator:  # Модератор может смотреть заявки всех пользователей
        print("модератор")
        applications = Request.objects.filter(creation_date__range=(start, end))
    else:  # Авторизованный пользователь может смотреть только свои заявки
        print("user")
        applications = Request.objects.filter().filter(user_id=current_user.id).filter(creation_date__range=(start, end))

    if int(current_status):
        applications = applications.filter(status=int(current_status))

    applications = applications.order_by("creation_date")
    serializer = RequestSerializer(applications, many=True)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuth])
def add_to_request(request, id):
    """Добавляет услугу в последнюю заявку"""
    access_token = request.COOKIES["access_token"]
    username = session_storage.get(access_token).decode('utf-8')
    user = Users.objects.filter(email=username).first()
    if user is None:
        return Response('Пользователь не зарегистрирован')

    if not Service.objects.filter(id=id).exists():
        return Response("Маршрута с таким id не существует")

    service = Service.objects.get(id=id)

    request = Request.objects.filter(status=1, user_id=user.id).last()

    if request is None:
        request = Request.objects.create(user_id=user.id)

    try:
        request_service = RequestService.objects.get(request=request, service=service)
        request_service.save()
    except RequestService.DoesNotExist:
        request_service = RequestService(request=request, service=service)
        request_service.save()

    serializer = RequestSerializer(request)
    request_data = serializer.data

    request_services = RequestService.objects.filter(request=request)
    services_data = []
    for app_service in request_services:
        service_serializer = ServiceSerializer(app_service.service)
        service_data = service_serializer.data
        services_data.append(service_data)

    request_data['services'] = services_data

    return Response(request_data)


@api_view(['Get'])
def get_request(request, id, format=None):
    """Получить одну заявку"""
    req = get_object_or_404(Request, id=id)
    if request.method == 'GET':
        serializer = RequestSerializer(req)
        request_data = serializer.data

        # Получить связанные опции для заявки с полными данными из таблицы Service
        request_service = RequestService.objects.filter(request=req)
        service_data = []
        for app_service in request_service:
            service_serializer = ServiceSerializer(app_service.service)
            service_data.append(service_serializer.data)

        # Добавить данные об опциях в данные о заявке
        request_data['service'] = service_data

        return Response(request_data)


@api_view(["PUT"])
@permission_classes([AllowAny])
def update_by_user(request):
    ssid = request.COOKIES["access_token"]
    try:
        email = session_storage.get(ssid).decode('utf-8')
        current_user = Users.objects.get(email=email)
    except:
        return Response('Сессия не найдена')
    try:
        req = get_object_or_404(Request, user_id=current_user, status=1)
    except:
        return Response("Такой заявки не зарегистрировано")

    req.status = "Черновик"
    req.publication_date = datetime.now().date()
    req.save()
    serializer = RequestSerializer(req)
    return Response(serializer.data)


@swagger_auto_schema(method='put', request_body=RequestSerializer)
@api_view(['Put'])
@permission_classes([IsModerator])
def update_by_admin(request, id):
    access_token = request.COOKIES["access_token"]
    modername = session_storage.get(access_token).decode('utf-8')
    user = Users.objects.filter(email=modername).first()

    if not Request.objects.filter(id=id).exists():
        return Response(f"Заявки с таким id не существует!")

    request_status = request.data["status"]

    if int(request.data["status"]) not in [4, 5]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    application = Request.objects.get(id=id)
    if int(request.data["status"]) in [4]:
        application.completed_at = timezone.now()
    # app_status = application.status

    # if app_status == 5:
    #     return Response("Статус изменить нельзя")
    application.moderator_id = user.id
    application.status = request_status
    application.save()

    serializer = RequestSerializer(application, many=False)
    response = Response(serializer.data)
    response.setHeader("Access-Control-Allow-Methods", "PUT")
    return response


@api_view(['Delete'])
def del_request(request, id, format=None):
    request = get_object_or_404(Request, id=id)
    if request.status == '1':
        request.delete()
        return Response("Заявка удалена.")
    else:
        return Response("Статус заявки изменить нельзя. Заявка не является черновиком",
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([AllowAny])
def delete_service_from_request(request, request_id, service_id):
    if not Request.objects.filter(id=request_id).exists():
        return Response("Такой заявки нету", status=status.HTTP_404_NOT_FOUND)

    if not Service.objects.filter(id=service_id).exists():
        return Response("Такого маршрута нету", status=status.HTTP_404_NOT_FOUND)

    req = Request.objects.get(id=request_id)
    service = Service.objects.get(id=service_id)

    application_subscription = get_object_or_404(RequestService, requset=req, service=service)
    if application_subscription is None:
        return Response("Заявка не найдена", status=404)
    req.applicationsoptions_set.filter(service=service).delete()
    req.save()

    return Response("Опция была удалена из заявки", status=200)





@api_view(["PUT"])
@permission_classes([AllowAny])
@authentication_classes([])
def updateStatus(request, application_id):
    secret_key = request.data.get('secret_key', None)
    if secret_key != 'secret-async-key':
        return Response({'error': 'Invalid secret key'}, status=status.HTTP_403_FORBIDDEN)
    app_acc = get_object_or_404(Request, id=application_id)
    serializer = RequestSerializer(app_acc, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
