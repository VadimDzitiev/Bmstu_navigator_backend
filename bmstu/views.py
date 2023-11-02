from .models import Service
from django.shortcuts import render
from .models import Service, Request, UserProfile, RequestService


def GetCampus(request, id):
    data1 = Service.objects.get(id=id)
    return render(request, 'campus.html', {'data': data1})

def GetCampuses(request):
    query = request.GET.get('Маршрут', '')
    if query == '':
        main = Service.objects.filter(status=True)
    else:
        main = Service.objects.filter(status=True, name__contains=query)

    return render(request, 'campuses.html', {'main': main, 'query_c': query})

def freezeTransition(request,account_id):
    query = request.GET.get('Маршрут', '')
    Service.objects.filter(id=account_id).update(status=False)
    return render(request, 'campuses.html', {'main': Service.objects.filter(status=True), 'query_c': query})
