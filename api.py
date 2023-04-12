import requests
import json

next = 'https://swapi.dev/api/people/?page=1'
employees = []

while next != None:
    # print(next)
    response_API = requests.get(next)
    # print(response_API.status_code)
    data = response_API.text
    json_format = json.loads(data)
    employees.extend(json_format['results'])
    # print(json_format['results'])
    next = json_format['next']


print(employees)
