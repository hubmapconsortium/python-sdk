import requests


def make_request(method_type, instance, url, optional_argument=None, data=None):
    if optional_argument is None:
        optional_argument = ''
    if data is None:
        if instance.token is None:
            if method_type == 'get':
                r = requests.get(url + optional_argument)
            if method_type == 'put':
                r = requests.get(url + optional_argument)
            if method_type == 'post':
                r = requests.get(url + optional_argument)
        else:
            if method_type == 'get':
                r = requests.get(url + optional_argument, headers=instance.header)
            if method_type == 'put':
                r = requests.get(url + optional_argument, headers=instance.header)
            if method_type == 'post':
                r = requests.get(url + optional_argument, headers=instance.header)
    else:
        if instance.token is None:
            if method_type == 'get':
                r = requests.get(url + optional_argument, json=data)
            if method_type == 'put':
                r = requests.get(url + optional_argument, json=data)
            if method_type == 'post':
                r = requests.get(url + optional_argument, json=data)
        else:
            if method_type == 'get':
                r = requests.get(url + optional_argument, headers=instance.header, json=data)
            if method_type == 'put':
                r = requests.get(url + optional_argument, headers=instance.header, json=data)
            if method_type == 'post':
                r = requests.get(url + optional_argument, headers=instance.header, json=data)
    if r.status_code > 299:
        err = r.json()['error']
        error = f"{r.status_code} {err}"
        raise Exception(error)
    else:
        return r.json()
