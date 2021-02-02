import httpie
import json
import requests

def post():
    data = {
        'title':'api',
        'description':'123654789',
        'starting_date':'2021-02-12',
        'ending_date':'2021-02-13',
        'status':'panding',
    }

    login_data = {
        "username":'rakesh@gmail.com',
        'password':"123456"
    }

    headers = {
        "content-type":'application/json'
    }

    login_url = "http://127.0.0.1:8000/api/login/"
    url = "http://127.0.0.1:8000/api/leave/"
    json_login_data = json.dumps(login_data)
    json_data = json.dumps(data)

    login_r = requests.post(url=login_url,headers=headers, data=json_login_data)
    r = requests.post(url=url,headers=headers, data=json_data)
    data = r.json()
    print('login', login_r)
    print('data', data)

