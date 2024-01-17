from minio import Minio
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from bmstu.models import Service, Request, UserProfile, RequestService
from bmstu.serializers import ServiceSerializer, RequestSerializer, UserProfileSerializer, RequestServiceSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils import timezone
import datetime

user = UserProfile.objects.get(id=1)


@api_view(['Get'])
def get_services(request, format=None):
    """Возвращает список маршрутов"""
    service = Service.objects.filter(status=True)
    serializer = ServiceSerializer(service, many=True)
    req = Request.objects.filter(status=1).first()
    if req:
        request_serializer = RequestSerializer(req)
        apps_data = [request_serializer.data]
    else:
        apps_data = []
    response_data = {
        'apps': apps_data,
        'service': serializer.data,
    }
    return Response(response_data)



@api_view(['Post'])
def post_service(request, format=None):
    """Добавить новый маршрут"""
    serializer = ServiceSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    new_service = serializer.save()

    client = Minio(endpoint="localhost:9000",
                   access_key='minioadmin',
                   secret_key='minioadmin',
                   secure=False)
    i = new_service.id - 1
    try:
        i = new_service.name
        img_rout_name = f"{i}.png"
        file_path = f"assets/img/{request.data.get('image')}"
        client.fput_object(bucket_name='pics',
                           object_name=img_rout_name,
                           file_path=file_path)
        new_service.image = f"http://localhost:9000/img/{img_rout_name}"
        new_service.save()
    except Exception as e:
        return Response({"error": str(e)})

    service = Service.objects.filter(status=True)
    serializer = ServiceSerializer(service, many=True)
    return Response(serializer.data)


@api_view(['Get'])
def get_service(request, id):
    """Возвращает 1 маршрут"""
    if not Service.objects.filter(id=id).exists():
        return Response(f"Такого маршрута нету")
    transition = get_object_or_404(Service, id=id)
    serializer = ServiceSerializer(transition)
    return Response(serializer.data)


@api_view(['Put'])
def put_service(request, id, format=None):
    """Обновляет информацию об услуге"""
    req = get_object_or_404(Service, id=id)
    serializer = ServiceSerializer(req, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def del_service(request, id, format=None):
    """Удаляет маршрут"""
    if not Service.objects.filter(id=id).exists():
        return Response(f"Маршрута с таким id не существует!")
    option = Service.objects.get(id=id)
    option.status = False
    option.save()

    options = Service.objects.filter(status=False)
    serializer = ServiceSerializer(options, many=True)
    return Response(serializer.data)


@api_view(['Post'])
def add_to_request(request, id):
    """добавить опцию в заявку, если нет открытых заявок, то создать"""
    if not Service.objects.filter(id=id).exists():
        return Response(f"Маршрута с таким id не существует!")

    service = Service.objects.get(id=id)

    req = Request.objects.filter(status=1).last()

    if req is None:
        req = Request.objects.create(user_id=user.id)

    time = request.data.get("time", 1)
    try:
        request_service = RequestService.objects.get(request=req, service=service)
        request_service.amount += int(time)
        request_service.save()
    except RequestService.DoesNotExist:
        request_service = RequestService(request=req, service=service, time=time)
        request_service.save()

    return Response(status=200)


@api_view(['Get'])
def get_requests(request, format=None):
    """Возвращает список заявок"""
    appointments = Request.objects.all()
    serializer = RequestSerializer(appointments, many=True)
    return Response(serializer.data)


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
            service_entry = service_serializer.data.copy()
            service_entry['time'] = app_service.time
            service_data.append(service_entry)

        request_data['service'] = service_data

        return Response(request_data)


@api_view(['Put'])
def update_by_user(request, id):
    if not Request.objects.filter(id=id).exists():
        return Response(f"Заявки с таким id не существует!")

    request_status = request.data["status"]

    if int(request.data["status"]) not in [2, 3]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    application = Request.objects.get(id=id)
    app_status = application.status

    if int(request.data["status"]) in [3]:
        application.formed_at = timezone.now()

    application.status = request_status
    application.save()

    serializer = RequestSerializer(application, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
def update_by_admin(request, id):
    if not Request.objects.filter(id=id).exists():
        return Response(f"Заявки с таким id нет")

    application = Request.objects.get(id=id)

    if int(application.status) == 2:
        return Response("Такой заявки нет на проверке")

    valid_statuses = [4, 3]

    # Ensure 'status' key is present in the request data
    request_status = request.data.get("status")

    if request_status is None or int(request_status) not in valid_statuses:
        return Response("Неверный статус!")

    application.status = request_status
    application.publication_date = datetime.now().date()
    application.save()

    serializer = RequestSerializer(application)
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_request(request, id, format=None):
    """Удаляет информацию о заявке"""
    if not Request.objects.filter(id=id).exists():
        return Response(f"Заявки с таким id нет")

    application = get_object_or_404(Request, id=id)

    if application.status == '1':
        application.delete()
        return Response("Заявка успешно удалена.")
    else:
        return Response("Невозможно изменить статус заявки. Текущий статус не равен 1.", status=status.HTTP_400_BAD_REQUEST)

@api_view(['Delete'])
def delete_service_from_request(request, request_id, service_id):
    """Удалить конкретную услугу из конкретной заявки"""
    if not Request.objects.filter(id=request_id).exists():
        return Response("Заявки с таким id не существует", status=status.HTTP_404_NOT_FOUND)

    if not Service.objects.filter(id=service_id).exists():
        return Response("Маршрута с таким id не существует", status=status.HTTP_404_NOT_FOUND)

    request = Request.objects.get(id=request_id)
    service = Service.objects.get(id=service_id)

    request.requestservice_set.filter(service=service).delete()
    request.save()

    return Response("Маршрут успешно удален из заявки", status=status.HTTP_204_NO_CONTENT)
