from django.shortcuts import render

data = {'transitions': [
            {'from': 'МТ', 'to': 'Главный кампус', 'id': 1, 'transition_time':8,'transition': 'Маршрут из МТ в Главное здание', 'img_url': '/pictures/МТ-ГЗ.png','transition_img': '/pictures/МТ-ГЗ Маршрут.PNG'},
            {'from': 'Главный кампус', 'to':'Энерго','id': 2, 'transition_time':4,'transition':'Маршрут из Главного здания в Энерго','img_url':'/pictures/ГЗ-Э.png','transition_img':'/pictures/ГЗ-Э Маршрут.png'},
            {'from': 'Энерго', 'to':'СМ','id': 3, 'transition_time':2,'transition':'Маршрут из Энерго в СМ','img_url':'/pictures/Э-СМ.png','transition_img':'/pictures/Э-СМ Маршрут.PNG'},
            {'from': 'СМ', 'to':'УЛК','id': 4, 'transition_time':5,'transition':'Маршрут из СМ в УЛК','img_url':'/pictures/СМ-УЛК.png','transition_img':'/pictures/СМ-УЛК Маршрут.PNG'},
            {'from': 'УЛК', 'to':'СК','id': 5, 'transition_time':15,'transition':'Маршрут из УЛК в СК','img_url':'/pictures/УЛК-СК.png','transition_img':'/pictures/УЛК-СК Маршрут.PNG'}]}

def GetCampus(request, id):
    new_data={}
    data['choosen_transition'] = id
    for campus in data['transitions']:
        if id == campus['id']:
            new_data = campus
    return render(request, 'campus.html',  {'data': new_data})

def GetCampuses(request):
    query = request.GET.get('Маршрут','')
    if query == '':
        return render(request, 'campuses.html', {'data':{'main': data, 'query_c': query}})
    else:
        result = {'transitions': []}
        for transition in data['transitions']:
            if query in transition['from'] or query in transition['to']:
                result['transitions'].append(transition)
        return render(request, 'campuses.html', {'data':{'main': result, 'query_c': query}})
