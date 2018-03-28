from django.test import TestCase
import re


# def validateEmail(email):
#     if len(email) > 7:
#         if re.match(r"^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
#             # return 1
#             print(1)
#     # return 0
#     print(0)

import threading

# s = threading.Thread()
#
# def ValidateEmail(email):
#     from django.core.validators import validate_email
#     from django.core.exceptions import ValidationError
#     try:
#         validate_email(email)
#         return True
#     except ValidationError:
#         return False

# email = 'fdasfadsadlkjf@qq.comxas.dsa'
# print(ValidateEmail(email))

teacher_list = [{'id': 1, 'name': 'mike', 'email': 'mike@qq.com', 'cls__id': 2, 'cls__caption': 'Java1班'}, {'id': 1, 'name': 'mike', 'email': 'mike@qq.com', 'cls__id': 3, 'cls__caption': 'java2班'}, {'id': 1, 'name': 'mike', 'email': 'mike@qq.com', 'cls__id': 4, 'cls__caption': 'java3班'}, {'id': 2, 'name': 'will', 'email': 'will@qq.com', 'cls__id': 1, 'cls__caption': 'c++1班'}, {'id': 2, 'name': 'will', 'email': 'will@qq.com', 'cls__id': 4, 'cls__caption': 'java3班'}, {'id': 3, 'name': 'jerry', 'email': 'jerry@qq.com', 'cls__id': 4, 'cls__caption': 'java3班'}, {'id': 3, 'name': 'jerry', 'email': 'jerry@qq.com', 'cls__id': 6, 'cls__caption': 'web2班'}, {'id': 4, 'name': 'jessica', 'email': 'jessica@qq.com', 'cls__id': 8, 'cls__caption': 'web4班'}, {'id': 5, 'name': 'jeson', 'email': 'jeosn@qq.com', 'cls__id': None, 'cls__caption': None}]

result = {}

for item in teacher_list:
    if item['id'] in result:
        if item['cls__id']:
            result[item['id']]['cls_list'].append({'cls__id': item['cls__id'], 'cls__caption': item['cls__caption']})
    else:
        if item['cls__id']:
            temp = [
                    {'cls__id': item['cls__id'], 'cls__caption': item['cls__caption']},
                ]
        else:
            temp = []
        result[item['id']] = {
                'nid': item['id'],
                'name': item['name'],
                'email': item['email'],
                'cls_list': temp
            }

print(result)


results = {
    1: {
        'nid': 1,
        'name': 'mike',
        'email': 'mike@qq.com',
        'cls_list': [
            {'id': 1, 'caption': 'ssss'},
            {'id': 2, 'caption': 'sada'}
        ]
    },
    2: {
        'nid': 3,
        'name': 'will',
        'email': 'will@qq.com',
        'cls_list': [
            {'id': 1, 'caption': 'ssss'},
            {'id': 2, 'caption': 'sada'}
        ]
    },
}
a = {
    1: {
        'nid': 1,
        'name': 'mike',
        'email': 'mike@qq.com',
        'cls_list': [
            {'cls__id': 2, 'cls__caption': 'Java1班'},
            {'cls__id': 3, 'cls__caption': 'java2班'},
            {'cls__id': 4, 'cls__caption': 'java3班'}
        ]
    },
}