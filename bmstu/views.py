from django.shortcuts import render
from .models import *  # Подставьте свою модель, если необходимо
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from bmstu.models import Service, Request, UserProfile, RequestService
from bmstu.serializers import ServiceSerializer, RequestSerializer, UserProfileSerializer, RequestServiceSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
import psycopg2
import base64
from PIL import Image

def GetCampus(request, id):
    appointments = Service.objects.filter(id=id)
    for appointment in appointments:
        if appointment.transition:
            data = bytes(appointment.transition)  # Преобразовать memoryview в bytes
            appointment.transition = (data.decode())

    return render(request, 'campus.html', {'data': appointments})

def GetCampuses(request):
    query = request.GET.get('Маршрут', '')
    if query == '':
        appointments = Service.objects.filter(status=True)
    else:
        appointments = Service.objects.filter(status=True, name__contains=query)
    for appointment in appointments:
        if appointment.buildings:
            data = bytes(appointment.buildings)
            appointment.buildings = (data.decode())

    return render(request, 'campuses.html', {'main': appointments, 'query_c': query})


def freezeTransition(request, account_id):
    query = request.GET.get('Маршрут', '')
    Service.objects.filter(id=account_id).update(status=False)
    appointments = Service.objects.filter(status=True)
    for appointment in appointments:
        if appointment.buildings:
            data = bytes(appointment.buildings)  # Преобразовать memoryview в bytes
            appointment.buildings = (data.decode())
    return render(request, 'campuses.html', {'main': appointments, 'query_c': query})

###################################################################################

@api_view(['Get'])#список+
def get_list_services(request, format=None):
    """Возвращает список услуг"""
    print('get_services')
    service = Service.objects.all()
    serializer = ServiceSerializer(service, many=True)
    return Response(serializer.data)

@api_view(["GET"])#одна запись+
def get_service(request, id):
    if not Service.objects.filter(pk=id).exists():
        return Response(f"Такой услуги нету")
    print('get_service')
    transition = get_object_or_404(Service, id=id)
    serializer = ServiceSerializer(transition)
    return Response(serializer.data)

@api_view(['Post'])#добавление+
def post_service(request, format=None):
    """Добавляет новую услугу"""
    print('post_service')
    serializer = ServiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['Put'])#изменение+
def put_detail_service(request, id, format=None):
    """Обновляет информацию об услуге"""
    appointment = get_object_or_404(Service, id=id)
    serializer = ServiceSerializer(appointment, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    print('put_service')
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['Put'])#"удаление"+
def del_service(request, id, format=None):
    """Обновляет информацию об услуге"""
    service = Service.objects.get(id=id)
    service.is_deleted = False
    service.save()
    service = Service.objects.filter(status=True)
    serializer = ServiceSerializer(service, many=True)
    return Response(serializer.data)

@api_view(['Post'])#добавление в заявку
def post_service_in_request(request, id, format=None):
    """Добавляет услугу в последнюю заявку"""
    new_appapp = RequestService.objects.create(
        request=Request.objects.latest('id'),
        service=Service.objects.get(id=id)
    )
    print('post_service in request')
    new_appapp.save()
    serializer = RequestServiceSerializer(new_appapp)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

#добавить опцию в заявку
@api_view(['POST'])
def add_to_request(request, pk):
    if not Service.objects.filter(id=id).exists():
        return Response(f"Опции с таким id не существует!")
    service = Service.objects.get(id=pk)
    request = Request.objects.filter(status=True).last()
    try:
        request_service = RequestService.objects.get(request=request, service=service)
        request_service.save()
    except RequestService.DoesNotExist:
        request_service = RequestService(request=request, service=service)
        request_service.save()

    return Response(status=200)

# @api_view(['Delete'])#удаление+
# def delete_service(request, id, format=None):
#     """Удаляет информацию о услуге"""
#     print('delete_service')
#     stock = get_object_   or_404(Service, id=id)
#     stock.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)

###################################################################################

@api_view(['Get'])#+
def get_list_requests(request, format=None):
    """Возвращает список заявок"""
    print('get_request')
    appointments = Request.objects.all()
    serializer = RequestSerializer(appointments, many=True)
    return Response(serializer.data)

@api_view(['Post'])#+
def post_request(request, format=None):
    """Добавляет новую заявку"""
    print('post_request')
    serializer = RequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['Delete'])#+
def delete_request(request, id, format=None):
    """Удаляет информацию о заявке"""
    stock = get_object_or_404(Request, id=id)
    stock.delete()
    print('delete_request')
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["DELETE"])#удалить конкретную услугу из конкретной заявки
def delete_service_from_request(request, request_id, service_id):
    if not Request.objects.filter(id=request_id).exists():
        return Response("Заявки с таким id не существует", status=status.HTTP_404_NOT_FOUND)

    if not Service.objects.filter(id=service_id).exists():
        return Response("Услуги с таким id не существует", status=status.HTTP_404_NOT_FOUND)

    request = Request.objects.get(id=request_id)
    service = Service.objects.get(id=service_id)

    request.requestsservice_set.filter(service=service).delete()
    request.save()

    return Response("Услуга успешно удалена из заявки", status=status.HTTP_204_NO_CONTENT)
###################################################################################

@api_view(['Get'])
def get_list_requestservices(request, format=None):
    """Возвращает список заявок в запросах"""
    print('get_RequestService')
    appointments = RequestService.objects.all()
    serializer = RequestServiceSerializer(appointments, many=True)
    return Response(serializer.data)

@api_view(['Put'])
def put_requestservice(request, id, format=None):
    """Добавляет новый запрос в заявку"""
    appointment = get_object_or_404(RequestService, id=id)
    serializer = RequestServiceSerializer(appointment, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    print('put_RequestService')
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['Delete'])
def delete_requestservice(request, id1, id2, format=None):
    """удаление заявки"""
    stock = get_object_or_404(RequestService, request=id1,service=id2)
    stock.delete()
    print('delete_RequestService')
    return Response(status=status.HTTP_204_NO_CONTENT)
###################################USER###############################################

@api_view(['Get'])#+
def get_list_userprofiles(request, format=None):
    """Возвращает список пользователей"""
    print('get_userpofile')
    service = UserProfile.objects.all()
    serializer = UserProfileSerializer(service, many=True)
    return Response(serializer.data)

@api_view(['Post'])#+
def post_userprofile(request, format=None):
    """Добавляет пользователя"""
    serializer = UserProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    print('post_userprofile')
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['Delete'])#+
def delete_userprofile(request, id, format=None):
    """Удаляет информацию о пользователе"""
    stock = get_object_or_404(UserProfile, id=id)
    stock.delete()
    print('delete_userprofile')
    return Response(status=status.HTTP_204_NO_CONTENT)