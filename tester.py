import requests
import json

APP_TOKEN = 'PX6eUmgv4th7GKqhqDr8E5AZt8SFi2Ja'

session = requests.Session()


def get_data(url, data):
    data2 = {
        'app_token': APP_TOKEN,
        'format': 'json'

    }

    data.update(data2)

    s = '?'
    for k in data:
        s += k + '=' + str(data[k]) + '&'

    r = session.get('http://tochkasbora.pythonanywhere.com/' + url + s)
    print(r.url)
    print(data)
    return json.loads(r.text)

phone = '+7 9032281480'

data = get_data(f"api/try_authentication", {'phone': phone})
if not data['success']:
    print("неизвестная ошибка")

print(data)

if data['user_founded']:
    print("попытка входа")
    data = get_data(f"api/init_authentication", {'phone': phone })
    if not data['success']:
        print("пользователь не найден. вы отправляли запрос 'api/try_authentication'?")
    data = get_data(f"api/authenticate_user", {'phone': phone, 'passcode': '1986' })
    if not data['success']:
        print("пароль из смс не совпал")
    print(data)

    token = data['token']

    data = get_data(f"api/user_info", {'token': token })
    print(data)

    data = get_data(f"api/user_garbage_info", {'token': token })
    print(data)

    data = get_data(f"api/collection_places_list", {'token': token })
    print(data)

    data = get_data(f"api/markets_list", {'token': token })
    print(data)

    data = get_data(f"api/market_items_list", {'token': token })
    print(data)

    data = get_data(f"api/market_item_info", {'token': token , 'id': 1 })
    print(data)
else:
    print("регистрация")
    data = get_data("api/create_user", {'phone': phone, 'passcode': 1986, 'first_name':'fname', 'last_name':'lname', 'patronymic':'otchestvo' })
    if not data['success']:
        print("ошибка регистрации")
