import requests
from rest_framework.response import Response
from .models import Service
import requests


def update_status_refer(account_id):
    print(account_id)
    # service = Service.objects.get(id=account_id)
    # # print(service.transition_time)
    # payload = {
    #     "id": service.id,
    #     "transition_time": service.transition_time,
    # }
    # headers = {
    #     "Authorization": "secret-async-key"
    # }
    # # print(payload)
    # response = requests.post("http://localhost:8080/set_status", json=payload, headers=headers)
    # if response.status_code == 200:
    #     print("Запрос успешно отправлен")
    # else:
    #     print(f"Ошибка при отправке запроса: {response.status_code}")
    # return response
